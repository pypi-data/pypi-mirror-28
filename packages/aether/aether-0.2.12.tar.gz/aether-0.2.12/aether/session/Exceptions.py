
class SkyError(Exception):
    """Base class from which all Exceptions on Sky derive. Useful for catching all errors regardless of type and case."""
    pass

class SkyValueError(SkyError, ValueError):
    """Raised if parameters passed into Sky are invalid or referred to an object or data that does not exist."""
    pass

class SkyRuntimeError(SkyError, RuntimeError):
    """Raised if Sky operation fails due to invalid state or server side error."""
    pass
