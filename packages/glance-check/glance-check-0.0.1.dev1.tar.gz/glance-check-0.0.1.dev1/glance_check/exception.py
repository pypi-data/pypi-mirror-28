class GlanceCheckException(Exception):
    pass


class GlanceCheckExceptionStatus(GlanceCheckException):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return repr(self.status)


class CheckConnectionError(GlanceCheckExceptionStatus):
    pass


class GetImageError(GlanceCheckExceptionStatus):
    pass


class CreateImageError(GlanceCheckExceptionStatus):
    pass


class DeleteImageError(GlanceCheckExceptionStatus):
    pass


class UpdateImageError(GlanceCheckExceptionStatus):
    pass


class TestImageNotFoundError(GlanceCheckException):
    pass


class TestImageAlreadyExistsError(GlanceCheckException):
    pass


class DeleteImageForbiddenError(GlanceCheckException):
    pass
