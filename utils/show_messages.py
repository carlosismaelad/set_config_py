from PySide6.QtWidgets import QTextEdit

import datetime
def show_message(log_widget, log_message):
        if log_widget is not None and not isinstance(log_widget, QTextEdit):
            print(f"log_widget: {log_widget}, type: {type(log_widget)}")
            raise TypeError("log_widget deve ser uma instância de SHOW MESSAGE.")
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {log_message}"
        
        if isinstance(log_widget, QTextEdit):
                log_widget.append(log_message)
        else:
                raise TypeError("log_widget deve ser uma instância de QTextEdit.")