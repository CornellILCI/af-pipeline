class ApiResponse:
    def __init__(self,
                 body=None,
                 is_success=False,
                 error=None):
        self.body = body
        self.is_success = is_success
        self.error = error
