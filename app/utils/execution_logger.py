import os
from datetime import datetime


class ExecutionLogger:

    LOG_FILE = "execution_logs.txt"

    @classmethod
    def log(cls, agent_name, message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_message = (
            f"[{timestamp}] "
            f"[{agent_name}] "
            f"{message}\n"
        )

        with open(
            cls.LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(log_message)

    @classmethod
    def read_logs(cls):

        if not os.path.exists(cls.LOG_FILE):
            return ""

        with open(
            cls.LOG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    @classmethod
    def clear_logs(cls):

        with open(
            cls.LOG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("")