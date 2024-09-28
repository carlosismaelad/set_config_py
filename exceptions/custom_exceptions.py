import datetime

class CustomExecption(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message       
    
    def __str__(self) -> str:
        return f"Exception: {self.message}"

        