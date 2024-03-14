class StepFunctionException(Exception):
    def __init__(self, status_code, message, detail_error=None):
        self.status_code = status_code
        self.message = message
        self.detail_error = detail_error
