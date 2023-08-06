import graphene

from . import mixins
from .decorators import token_auth
from .utils import get_payload

__all__ = [
    'JSONWebTokenMutation',
    'ObtainJSONWebToken',
    'Verify',
    'Refresh',
]


class JSONWebTokenMutation(mixins.ObtainJSONWebTokenMixin,
                           graphene.ClientIDMutation):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, input_fields=None, **options):
        super().__init_subclass_with_meta__(
            input_fields=cls.auth_fields(),
            **options)

    @classmethod
    @token_auth
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return cls.do_auth(info)


class ObtainJSONWebToken(mixins.DoAuthMixin, JSONWebTokenMutation):
    """Obtain JSON Web Token mutation"""


class JSONWebTokenMixin(object):

    class Input:
        token = graphene.String()


class Verify(JSONWebTokenMixin,
             mixins.VerifyMixin,
             graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, root, info, token, **kwargs):
        return cls(payload=get_payload(token))


class Refresh(JSONWebTokenMixin,
              mixins.RefreshMixin,
              graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.refresh(*args, **kwargs)
