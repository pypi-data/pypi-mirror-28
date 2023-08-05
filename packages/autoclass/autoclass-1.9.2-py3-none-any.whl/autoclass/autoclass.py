from typing import Union, Tuple, Type, Any

from autoclass.autoargs import autoargs_decorate
from autoclass.autoprops import autoprops_decorate
from autoclass.autodict import autodict_decorate
from autoclass.utils_reflexion import get_constructor
from autoclass.utils_decoration import _create_class_decorator__robust_to_args
from autoclass.autohash import autohash_decorate


def autoclass(include: Union[str, Tuple[str]]=None, exclude: Union[str, Tuple[str]]=None,
              autoargs: bool=True, autoprops: bool=True, autodict: bool=True, autohash: bool=True):
    """
    A decorator to perform @autoargs, @autoprops and @autodict all at once with the same include/exclude list.

    :param include: a tuple of explicit attribute names to include (None means all)
    :param exclude: a tuple of explicit attribute names to exclude. In such case, include should be None.
    :param autoargs: a boolean to enable autoargs on the consturctor (default: True)
    :param autoprops: a boolean to enable autoargs on the consturctor (default: True)
    :param autodict: a boolean to enable autoargs on the consturctor (default: True)
    :param autohash: a boolean to enable autohash on the constructor (default: True)
    :return:
    """
    return _create_class_decorator__robust_to_args(autoclass_decorate, include, exclude=exclude, autoargs=autoargs,
                                                   autoprops=autoprops, autodict=autodict, autohash=autohash)


def autoclass_decorate(cls: Type[Any], include: Union[str, Tuple[str]] = None, exclude: Union[str, Tuple[str]] = None,
                       autoargs: bool=True, autoprops: bool=True, autodict: bool=True, autohash: bool=True) \
        -> Type[Any]:
    """

    :param cls: the class on which to execute. Note that it won't be wrapped.
    :param include: a tuple of explicit attributes to include (None means all)
    :param exclude: a tuple of explicit attribute names to exclude. In such case, include should be None.
    :param autoargs: a boolean to enable autoargs on the consturctor (default: True)
    :param autoprops: a boolean to enable autoprops on the consturctor (default: True)
    :param autodict: a boolean to enable autodict on the consturctor (default: True)
    :param autohash: a boolean to enable autohash on the constructor (default: True)
    :return:
    """

    # @autoargs
    if autoargs:
        init = get_constructor(cls)
        cls.__init__ = autoargs_decorate(init, include=include, exclude=exclude)

    # @autoprops
    if autoprops:
        autoprops_decorate(cls, include=include, exclude=exclude)

    # @autodict
    if autodict:
        autodict_decorate(cls, include=include, exclude=exclude)

    # @autohash
    if autohash:
        autohash_decorate(cls, include=include, exclude=exclude)

    return cls
