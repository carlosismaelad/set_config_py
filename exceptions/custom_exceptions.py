import datetime

class CustomExecption(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
       
    
    def __str__(self) -> str:
        return f"Exception: {self.message}"
    
    def append_exception_on_log_tab(self, log_widget):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {self.message}"

        log_widget.append(log_message)
        