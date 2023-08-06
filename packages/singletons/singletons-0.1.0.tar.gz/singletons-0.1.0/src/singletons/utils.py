"""
Utility classes
"""
import sys
from typing import Any, MutableMapping
from unittest.mock import Mock


_greenthread_environment = None


class SharedModule:
    """
    Base class used to intercept attribute accesses to a module

    See https://mail.python.org/pipermail/python-ideas/2012-May/014969.html where Guido talks about this technique

    This allows for lazy loading and overriding in the case of ``setup_mock``

    Subclasses must set ``globals`` class attribute.

    Example usage (at the very bottom of a module to be made into a shared module)::

        class _Shared(SharedModule):
            globals = globals()
        sys.modules[__name__] = _Shared()
    """
    _mock: MutableMapping = None

    def setup_mock(self):
        """
        Switches the module to ``mock`` mode, or resets all existing Mocks. All attribute accesses will receive mock
        objects instead of actual ones
        """
        self._mock = {}

    def __getattr__(self, item: str) -> Any:
        if self._mock is None:
            try:
                return self.globals[item]
            except KeyError:
                raise AttributeError(f"module '{self.globals['__name__']}' has no attribute '{item}'")
        if item not in self._mock:
            self._mock[item] = Mock()
        return self._mock[item]

    def __setattr__(self, key: str, value: Any) -> None:
        self._mock[key] = value


def _detect_greenthread_environment() -> str:
    """
    Detect if eventlet or gevent are in use
    """
    if 'eventlet' in sys.modules:
        try:
            from eventlet.patcher import is_monkey_patched as is_eventlet
            import socket

            if is_eventlet(socket):
                return 'eventlet'
        except ImportError:
            pass

    if 'gevent' in sys.modules:
        try:
            from gevent import socket as _gsocket
            import socket

            if socket.socket is _gsocket.socket:
                return 'gevent'
        except ImportError:
            pass

    return 'default'


def detect_greenthread_environment() -> str:
    """
    Detect the current environment: eventlet, or gevent, or '' for default
    """
    global _greenthread_environment
    if _greenthread_environment is None:
        _greenthread_environment = _detect_greenthread_environment()
    return _greenthread_environment


def greenthread_ident() -> int:
    """
    Returns the identifier of the current greenthread environment
    """
    greenthread_environment = detect_greenthread_environment()
    if greenthread_environment == 'eventlet':
        import eventlet.corolocal  # pylint: disable=import-error
        return eventlet.corolocal.get_ident()
    if greenthread_environment == 'gevent':
        import gevent.thread  # pylint: disable=import-error
        return gevent.thread.get_ident()
    raise RuntimeError('No greenthread environment detected')
