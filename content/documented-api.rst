Building self-documented APIs
#############################

:tags: Swagger, OpenAPI, Kinto, Mozilla, Outreachy, cornice
:date: 2017-01-10 22:19
:category: OpenAPI
:author: Gabriela Surita
:slug: self-documented-apis


First, I'm sorry for taking too long since the last post, but I was a bit busy during
the holidays and one of the things that I was most involved in is this package called
`cornice.ext.swagger <https://github.com/Cornices/cornice.ext.swagger>`_,
which I'll explain soon.

As I mentioned on my blog post about `testing OpenAPI specification <testing-swagger-spec>`_
the OpenAPI/Swagger workflow usually assumes you are creating the specification before
coding the API there are many use cases where you already have
a working API or just wants to start with coding ASAP and just want to add
the documentation later.

Writing the specification by hand and testing it with ``Bravado`` or ``Flex``, like I did on
the last post, is somewhat fast approach that doesn't involving changing the API code.
This makes it useful for several cases, but when working with some huge APIs, it
can be tedious and lead to vagueness in the documentation, as it becomes
complicated for one or a small group of people to know all the aspects of the API.

To deal with this, a different approach is to use a documentation generator, which
I'll let you guess what it is.


OpenAPI documentation generators
--------------------------------

Well, time's up. An OpenAPI documentation generator does exactly what the name
suggests, it creates an OpenAPI specification directly from the API runnable code.
But how is that possible? Well, there are a few things that are part of the documentation
that are derived from code, but as there's no free lunch, there are a few
things that probably can't be extracted directly from the code, so you may need to add or patch
some things on the API to make it "self-documentable".

But that's enough talking -- let's try some examples. One cool package for building
such APIs using Flask is called
`flasgger <https://github.com/rochacbruno/flasgger>`_. You may install it with::

    $ pip install flasgger

And here follows a quick example:

.. code-block:: python

    from flask import Flask, jsonify
    from flasgger import Swagger

    app = Flask(__name__)
    Swagger(app)

    @app.route('/api/<string:username>')
    def user_api(username):
        """
        User API
        This resource returns user information
        ---
        tags:
          - users
        parameters:
          - name: username
            in: path
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: user_response
              properties:
                username:
                  type: string
                  description: The username
                  default: some_username

        """
        return jsonify({'username': username})


    app.run()


So if you check http://localhost:5000/spec you'll find the generated spec.
we can see that the path was automatically set and what we documented is right below.
The object schema we defined was also been broken into a reference at `definitions`
section.

.. code-block:: json

    {
        "swagger": "2.0",
        "info": {
            "description": "API description",
            "termsOfService": "Terms of service",
            "title": "A swagger API",
            "version": "1.0.1"
        },
        "paths": {
            "/api/{username}": {
                "get": {
                    "description": "This resource returns user information",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "username",
                            "required": true,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "A single user item",
                            "schema": {
                                "$ref": "#/definitions/user_api_get_user_response"
                            }
                        }
                    },
                    "summary": "User API",
                    "tags": [
                        "users"
                    ]
                }
            }
        },
        "definitions": {
            "user_api_get_user_response": {
                "properties": {
                    "username": {
                        "default": "some_username",
                        "description": "The username",
                        "type": "string"
                    }
                }
            }
        }
    }

So what did you think? In my opinion that's a lot better for some use cases than
providing a huge separate `swagger.yaml` file and not having the documentation close
to the code. Got interested on this? Please check some more examples
`at their repository <https://github.com/rochacbruno/flasgger>`_.
But some may think: can we do better? There's still a lot of
raw swagger in the docstring and that's something we usually don't want.
An answer I can give is that for `Cornice <https://github.com/Cornices/cornice>`, we can.


Cornice Swagger
---------------

`Cornice Swagger <https://github.com/Cornices/cornice.ext.swagger>`_
is an OpenAPI documentation generator for
`Cornice <https://github.com/Cornices/cornice>`_. For those who don't know,
Cornice is an extension for Pyramid that allows creating REST web services with almost
no effort. I'll assume some basic knowledge about Cornice, but you may be able to understand
even if you are unfamiliar with it. It also provides a very nice
`quickstart for peaple in a hurry <https://cornice.readthedocs.io/en/latest/quickstart.html>`_
that I totally recommend if this is the first time you hear that name.

