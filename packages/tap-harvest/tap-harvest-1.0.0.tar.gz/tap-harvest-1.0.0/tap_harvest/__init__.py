#!/usr/bin/env python3

import datetime
import os

import backoff
import requests
import pendulum

import singer
from singer import utils
from tap_harvest.transform import transform


LOGGER = singer.get_logger()
SESSION = requests.Session()
REQUIRED_CONFIG_KEYS = [
    "start_date",
    "refresh_token",
    "client_id",
    "client_secret",
    "account_name",
]

BASE_URL = "https://{}.harvestapp.com/"
CONFIG = {}
STATE = {}
AUTH = {}

class Auth:
    def __init__(self, client_id, client_secret, refresh_token):
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._refresh_access_token()

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.RequestException),
        max_tries=5,
        giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500,
        factor=2)
    def _make_refresh_token_request(self):
        return requests.request('POST',
                                url='https://api.harvestapp.com/oauth2/token',
                                params={'client_id': self._client_id,
                                        'client_secret': self._client_secret,
                                        'refresh_token': self._refresh_token,
                                        'grant_type': 'refresh_token'})

    def _refresh_access_token(self):
        LOGGER.info("Refreshing access token")
        resp = self._make_refresh_token_request()
        expires_in_seconds = resp.json().get('expires_in', 17 * 60 * 60)
        self._expires_at = pendulum.now().add(seconds=expires_in_seconds)
        resp_json = {}
        try:
            resp_json = resp.json()
            self._access_token = resp_json['access_token']
        except KeyError as key_err:
            if resp_json.get('error'):
                LOGGER.critical(resp_json.get('error'))
            if resp_json.get('error_description'):
                LOGGER.critical(resp_json.get('error_description'))
            raise key_err
        LOGGER.info("Got refreshed access token")

    def get_access_token(self):
        if (self._access_token is not None and self._expires_at > pendulum.now()):
            return self._access_token

        self._refresh_access_token()
        return self._access_token


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schema(entity):
    return utils.load_json(get_abs_path("schemas/{}.json".format(entity)))


def get_start(key):
    if key not in STATE:
        STATE[key] = CONFIG['start_date']

    return STATE[key]


def get_url(endpoint):
    return BASE_URL.format(CONFIG['account_name']) + endpoint

@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.RequestException),
    max_tries=5,
    giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500,
    factor=2)
@utils.ratelimit(100, 15)
def request(url, params=None):
    params = params or {}
    params["access_token"] = AUTH.get_access_token()
    headers = {"Accept": "application/json"}
    req = requests.Request("GET", url=url, params=params, headers=headers).prepare()
    LOGGER.info("GET {}".format(req.url))
    resp = SESSION.send(req)
    resp.raise_for_status()
    return resp.json()

def append_times_to_dates(item, date_fields):
    if date_fields:
        for date_field in date_fields:
            if item.get(date_field):
                item[date_field] += "T00:00:00Z"

def sync_endpoint(endpoint, path, date_fields=None):
    schema = load_schema(endpoint)
    singer.write_schema(endpoint, schema, ["id"])
    start = get_start(endpoint)

    url = get_url(endpoint)
    for row in request(url):
        item = row[path]
        item = transform(item, schema)
        append_times_to_dates(item, date_fields)

        if item['updated_at'] >= start:
            singer.write_record(endpoint, item)
            utils.update_state(STATE, endpoint, item['updated_at'])

    singer.write_state(STATE)


