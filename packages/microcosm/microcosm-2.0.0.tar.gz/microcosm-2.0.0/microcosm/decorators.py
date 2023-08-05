"""
Factory decorators

"""
from microcosm.registry import _registry


DEFAULTS = "_defaults"


def binding(key, registry=None):
    """
    Creates a decorator that binds a factory function to a key.

    :param key: the binding key
    :param: registry: the registry to bind to; defaults to the global registry

    """
    if registry is None:
        registry = _registry

    def decorator(func):
        registry.bind(key, func)
        return func
    return decorator


def defaults(**kwargs):
    """
    Creates a decorator that saves the provided kwargs as defaults for a factory function.

    """
    def decorator(func):
        setattr(func, DEFAULTS, kwargs)
        return func
    return decorator


def get_defaults(func):
    """
    Retrieve the defaults for a factory function.

    """
    return getattr(func, DEFAULTS, {})
