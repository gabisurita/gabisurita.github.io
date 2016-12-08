Testing an OpenAPI Spec with Python
###################################

:tags: Swagger, OpenAPI, Testing, Python
:date: 2016-12-07 11:57
:category: Outreachy
:author: Gabriela Surita
:slug: openapi-logic-validation
:description: About outreachy

`OpenAPI <https://github.com/OAI/OpenAPI-Specification>`_ (formally known as Swagger)
is a standard describe REST APIs on a computer and human readable way.
It can be used with several utilities, like automated server and client code generation,
generating interactive documentation and mock testing.

The Swagger way of describing an API usually assumes you are creating the Spec **before**
coding the API. What is expected using this workflow is that everything after the spec
should follow and comply with it. There are several ways to ensure that the server
and the clients are matching a spec, but lets imagine another use case where you already
have a complex API running, a static documentation and you want to generate an OpenAPI
description of the application.
In this case, the running app should be the source of truth and the compliance
of the spec should be tested.

For this simple tutorial I'll be using Python and Bravado, which is a cool app
maintained by Yelp to generate clients for Swagger on runtime. So imagine we have
Pyramid or a Flask App like follows:

Pyramid Server Example
----------------------

.. code-block:: python

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response
    import json

    def hello(request):
        return json.dumps({'hello': '{name}'.format(request.matchdict)})

    if __name__ == '__main__':
        config = Configurator()
        config.add_route('hello', '/hello/{name}')
        config.add_view(hello, route_name='hello')
        app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 8080, app)
        server.serve_forever()


Flask Server Example
--------------------

.. code-block:: python

    import Flask
    import json

    app = Flask(__name__)

    @app.route("/hello/<name>")
    def hello(name):
        return json.dumps({'hello': name})

    if __name__ == "__main__":
        app.run()


OpenAPI description
-------------------

.. code-block:: yaml

    swagger: '2.0'
    info:
      version: '0.0.0'
      title: Hello API
    host: 0.0.0.0:8080
    basePath: /
    schemes:
      - http

    paths:
      '/hello/{name}':
        get:
          produces:
            - application/json
          parameters:
            - name: name
              in: path
              description: Your name.
              required: true
              type: string
          responses:
            '200':
              description: Hello message.
              schema:
                $ref: '#/definitions/Hello-object'

    definitions:
      Hello-object:
        type: object
        properties:
          hello:
            type: string
        required:
          - hello


Testing using Bravado
---------------------

Testing using Bravado Core
--------------------------


