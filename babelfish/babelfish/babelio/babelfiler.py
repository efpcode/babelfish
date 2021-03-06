from pathlib import Path
from distutils.util import strtobool
from typing import List, Any, Union, DefaultDict
from json import dump, load


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
    def babel_mkdir(dir_name: str = "default", parents=True,
                    exist_ok=False) -> object:

        if dir_name[dir_name.rfind("/"):].rfind(".") > 1:
            dir_name = dir_name[:dir_name.find(".")]

        babel_filename = BabelFiler.BABELHOME / dir_name
        return babel_filename.mkdir(parents=parents, exist_ok=exist_ok)

    @staticmethod
    def babel_mkfile(new_file: str = "untitled", suffix=".txt",
                     exist_ok=False) -> object:
        new_file = str(new_file)

        if new_file.count("."):
            new_file, *rm_string = new_file.rsplit(
                ".", maxsplit=new_file.count("."))

        file_name = "".join([new_file, suffix])

        babel_filename = BabelFiler.BABELHOME / file_name
        print(f"New file was created at: {babel_filename.parent}, filename: "
              f"{babel_filename.name}")

        return babel_filename.touch(exist_ok=exist_ok)

    @staticmethod
    def babel_fileopen(path_to_file: str = ""):
        path_object = Path(path_to_file)
        with path_object.open(mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                yield line

    @staticmethod
    def babel_write_to_file(mode, data, path_to_file: str = ""):
        path_object = Path(path_to_file)
        with path_object.open(mode=mode, encoding="utf-8") as f:
            for line in data:
                f.write(line)
            f.close()

    @staticmethod
    def create_json(ordered_dict: DefaultDict) -> str:
        """Methods takes a default dict converts it json file with
        indent of 4.
        """
        filename = Path.cwd() / "languages_codes.json"
        with open(filename, "w") as j_file:
            dump(ordered_dict, j_file, indent=4)
            j_file.close()
        return f"Json-object was created at {filename}"

    @staticmethod
    def read_json(filename: str = None, cwd: bool = False) -> Union[str, Any]:
        """Methods reads json file and returns dict object.
        json file is parsed with indent of 4.

        cwd : bool
            If cwd is set to 'True' filepath starts at current work directory.
            Default value is 'False'
        """
        if cwd:
            filename = Path.cwd() / filename
        filename = Path(filename)

        try:
            filename.open()

        except (IOError, FileExistsError, FileNotFoundError) as errors:
            print(errors)
            return f"Could not process {str(filename)}"
        else:
            with open(str(filename), 'r') as f:
                j_file = load(f)
                f.close()
                return j_file

    @staticmethod
    def view_filesystem(
            root_path: str = None, ignore: bool = True,
            ignore_list: list = None
    ) -> None:
        if root_path:
            root_path = Path(root_path)

        if not root_path:
            root_path = Path.cwd()
        if not ignore_list:
            ignore_list = ["__", ".pyc", ".DS_Store"]

        print(f"rootdir: * {root_path} *")
        for path in sorted(root_path.rglob("*")):
            symbol = "+"
            depth = len(path.relative_to(root_path).parts)
            if ignore:
                ignore = ignore_list
                sys_path = BabelFiler._filter_files(path_to_io=path.name,
                                                    pattern=ignore)
                if sys_path:

                    spacer = '   ' * depth
                    if path.is_dir():
                        spacer = f"\ndir:{'. . ' * depth}"
                        symbol = "#"
                    print(f"{spacer}{symbol} {path.name}")
            else:
                if path.is_dir():
                    spacer = f"\ndir>{depth * '   '}"
                    print(f"{spacer}# {path.name}")
                else:
                    spacer = ". . " * depth
                    print(f"{spacer}+ {path.name}")

    @staticmethod
    def _filter_files(path_to_io: str, pattern: list = None) -> bool:
        """
        Function take str and 'searches' for given pattern.
        """
        match_pattern = [True if path_to_io.count(i) else False for i in
                         pattern]

        if sum(match_pattern):
            return False
        else:
            return True

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
