from PySide6.QtWidgets import QTextEdit

import datetime
def show_message(log_widget, log_message):
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {log_message}"
        
        if isinstance(log_widget, QTextEdit):
                log_widget.append(log_message)
        else:
                raise TypeError("log_widget deve ser uma instância de QTextEdit.")