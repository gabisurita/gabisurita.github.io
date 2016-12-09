Testing an OpenAPI Spec with Bravado
####################################

:tags: Swagger, OpenAPI, Bravado, Testing, Python
:date: 2016-12-09 01:22
:category: OpenAPI
:author: Gabriela Surita
:slug: openapi-logic-validation


`OpenAPI <https://github.com/OAI/OpenAPI-Specification>`_ (formally known as Swagger)
is a standard to describe REST APIs on a computer and human readable way.
It can be used with several utilities, like automated server and client code generation,
generating interactive documentation, prototyping and mock testing.

The Swagger way of describing an API usually assumes you are creating the Spec **before**
coding the API. What is expected using this workflow is that everything after the spec
should follow and comply with it. There are several ways to ensure that the server
and the clients are matching a spec, but lets imagine another use case where you already
have a complex API running, a static documentation and you want to generate an OpenAPI
description of the application.
In this case, the running app should be the source of truth and the compliance
of the spec should be tested.

For this simple tutorial I'll be using
`Pyramid <http://docs.pylonsproject.org/projects/pyramid/en/latest/index.html>`_
as a server and
`Bravado <https://github.com/Yelp/bravado>`_
for the spec testing, which is a cool app
maintained by Yelp which allows generate clients for Swagger powered server on runtime.
It doesn't have a fairly comprehensive documentation though.

Before we start I suggest that if you want to follow this tutorial in detail,
you should clone it on `Github <https://github.com/gabisurita/swagger-testing-tutorial>`_,
start a *virtualenv* and install the Python requirements.

.. code-block:: bash

    git clone https://github.com/gabisurita/swagger-testing-tutorial
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

So lets start! Imagine we have Pyramid App on `app.py` as follows:


Pyramid Server Example
----------------------

.. code-block:: python

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.view import view_config


    @view_config(route_name='hello', renderer='json')
    def hello_view(request):
        return {'hello': request.matchdict['name']}


    def setup():
        config = Configurator()
        config.add_route('hello', '/hello/{name}')
        config.scan()
        app = config.make_wsgi_app()
        return app


    if __name__ == '__main__':
        app = setup()
        server = make_server('0.0.0.0', 8080, app)
        server.serve_forever()


You can try the server running it with Python and making browser httpie or CURL requests.

.. code-block:: bash

    python app.py &
    curl localhost:8080/hello/gabi


OpenAPI description
-------------------

The equivalent OpenAPI/Swagger specification on ``swagger.yaml`` for our app is

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


We can now go ahead and test our description.

Testing using Bravado
---------------------

Now, the next step is to write tests for our specification. For this first example
we'll consider testing with a running instance of the API and we'll use Bravado to
make requests to it. Notice that you'll need to start the server prior to running
the tests. Consider the following `test_bravado.py` file.

.. code-block:: python

    import unittest

    from bravado.client import SwaggerClient, SwaggerMappingError
    from bravado.swagger_model import load_file
    from jsonschema.exceptions import ValidationError


    class TestSwaggerBravado(unittest.TestCase):

        def setUp(self):
            self.client = SwaggerClient.from_spec(load_file('swagger.yaml'))

        def test_hello_validate_required_fields(self):
            get_hello = self.client.hello.get_hello
            self.assertRaises(SwaggerMappingError, get_hello)

        def test_hello_validate_name_type(self):
            get_hello = self.client.hello.get_hello
            self.assertRaises(ValidationError, get_hello, name={})

        def test_get_hello_200(self):
            get_hello = self.client.hello.get_hello
            response = get_hello(name='Gabi').result()
            self.assertEquals(response.hello, 'Gabi')


You may run it with:

.. code-block:: bash

    python app.py &
    pytest test_bravado.py

This is cool, but has some limitations, like what if we don't want to run an
instance of the server in parallel and use something like WebTest to encapsulate
our web app?

Testing using Bravado Core and WebTest
--------------------------------------

The answer is we can validate requests, responses and objects using Bravado core.
This increases a bit the amount of code needed, but allow us more modularity.

.. code-block:: python

    import yaml
    import unittest
    from webtest import TestApp

    from bravado_core.spec import Spec
    from bravado_core.resource import build_resources
    from bravado_core.request import IncomingRequest, unmarshal_request
    from bravado_core.response import OutgoingResponse, validate_response
    from bravado_core.swagger20_validator import ValidationError

    from app import setup


    class TestSwaggerBravadoCore(unittest.TestCase):

        def setUp(self):
            self.app = TestApp(setup())

            self.spec_dict = yaml.load(open('swagger.yaml'))
            self.spec = Spec.from_dict(self.spec_dict)
            self.resources = build_resources(self.spec)

        def create_bravado_request(self):
            """Auxiliary method to create a blank Bravado request."""

            request = IncomingRequest()
            request.path = {}
            request.query = {}
            request._json = {}
            request.json = lambda: request._json

            return request

        def cast_bravado_response(self, response):
            """Auxiliary method to cast webtest response as Bravado response."""

            resp = OutgoingResponse()
            resp.text = response.body
            resp.headers = response.headers
            # Drop charset (it's a bug on Pyramid <= 1.7.3)
            resp.content_type = response.headers.get('Content-Type').split(';')[0]
            resp.json = lambda: response.json

            return resp

        def test_hello_validate_required_fields(self):
            op = self.resources['hello'].get_hello
            request = self.create_bravado_request()

            self.assertRaises(ValidationError, unmarshal_request, request, op)

        def test_hello_validate_name_type(self):
            op = self.resources['hello'].get_hello
            request = self.create_bravado_request()
            request.path = {'name': {}}

            self.assertRaises(ValidationError, unmarshal_request, request, op)

        def test_get_hello_200(self):
            op = self.resources['hello'].get_hello
            request = self.create_bravado_request()
            request.path = {'name': 'Gabi'}
            params = unmarshal_request(request, op)

            response = self.app.get(op.path_name.format(**params))
            response = self.cast_bravado_response(response)

            schema = self.spec.deref(op.op_spec['responses']['200'])

            validate_response(schema, op, response)
            self.assertEquals(response.json()['hello'], 'Gabi')


And now you can test it only with:

.. code-block:: bash

    pytest test_bravado_core.py

So, I hope that you found this helpful! Fell free to contact me for upgrades
on this tutorial by email or opening an issue on it's repository. See you! :)