You may install `cornice_swagger` package with::

    $ pip install cornice_swagger


Now let's try a simple app:

.. code-block:: python

    import colander
    from cornice import Service
    from cornice.service import get_services
    from cornice.validators import colander_body_validator
    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from cornice_swagger.swagger import CorniceSwagger

    _VALUES = {}

    # Create a simple service that will store and retrieve values
    values = Service(name='foo',
                     path='/values/{value}',
                     description="Cornice Demo")


    # Create a request schema for storing values
    class PutBodySchema(colander.MappingSchema):
        value = colander.SchemaNode(colander.String(),
                                    description='My precious value')


    # Create our cornice service views
    class MyValueApi(object):
        """My precious API."""

        @values.get()
        def get_value(request):
            """Returns the value."""
            key = request.matchdict['value']
            return _VALUES.get(key)

        @values.put(validators=(colander_body_validator, ),
                    schema=PutBodySchema())
        def set_value(request):
            """Set the value and returns *True* or *False*."""

            key = request.matchdict['value']
            try:
                _VALUES[key] = request.json_body
            except ValueError:
                return False
            return True


    # Create a service to serve our OpenAPI spec
    swagger = Service(name='OpenAPI',
                      path='/__api__',
                      description="OpenAPI documentation")


    @swagger.get()
    def openAPI_spec(request):
        my_generator = CorniceSwagger(get_services())
        my_spec = my_generator('MyAPI', '1.0.0')
        return my_spec


    # Setup and run our app
    def setup():
        config = Configurator()
        config.include("cornice")
        config.scan()
        app = config.make_wsgi_app()
        return app


    if __name__ == '__main__':
        app = setup()
        server = make_server('127.0.0.1', 8000, app)
        server.serve_forever()


And of course we should take a look at the resulting documentation. JSON may be a bit harsh
to read but with time you should get used to it. The resulting documentation can be
found at http://localhost:8000/__api__.

.. code-block:: json

    {
        "swagger": "2.0",
        "info": {
            "version": "1.0.0",
            "title": "MyAPI"
        },
        "basePath": "/",
        "tags": [
            {
                "name": "values"
            },
            {
                "name": "__api__"
            }
        ]
        "paths": {
            "/values/{value}": {
                "parameters": [
                    {
                        "name": "value",
                        "in": "path",
                        "required": true,
                        "type": "string"
                    }
                ],
                "get": {
                    "summary": "Returns the value.",
                    "responses": {
                        "default": {
                            "description": "UNDOCUMENTED RESPONSE"
                        }
                    },
                    "tags": [
                        "values"
                    ],
                    "produces": [
                        "application/json"
                    ]
                },
                "put": {
                    "tags": [
                        "values"
                    ],
                    "summary": "Set the value and returns *True* or *False*.",
                    "responses": {
                        "default": {
                            "description": "UNDOCUMENTED RESPONSE"
                        }
                    },
                    "parameters": [
                        {
                            "name": "PutBodySchema",
                            "in": "body",
                            "schema": {
                                "required": [
                                    "value"
                                ],
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "My precious value",
                                        "title": "Value"
                                    }
                                },
                                "title": "PutBodySchema"
                            },
                            "required": true
                        }
                    ],
                    "produces": [
                        "application/json"
                    ]
                }
            },
            "/__api__": {
                "get": {
                    "tags": [
                        "__api__"
                    ],
                    "responses": {
                        "default": {
                            "description": "UNDOCUMENTED RESPONSE"
                        }
                    },
                    "produces": [
                        "application/json"
                    ]
                }
            }
        }
    }


So see the difference? Now we get our properties extracted automatically since we
are now using a default schema validator defined with colander. Also, path parameters
are also extracted from the path description and content-types come from renderers.
This way we can extract much more information from useful code than with other approaches.

But you may ask, what about responses? Well, I'm working on it right now, and perhaps
I should stop writing at this moment and tell you when I'm finished.

See you :)

Edit: In case you want to see how I actually did it, please check
`the documentation for the package <https://cornices.github.io/cornice.ext.swagger>`_
I just wrote.
