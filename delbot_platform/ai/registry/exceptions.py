class RegistryError(Exception):
    """Base registry exception."""


class ModelNotFoundError(RegistryError):
    """Requested model was not found."""


class InvalidModelConfiguration(RegistryError):
    """Invalid model configuration."""