def sync_projects():
    tasks_schema = load_schema("project_tasks")
    singer.write_schema("project_tasks", tasks_schema, ["id"])

    users_schema = load_schema("project_users")
    singer.write_schema("project_users", users_schema, ["id"])

    entries_schema = load_schema("time_entries")
    singer.write_schema("time_entries", entries_schema, ["id"])

    schema = load_schema("projects")
    singer.write_schema("projects", schema, ["id"])
    start = get_start("projects")

    start_dt = pendulum.parse(start)
    updated_since = start_dt.strftime("%Y-%m-%d %H:%M")

    url = get_url("projects")
    for row in request(url):
        item = row["project"]
        item = transform(item, schema)
        date_fields = ["starts_on", "ends_on", "hint_earliest_record_at", "hint_latest_record_at"]
        append_times_to_dates(item, date_fields)

        if item['updated_at'] >= start:
            singer.write_record("projects", item)
            utils.update_state(STATE, "projects", item['updated_at'])

        suburl = url + "/{}/user_assignments".format(item["id"])
        for subrow in request(suburl, params={"updated_since": updated_since}):
            subitem = subrow["user_assignment"]
            subitem = transform(subitem, users_schema)
            singer.write_record("project_users", subitem)

        suburl = url + "/{}/task_assignments".format(item["id"])
        for subrow in request(suburl, params={"updated_since": updated_since}):
            subitem = subrow["task_assignment"]
            subitem = transform(subitem, tasks_schema)
            singer.write_record("project_tasks", subitem)

        suburl = url + "/{}/entries".format(item["id"])
        subparams = {
            "from": start_dt.strftime("%Y%m%d"),
            "to": datetime.datetime.utcnow().strftime("%Y%m%d"),
            "updated_since": updated_since,
        }
        for subrow in request(suburl, params=subparams):
            subitem = subrow["day_entry"]
            subitem = transform(subitem, entries_schema)
            singer.write_record("time_entries", subitem)

    singer.write_state(STATE)


def sync_invoices():
    messages_schema = load_schema("invoice_messages")
    singer.write_schema("invoice_messages", messages_schema, ["id"])

    payments_schema = load_schema("invoice_payments")
    singer.write_schema("invoice_payments", payments_schema, ["id"])

    schema = load_schema("invoices")
    singer.write_schema("invoices", schema, ["id"])
    start = get_start("invoices")

    start_dt = pendulum.parse(start)
    updated_since = start_dt.strftime("%Y-%m-%d %H:%M")

    url = get_url("invoices")
    while True:
        data = request(url, {"updated_since": updated_since})
        for row in data:
            item = row["invoices"]
            item = transform(item, schema)
            append_times_to_dates(item, ["issued_at", "due_at"])

            singer.write_record("invoices", item)
            utils.update_state(STATE, "invoices", item['updated_at'])

            suburl = url + "/{}/messages".format(item['id'])
            for subrow in request(suburl):
                subitem = subrow["message"]
                if subitem['updated_at'] >= start:
                    append_times_to_dates(subitem, ["send_reminder_on"])
                    singer.write_record("invoice_messages", subitem)

            suburl = url + "/{}/payments".format(item['id'])
            for subrow in request(suburl):
                subitem = subrow["payment"]
                subitem = transform(subitem, payments_schema)
                if subitem['updated_at'] >= start:
                    singer.write_record("invoice_payments", subitem)

            singer.write_state(STATE)

        if len(data) < 50:
            break

    singer.write_state(STATE)


def do_sync():
    LOGGER.info("Starting sync")

    # Grab all clients and client contacts. Contacts have client FKs so grab
    # them last.
    sync_endpoint("clients", "client")
    sync_endpoint("contacts", "contact")

    # Get all people and tasks before grabbing the projects. When we grab the
    # projects we will grab the project_users, project_tasks, and time_entries
    # for each.
    sync_endpoint("people", "user")
    sync_endpoint("tasks", "task")
    sync_projects()

    # Sync expenses and their categories
    sync_endpoint("expense_categories", "expense_category")
    sync_endpoint("expenses", "expense", date_fields=["spent_at"])

    # Sync invoices and all related records
    sync_endpoint("invoice_item_categories", "invoice_category")
    sync_invoices()

    LOGGER.info("Sync complete")


def main_impl():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(args.config)
    global AUTH # pylint: disable=global-statement
    AUTH = Auth(CONFIG['client_id'], CONFIG['client_secret'], CONFIG['refresh_token'])
    STATE.update(args.state)
    do_sync()

def main():
    try:
        main_impl()
    except Exception as exc:
        LOGGER.critical(exc)
        raise exc


if __name__ == "__main__":
    main()
