"""
    Node basis class

    Usage:

    >>> from poly_escape_graph import Node
    >>> Node().run(port=5000)

    >>> class MyNode(Node):
            def listen(self):
                return "It's my node"
    >>> MyNode().run(port=5000)
"""


from collections import defaultdict
from typing import List

import requests
from flask import Flask, request, jsonify


__all__ = ['Node']


OK = 'OK'
POST = 'POST'
TAGS = 'tags'
SUBSCRIBER = 'subscriber'


class Node:
    """
        Base class for Plugins.
        Define the listen, subscribe and unsubscribe routes.
        The listen route may be overwritten by the subclasses.
        The method publish is here to send a message to the instance subscribers, it must not be overwritten.
        A subclass can add another route by using the method
            self.app.route('route', methods=[get, post, ...])(function)
        This method will, however, not be public and therefore, is only for internal uses
    """

    def __init__(self, name=None):
        self._subscriptions = defaultdict(list)
        self.app = Flask(name or __name__)
        self.app.route('/listen', methods=[POST])(self.listen)
        self.app.route('/subscribe', methods=[POST])(self.subscribe)
        self.app.route('/unsubscribe', methods=[POST])(self.unsubscribe)

    def listen(self):
        """
            Overwrite this
            The data of the POST http request can be found in the property request.json
        :return: {"status": "OK"}
        """
        data: dict = request.json
        return jsonify(status=OK)

    def publish(self, tags: List[str], **data):
        """
            This method send a message to all the subscribers
            This method may not be overwritten.
        :param tags: the list of tags used in the message
        :param data: a dict with the data for the subscribers
        :return: None
        """
        for subscriber in set(subscriber for tag in tags for subscriber in self._subscriptions[tag]):
            requests.post(subscriber, json={"tags": tags, "data": data})

    def subscribe(self):
        """
            This method subscribe the applicant to this service
            This method may not be overwritten.
        :return: {"status": "OK"}
        """
        data = request.json
        for tag in data[TAGS]:
            self._subscriptions[tag].append(data[SUBSCRIBER])
        return jsonify(status=OK)

    def unsubscribe(self):
        """
            This method unsubscribe the applicant from this service
            This method may not be overwritten.
        :return: {"status": "OK"}
        """
        data = request.json
        for tag in data[TAGS]:
            self._subscriptions[tag].remove(data[SUBSCRIBER])
        return jsonify(status=OK)

    def run(self, port: int):
        self.app.run(port=port)


if __name__ == '__main__':
    Node().run(5000)
