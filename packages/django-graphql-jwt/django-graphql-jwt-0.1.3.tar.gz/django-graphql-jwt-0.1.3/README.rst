Django GraphQL JWT
==================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


`JSON Web Token`_ authentication for `Django GraphQL`_

.. _JSON Web Token: https://jwt.io/
.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-jwt


Include the JWT middleware in your *MIDDLEWARE* settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'graphql_jwt.middleware.JWTMiddleware',
        ...
    ]

Include the JWT backend in your *AUTHENTICATION_BACKENDS* settings:

.. code:: python

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JWTBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]


Login
-----

Create a *LogIn* mutation to authenticate the user.

.. code:: python

    from django.contrib.auth import authenticate, login

    import graphene
    from graphql_jwt.shortcuts import get_token


    class LogIn(graphene.Mutation):
        token = graphene.String()

        class Arguments:
            username = graphene.String()
            password = graphene.String()

        @classmethod
        def mutate(cls, root, info, username, password):
            user = authenticate(username=username, password=password)

            if user is None:
                raise Exception('Please enter a correct username and password')

            if not user.is_active:
                raise Exception('It seems your account has been disabled')

            login(info.context, user)
            return cls(token=get_token(user))


Add the *LogIn* mutation to your GraphQL schema.

.. code:: python

    import graphene


    class Mutations(graphene.ObjectType):
        login = LogIn.Field()


    schema = graphene.Schema(mutations=Mutations)


Verify and refresh token
------------------------

Add mutations to the root schema.

.. code:: python

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()


``verifyToken`` to confirm that the JWT is valid.

.. code::

    mutation VerifyToken($token: String!) {
      verifyToken(token: $token) {
        payload
      }
    }


``refreshToken`` to obtain a brand new token with renewed expiration time for non-expired tokens.

.. code::

    mutation RefreshToken($token: String!) {
      refreshToken(token: $token) {
        token
        payload
      }
    }


Relay
-----

Complete support for `Relay`_.

.. _Relay: https://facebook.github.io/relay/

.. code:: python

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.relay.Verify.Field()
        refresh_token = graphql_jwt.relay.Refresh.Field()


Environment variables
---------------------

`JWT_ALGORITHM`_

::

    Algorithm for cryptographic signing
    Default: HS256 

`JWT_AUDIENCE`_

::

    Identifies the recipients that the JWT is intended for
    Default: None

`JWT_ISSUER`_

::

    Identifies the principal that issued the JWT
    Default: None

`JWT_LEEWAY`_

::

    Validate an expiration time which is in the past but not very far
    Default: seconds=0

`JWT_SECRET_KEY`_

::

    The secret key used to sign the JWT
    Default: settings.SECRET_KEY

`JWT_VERIFY`_

::

    Secret key verification
    Default: True

`JWT_VERIFY_EXPIRATION`_

::

    Expiration time verification
    Default: False

JWT_EXPIRATION_DELTA

::

    Timedelta added to utcnow() to set the expiration time
    Default: minutes=5

JWT_ALLOW_REFRESH

::

    Enable token refresh
    Default: True

JWT_REFRESH_EXPIRATION_DELTA

::

    Limit on token refresh
    Default: days=7

JWT_AUTH_HEADER_PREFIX

::

    Authorization prefix
    Default: JWT


.. _JWT_ALGORITHM: https://pyjwt.readthedocs.io/en/latest/algorithms.html
.. _JWT_AUDIENCE: http://pyjwt.readthedocs.io/en/latest/usage.html#audience-claim-aud
.. _JWT_ISSUER: http://pyjwt.readthedocs.io/en/latest/usage.html#issuer-claim-iss
.. _JWT_LEEWAY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=leeway#expiration-time-claim-exp
.. _JWT_SECRET_KEY: http://pyjwt.readthedocs.io/en/latest/algorithms.html?highlight=secret+key#asymmetric-public-key-algorithms
.. _JWT_VERIFY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify#reading-the-claimset-without-validation
.. _JWT_VERIFY_EXPIRATION: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify_exp#expiration-time-claim-exp


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-jwt.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-jwt

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-jwt.svg
   :target: https://codecov.io/gh/flavors/django-graphql-jwt

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/7ca6c7ced3df021b7915/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-jwt
