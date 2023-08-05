class RecordNotFoundError(Exception):
    def __init__(self, wrapped_error):
        super().__init__()
        self.wrapped_error = wrapped_error
        self.message = str(self.wrapped_error)
