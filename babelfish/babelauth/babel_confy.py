from pathlib import Path
from os import environ
from babelfish.babelfish.babelio import BabelFiler


# Global Variable

class BabelConfig:
    HOME = Path.home()

    @staticmethod
    def _babel_configurator(sub_dir: str ="", babel_env: str ="") -> object:
        babel_config = BabelFiler()
        if not (sub_dir and babel_env):
            sub_dir = str(BabelFiler.HOME / "babel_data/.babel_config/")
            babel_env = str(
                BabelFiler.HOME / "babel_data/.babel_config/babelenv.cfg"
            )

        try:
            babel_config.babel_mkfile(babel_env)

        except FileExistsError as error:
            text = f"\nConfiguration file already exists at " \
                   f"\n{error}"
            return text

        except FileNotFoundError:
            babel_config.babel_mkdir(sub_dir)
            babel_config.babel_mkfile(babel_env)
            return "Configuration was completed."

        else:
            return "Configuration files already exists."


class BabelCredentials:

    HOME = Path.home().joinpath("babel_data", ".babel_config", "babelenv.cfg")

    def __init__(self, data=dict(my_username=None, my_password=None)):

        self.keys = data

    def __repr__(self):
        return "BabelCredential({MY_USERNAME:username, " \
               "MY_PASSWORD:secrete_password})"

    def __str__(self):
        return "BabelCredential object has your username & password"

    def _io_exists__(self):
        return self.HOME.exists()

    def _template_parser(self, data: list):
        envars = list()
        for item in data:
            a, b, c = item.partition("=")
            tmp = a.strip("export").strip()
            key = "".join((a, b, self.keys.get(tmp.casefold()), "\n"))
            envars.append(key)
        return envars

    @property
    def keys(self):

        return dict(my_username=self.__babel_user,
                    my_password=self.__babel_skey)

    @keys.setter
    def keys(self, data_vals):
        usr_name, password = data_vals.values()
        while True:
            cond1, cond2 = isinstance(usr_name, str), isinstance(
                password, str)
            try:
                if not (cond1 and cond2):
                    raise TypeError(f"Expected usr_name:{type(usr_name)} and "
                                    f"password {type(password)} to be "
                                    f"string typed inputs.")
            except TypeError as error:
                print(error)
                usr_name = input("Enter a valid username: ")
                password = input("Enter your password: ")
                continue
            else:
                self.__babel_user = usr_name
                self.__babel_skey = password
                break

    def credential_setup(self, override=False):
        if BabelCredentials.HOME.stat().st_size == 0 or override:
            list(BabelCredentials._template())
            data = list(BabelFiler.babel_fileopen(self.HOME))
            keys = self._template_parser(data)
            BabelFiler.babel_write_to_file(mode="w", data=keys,
                                           path_to_file=self.HOME)
            for k, v in self.keys.items():
                environ[k.upper()] = v
            return "Credentials are done!"
        else:
            new_object = BabelCredentials.user_credentials()
            self.keys = new_object.keys
            return f"Previous data entry has been loaded"

    @classmethod
    def _template(cls):
        if not(cls._io_exists__(cls)):
            raise ValueError(f"File must exists to create template: "
                             f"{str(cls.HOME)}")
        value_pairs = {"MY_USERNAME": None, "MY_PASSWORD": None}
        api_file = cls.HOME

        if api_file.stat().st_size == 0:
            with api_file.open(mode="w", encoding="utf-8") as f:
                for key, value in value_pairs.items():
                    yield f.write(f"export {key}={value}\n")
        else:
            with api_file.open(mode="r", encoding="utf-8") as f:
                for line in f.readlines():
                    yield line

    @classmethod
    def user_credentials(cls):
        new_dict = dict()
        data = list(BabelFiler.babel_fileopen(cls.HOME))
        keys = [i.replace("\n", "").lstrip("export").strip()
                for i in data]
        for items in keys:
            k, v = items.split("=")
            new_dict.update({k: v})
            environ[k] = v

        keys_lower = {k.lower(): v for k, v in new_dict.items()}
        babel_object = cls(data=keys_lower)

        return babel_object
