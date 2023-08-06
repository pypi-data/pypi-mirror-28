"""
    Node basis class

    Usage:

    >>> from poly_escape_graph import Node
    >>> class MyNode(Node):
            def listen(self):
                return "It's my node"
    >>> MyNode('My Node').run(port=5000)
"""
from collections import defaultdict
from typing import List

import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from requests import ReadTimeout

__all__ = ['Node']

OK = 'OK'
GET = 'GET'
POST = 'POST'
TAGS = 'tags'
SUBSCRIBER = 'subscriber'
SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI'
SQLALCHEMY_TRACK_MODIFICATIONS = 'SQLALCHEMY_TRACK_MODIFICATIONS'


class Node(Flask):
    """
        Base class for Plugins.
        Define the listen, subscribe and unsubscribe routes.
        The listen route may be overwritten by the subclasses.
        The method publish is here to send a message to the instance subscribers, it must not be overwritten.
        A subclass can add another route by using the method
            self.add_url_rule('/listen', 'listen', self.listen, methods=[POST])
        This method will, however, not be public and therefore, is only for internal uses
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self._config()
        self._create_db()
        self.add_url_rule('/info', 'info', self.info, methods=[GET])
        self.add_url_rule('/listen', 'listen', self.listen, methods=[POST])
        self.add_url_rule('/subscribe', 'subscribe', self.subscribe, methods=[POST])
        self.add_url_rule('/unsubscribe', 'unsubscribe', self.unsubscribe, methods=[POST])

    def _config(self):
        self.config.update(
            {
                SQLALCHEMY_DATABASE_URI: f'sqlite:///{self.name}.db',
                SQLALCHEMY_TRACK_MODIFICATIONS: False,
            }
        )

    def _create_db(self):
        self.db = SQLAlchemy(self)
        self.plugin = self._create_model('Plugin', self.db.Model,
                                         url=self.db.Column(self.db.String(200), primary_key=True),
                                         tag=self.db.Column(self.db.String(50), primary_key=True))
        self.db.create_all()

    def _create_model(self, name, *bases, **attributes):
        return type(name, bases, attributes)

    def info(self):
        """
            A basic route to get the info of the node
                The name of the node
                The subscribers of the node
        :return: a json response formatted as follows
                    {
                        "name": "Node",
                        "subscribers":
                        [
                            {"url": "subscriber-1", "tags": ["tag-1", "tag-2"]},
                            {"url": "subscriber-2", "tags": ["tag-2", "tag-3"]},
                            {"url": "subscriber-3", "tags": ["tag-3", "tag-1"]}
                        ]
                    }
        """
        subscribers = defaultdict(list)
        for plugin in self.plugin.query.all():
            subscribers[plugin.url].append(plugin.tag)
        return jsonify(name=self.name,
                       subscribers=[{"url": url, "tags": tuple(tags)} for url, tags in subscribers.items()])

    def listen(self):
        """
            Overwrite this
            The data of the POST http request can be found in the property request.json as a dict
        :return: {"status": "OK"}
        """
        self.logger.debug(f'{request.host_url} listen {request}={request.json}')
        return jsonify(status=OK)

    def publish(self, tags: List[str], files=None, **data):
        """
            This method send a message to all the subscribers
            This method may not be overwritten.
        :param files: files: (optional) Dictionary of couple {'name': file-tuple}
        :param tags: the list of tags used in the message
        :param data: a dict with the data for the subscribers
        :return: None
        """
        subscribers = set(plugin for tag in tags for plugin in self.db.session.query(self.plugin).filter_by(tag=tag))
        for subscriber in subscribers:
            self.logger.debug(f'{request.host_url} publish to {subscriber.url} with the tags={tags} and data={data}')
            try:
                self.logger.debug(requests.post(f'{subscriber.url}/listen',
                                                json={"tags": tags, "data": data}, files=files, timeout=0.1))
            except ReadTimeout as e:
                self.logger.warning(e)

    def subscribe(self):
        """
            This method subscribe the applicant to this service
            This method may not be overwritten.
        :return: {"status": "OK"}
        """
        data = request.json
        for tag in data[TAGS]:
            plugin = self.plugin(url=data[SUBSCRIBER], tag=tag)
            self.logger.debug(f'{plugin.url} subscribe to {request.host_url} with tag {tag}')
            self.db.session.add(plugin)
        self.db.session.commit()
        return jsonify(status=OK)

    def unsubscribe(self):
        """
            This method unsubscribe the applicant from this service
            This method may not be overwritten.
        :return: {"status": "OK"}
        """
        data = request.json
        for tag in data[TAGS]:
            plugin = self.db.session.query(self.plugin).filter_by(url=data[SUBSCRIBER], tag=tag).first()
            if plugin is not None:
                self.logger.debug(f'{plugin.url} unsubscribe to {request.host_url} with tag {tag}')
                self.db.session.delete(plugin)
        self.db.session.commit()
        return jsonify(status=OK)


if __name__ == '__main__':
    app = Node('Node')
    app.run(port=5000, debug=True)
