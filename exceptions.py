class NotFoundError(Exception):
    def __init__(self, message="Not Found"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedError(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)
        