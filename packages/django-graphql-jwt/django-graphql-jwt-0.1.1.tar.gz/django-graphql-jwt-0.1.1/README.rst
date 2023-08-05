Django GraphQL JWT
==================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


JSON Web Token Authentication for `Django GraphQL`_

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


Include the JWT middleware in your `MIDDLEWARE` settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'graphql_jwt.middleware.JWTMiddleware',
        ...
    ]

Include the JWT backend in your `AUTHENTICATION_BACKENDS` settings:

.. code:: python

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JWTBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]


User Node
---------

Let's start by creating a simple `UserNode`.

.. code:: python

    from django.contrib.auth import get_user_model

    import graphene
    from graphene_django import DjangoObjectType
    from graphql_jwt.utils import jwt_encode, jwt_payload


    class UserNode(DjangoObjectType):
        token = graphene.String()

        class Meta:
            model = get_user_model()

        def resolve_token(self, info, **kwargs):
            if info.context.user != self:
                return None

            payload = jwt_payload(self)
            return jwt_encode(payload)


Login mutation
--------------

Create the `LogIn` mutation on your schema to authenticate the user.

.. code:: python

    from django.contrib.auth import authenticate, login

    import graphene


    class LogIn(graphene.Mutation):
        user = graphene.Field(UserNode)

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
            return cls(user=user)


Verify and refresh token
------------------------

Add mutations to your GraphQL schema.

.. code:: python

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()


    schema = graphene.Schema(mutations=Mutations)


``verifyToken`` to confirm that the JWT is valid.

.. code::

    mutation {
      verifyToken(token: "...") {
        payload
      }
    }


``refreshToken`` to obtain a brand new token with renewed expiration time for non-expired tokens.

.. code::

    mutation {
      refreshToken(token: "...") {
        data
      }
    }


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


JWT_AUTH_HEADER_PREFIX

::

    Authorization prefix
    Default: JWT

`JWT_ISSUER`_

::

    Identifies the principal that issued the JWT
    Default: None

`JWT_LEEWAY`_

::

    Validate an expiration time which is in the past but not very far
    Default: seconds=0

JWT_SECRET_KEY

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


.. _JWT_ALGORITHM: https://pyjwt.readthedocs.io/en/latest/algorithms.html
.. _JWT_AUDIENCE: http://pyjwt.readthedocs.io/en/latest/usage.html#audience-claim-aud
.. _JWT_ISSUER: http://pyjwt.readthedocs.io/en/latest/usage.html#issuer-claim-iss
.. _JWT_LEEWAY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=leeway#expiration-time-claim-exp
.. _JWT_VERIFY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify#reading-the-claimset-without-validation
.. _JWT_VERIFY_EXPIRATION: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify_exp#expiration-time-claim-exp


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Build Status| image:: https://travis-ci.org/flavors/graphql-jwt.svg?branch=master
   :target: https://travis-ci.org/flavors/graphql-jwt

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/graphql-jwt.svg
   :target: https://codecov.io/gh/flavors/graphql-jwt

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/7ca6c7ced3df021b7915/maintainability
   :target: https://codeclimate.com/github/flavors/graphql-jwt
