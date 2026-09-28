class FSFToolError(Exception):
    """Base error reported to CLI users."""


class JavaParseError(FSFToolError):
    pass


class UnsupportedJavaError(FSFToolError):
    pass


class FSFValidationError(FSFToolError):
    pass


class ExpressionError(FSFToolError):
    pass

