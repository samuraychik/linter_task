class LinterLogger:
    def __init__(self, saving_path: str):
        self.saving_path = saving_path

    def log_new_header(self, filename: str) -> None:
        with open(self.saving_path, "a") as f:
            f.write("\n\n")
            f.write(filename)
            f.write("\n")

    def log_comment(self, comment: str) -> None:
        with open(self.saving_path, "a") as f:
            f.write(comment)
