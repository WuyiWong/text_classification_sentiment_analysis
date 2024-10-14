from datetime import datetime


class ScriptBase:
    def info(self, message):
        self._print_info("INFO", message)

    def error(self, message):
        self._print_info("ERROR", message)

    def _print_info(self, info_type: str, message: str):
        print("[", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "][", info_type, "] ", message, sep="")
