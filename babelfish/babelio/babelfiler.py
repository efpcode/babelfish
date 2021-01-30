from pathlib import Path
from distutils.util import strtobool
from typing import List


class BabelFiler:
    """
    The BabelFiler class handles all IO functions from read & write to file.
    """
    def __str__(self):
        return "BabelFiler.staticmethods"

    def __repr__(self):
        return "BabelFiler.FileIOStaticMethods()"

    BABELHOME = Path.cwd()

    @staticmethod
    def babel_mkdir(dir_name: str ="default", parents=True,
                    exist_ok=False) -> object:

        if dir_name[dir_name.rfind("/"):].rfind(".") > 1:
            dir_name = dir_name[:dir_name.find(".")]

        babel_filename = BabelFiler.BABELHOME / dir_name
        return babel_filename.mkdir(parents=parents, exist_ok=exist_ok)

    @staticmethod
    def babel_mkfile(new_file: str = "untitled", suffix=".txt",
                     exist_ok=False) -> object:

        if not (str(new_file).count(".")):
            new_file = "".join([str(new_file), suffix])

        babel_filename = BabelFiler.BABELHOME / new_file

        return babel_filename.touch(exist_ok=exist_ok)


# Static Method
    @staticmethod
    def babel_fileopen(path_to_file:str =""):
        path_object = Path(path_to_file)
        with path_object.open(mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                yield line

    @staticmethod
    def babel_write_to_file(mode, data, path_to_file:str =""):
        path_object = Path(path_to_file)
        with path_object.open(mode=mode, encoding="utf-8") as f:
            for line in data:
                f.write(line)
            f.close()


    # Static methods.
    @staticmethod
    def interactive_writing():
        lines: List[str] = list()
        text = input("Press <ENTER>- key to exit interactive text mode or "
                     "enter text here:\n ")

        lines.append(text[:140])
        while True:
            count_chr = len(" ".join(lines))
            print(f"Characters in text: {count_chr}/140")
            try:
                choice = strtobool(input("Do you want enter more text? ["
                                   "Y/N]"))
            except ValueError as error:
                print(f"Valid inputs are yes, y, 1 or no, n, 0.\n\n**User "
                      f"input resulted in the following output:{error}\n\n**")
                continue
            if count_chr >= 140:
                print("Max number of character were met exit.")
                text_input = "".join(lines)
                return text_input[:140]

            elif choice:
                more_text = input()
                lines.append(more_text)
            else:
                return "\n".join(lines)

