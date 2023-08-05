class KhipuError(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        Exception.__init__(self, message, error_code)
