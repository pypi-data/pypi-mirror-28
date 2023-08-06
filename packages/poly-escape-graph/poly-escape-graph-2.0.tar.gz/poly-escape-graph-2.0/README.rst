============
Poly Graph
============

Quickstart
----------

Install poly-escape-graph::

    pip install poly-escape-graph


Then use it in a project::

    from poly_escape_graph import Node
    from flask import request, jsonify

    class MyNode(Node):
        def listen(self):
            data: dict = request.json
            # process data
            return jsonify(status=OK)

    MyNode().run(5001)

