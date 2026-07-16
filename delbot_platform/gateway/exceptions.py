from __future__ import annotations


class GatewayError(Exception):
    """
    Base exception for Gateway.
    """


class GatewayTimeout(GatewayError):
    """
    Runtime did not respond before timeout.
    """


class GatewayUnavailable(GatewayError):
    """
    Gateway cannot reach runtime.
    """


class ModelUnavailable(GatewayError):
    """
    Requested model is unavailable.
    """


class InferenceError(GatewayError):
    """
    Runtime returned an inference error.
    """