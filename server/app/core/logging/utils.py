# -*- coding=utf-8 -*-
r"""

"""
import inspect
from structlog._frames import _find_first_app_frame_and_name


__all__ = ['add_module_info']


def add_module_info(_logger, _method_name, event_dict):
    frame, _ = _find_first_app_frame_and_name(additional_ignores=[
        "logging",
        __name__,
    ])
    if frame:
        frameinfo = inspect.getframeinfo(frame)
        module = inspect.getmodule(frame)
        if module:
            event_dict["module"] = module.__name__
            event_dict["lineno"] = frameinfo.lineno
    return event_dict
