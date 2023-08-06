from collections import UserList, UserDict, UserString

from enum import Enum


class SirenBase:
    pass


class UserInt(int):
    pass


class UserBool:
    def __init__(self, b):
        self.data = b


class UserFloat(float):
    pass


# TODO: get rid of this nonsense
def to_renderable(v):
    if not issubclass(v.__class__, RendererMixin):
        if type(v) == list:
            v = UserList(v)
        elif type(v) == dict:
            v = UserDict(v)
        elif type(v) == str:
            v = UserString(v)
        elif type(v) == int:
            v = UserInt(v)
        elif type(v) == float:
            v = UserFloat(v)
        elif type(v) == bool:
            v = UserBool(v)
        elif issubclass(v.__class__, Enum):
            v = UserString(v.value)
        try:
            v.__class__ = type('Renderable{}'.format(v.__class__.__name__), (v.__class__, RendererMixin), {})
        except Exception as e:
            print(v)
    return v


class RendererMixin:
    def render_list(self):
        return [to_renderable(v).render() for v in self if v is not None]

    def render_dict(self):
        return {k: to_renderable(v).render() for k, v in self.items() if v is not None}

    def render_siren_type(self):
        return {k[1:]: to_renderable(v).render() for k, v in self.__dict__.items() if v is not None}

    def render(self):
        if issubclass(self.__class__, SirenBase):
            return self.render_siren_type()
        elif isinstance(self, UserDict):
            return self.render_dict()
        elif isinstance(self, UserList):
            return self.render_list()
        elif hasattr(self, 'data'):
            return self.data

        return self

