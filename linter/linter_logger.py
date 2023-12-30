class LinterLogger:
    def __init__(self, saving_path: str):
        self.saving_path = saving_path

    def log_new_header(self, filename: str) -> None:
        with open(self.saving_path, "a") as f:
            self.write_line(f, "-" * 30)
            self.write_line(f, filename)
            self.write_line(f, "-" * 30)

    def log_comment(self, index, comment: str) -> None:
        with open(self.saving_path, "a") as f:
            self.write_line(f, f"Line {index}: {comment}")

    def log_emptylines_eof(self, index: int,
                           actual: int, correct: int) -> None:
        self.log_comment(index,
                         f"Should have {correct} empty line(s) "
                         f"at the end of file, not {actual}")

    def log_emptylines_sub(self, index: int,
                           actual: int, correct: int) -> None:
        self.log_comment(index,
                         f"Should have {correct} empty line(s) "
                         f"between subroutines, not {actual}")

    def log_emptylines_max(self, index: int,
                           actual: int, limit: int) -> None:
        self.log_comment(index,
                         f"Too many empty lines in a row - "
                         f"{actual}, limit is {limit}")

    def log_naming_case(self, index: int,
                        name: str, case: str):
        self.log_comment(index,
                         f"Identifier '{name}' "
                         f"is not in {case}")

    def log_before_item(self, index: int,
                        item: str, actual: int, correct: int) -> None:
        self.log_comment(index,
                         f"Before '{item}' should be "
                         f"{correct} whitespace(s), not {actual}")

    def log_after_item(self, index: int,
                       item: str, actual: int, correct: int) -> None:
        self.log_comment(index,
                         f"After '{item}' should be "
                         f"{correct} whitespace(s), not {actual}")

    def write_line(self, f, line: str):
        f.write(line + "\n")
