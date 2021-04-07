class ApiResponse:
    def __init__(self,
                 http_status=None,
                 body=None,
                 error=None,
                 is_success=False):
        self.http_status = None
        self.body = body
        self.is_success = is_success
        self.error = error
