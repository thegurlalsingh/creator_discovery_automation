import threading

_stop_requested = False
_lock = threading.Lock()


def request_stop():
    global _stop_requested
    with _lock:
        _stop_requested = True


def reset_stop():
    global _stop_requested
    with _lock:
        _stop_requested = False


def is_stop_requested():
    global _stop_requested
    with _lock:
        return _stop_requested


class PipelineStoppedException(BaseException):
    pass


def check_stop():
    if is_stop_requested():
        raise PipelineStoppedException("Pipeline stopped by user request.")
