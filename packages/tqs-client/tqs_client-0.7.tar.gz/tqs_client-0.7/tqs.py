import base64
import contextlib
import datetime
import json
import requests
import time
import random


USER_AGENT = "TQS-Client/0.1 Python/3.6.3" # TODO Runtime


def encode_body(body):
    if type(body) == str:
        return body, "text/plain"
    if type(body) == bytes:
        return base64.b64encode(body).decode("ascii"), "application/octet-stream"
    if type(body) in (list, dict):
        return json.dumps(body), "application/json"
    raise Error("Don't know how to encode body of type <%s>" % type(body).__name__)


def decode_body(body_data, body_type):
    if body_type in (None, "text/plain"):
        return body_data
    if body_type == "application/octet-stream":
        return base64.b64decode(body_data)
    if body_type == "application/json":
        return json.loads(body_data)
    raise Error("Don't know how to decode body of type <%s>" % body_type)


def partition_all(n, coll, step=None):
    return (coll[i:i+n] for i in range(0, len(coll), step or n))


class Message:

    def __init__(self, queue, message):
        self.queue = queue
        self.message = message
        self.decoded_body = decode_body(self.body_text, self.body_type)

    def delete(self):
        r = requests.delete(self.queue.queue_url + "/leases/" + self.message["lease_uuid"], headers=self.queue.headers)
        r.raise_for_status()

    @property
    def body(self):
        return self.decoded_body

    @property
    def body_text(self):
        return self.message["body"] # TODO Should become body_text

    @property
    def body_type(self):
        return self.message["type"] # TODO Should become body_type

    @property
    def create_date(self):
        return datetime.datetime.fromtimestamp(self.message["create_date"])

    @property
    def visible_date(self):
        return datetime.datetime.fromtimestamp(self.message["visible_date"])

    @property
    def expire_date(self):
        return datetime.datetime.fromtimestamp(self.message["expire_date"])

    @property
    def lease_uuid(self):
        if "lease_uuid" in self.message:
            return self.message["lease_uuid"]

    @property
    def lease_date(self):
        if "lease_date" in self.message:
            return datetime.datetime.fromtimestamp(self.message["lease_date"])

    @property
    def lease_timeout(self):
        if "lease_timeout" in self.message:
            return self.message["lease_timeout"]


class QueuePoller:

    def __init__(self, queue, batch_size=1, auto_delete=False, wait_time=0, done_check=None):
        self.queue = queue
        self.batch_size = batch_size
        self.batch = []
        self.auto_delete = auto_delete
        self.wait_time = wait_time
        self.delay_time = 2.5
        self.done_check = done_check
        if not self.done_check:
            self.done_check = lambda: True

    def __iter__(self):
        return self

    def __next__(self):
        params = { "message_count": self.batch_size }
        if self.auto_delete is True:
            params["delete"] = "true"
        if self.wait_time != 0:
            params["wait_time"] = str(self.wait_time)
        while True:
            if self.done_check():
                raise StopIteration()
            start_time = time.time()
            if len(self.batch) == 0:
                r = requests.get(self.queue.queue_url, params=params, headers=self.queue.headers, timeout=self.wait_time+5)
                r.raise_for_status()
                result = r.json()
                self.batch = result["messages"]
            if len(self.batch) > 0:
                return Message(self.queue, self.batch.pop())
            if time.time() - start_time < self.delay_time:
                time.sleep(self.delay_time) # This could be exponential


class Queue:

    def __init__(self, endpoint, queue_name, api_token=None):
        self.endpoint = endpoint
        self.queue_name = queue_name
        self.api_token = api_token
        self.headers = {"User-Agent": USER_AGENT}
        if self.api_token:
            self.headers["Authentication"] = "token " + self.api_token
        self.queue_url = "%s/queues/%s" % (self.endpoint, self.queue_name)

    def exists(self):
        r = requests.get(self.endpoint + "/queues", headers=self.headers)
        r.raise_for_status()
        for queue in r.json()["queues"]:
            if queue["name"] == self.queue_name:
                return True
        return False

    def create(self):
        r = requests.post(self.endpoint + "/queues", json={"name": self.queue_name}, headers=self.headers)
        r.raise_for_status
        return r.json()

    def put(self, body):
        body_data, body_type = encode_body(body)
        data = { "messages": [{"body": body_data, "type": body_type}] }
        r = requests.post(self.queue_url, json=data, headers=self.headers)
        r.raise_for_status()

    def put_many(self, bodies, batch_size=25):
        for partition in partition_all(batch_size, bodies):
            messages = []
            for body in partition:
                body_data, body_type = encode_body(body)
                messages.append({"body": body_data, "type": body_type})
            r = requests.post(self.queue_url, json={"messages": messages}, headers=self.headers)
            r.raise_for_status()

    # TODO This is essentially the same code as the poller
    def get(self, auto_delete=False):
        params = { "message_count": 1 }
        if auto_delete is True:
            params["delete"] = "true"
        r = requests.get(self.queue_url, params=params, headers=self.headers)
        r.raise_for_status()
        result = r.json()
        messages = result["messages"]
        if len(messages) > 0:
            return Message(self, messages[0])

    def messages(self, batch_size=1, auto_delete=False, wait_time=0, done_check=None):
        return QueuePoller(self, batch_size=batch_size, auto_delete=auto_delete, wait_time=wait_time, done_check=done_check)
