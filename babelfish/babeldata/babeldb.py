from sqlite3 import connect, OperationalError, ProgrammingError
from sqlite3 import Connection, Cursor
from pathlib import Path
from typing import Generator, Tuple, Pattern, List
from ..babelio.babelfiler import BabelFiler
from distutils.util import strtobool
from collections import defaultdict
from re import compile
from ..babeldata.babellangcode import BabelLangCode
from collections import namedtuple


class BabelDB:
    """General db object methods"""

    def __init__(self, db_name: str = None, db_connect: object = None) -> None:
        self.db_name = db_name
        self.db_connect = db_connect
        if not self.db_name:
            self.db_name = "babeldb"

        if not self.db_connect:
            self.db_connect = ConnectDB(database=self.db_name)

    def __repr__(self):
        return f"BabelDB('test')"

    def __str__(self):
        return f"class BabelDB.Methods([GET]) from Local " \
               f"Database."

    @property
    def db_name(self):
        return self._dbname

    @db_name.setter
    def db_name(self, name):
        name, *junk = name.rsplit(".")
        del junk
        while True:
            t_name = f"{name}.db"

            try:
                connect(f"file:{Path(t_name).absolute()}?mode=rw", uri=True)

            except (OperationalError, ProgrammingError) as error:
                print(f"DB-file does not exist 'db_name' -> {error}")
                user_choice = strtobool(input(f"Do you wish to create db "
                                              f"with name: {t_name}?: Y/N"))
                if not user_choice:
                    name = input("Input absolute path or relative path "
                                 "local or remote database file here:\n")
                    if name == "exit":
                        self._dbname = None
                        break
                elif user_choice:
                    BabelFiler.babel_mkfile(new_file=name, suffix=".db")
                    print(f"File is created {name}")
                    self._dbname = f"{name}.db"
                    break

            else:
                print(f"db is loaded -> {name}.db")
                self._dbname = f"{name}.db"
                break

    def _create_langcode_table(self):
        conn = self.db_connect
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lang_codes 
        (lang_id INTEGER PRIMARY KEY NOT NULL,
        date_added DATE NOT NULL,
        comments VARCHAR(80),
        deprecated DATE,
        description TEXT,
        macrolanguage VARCHAR(80),
        preferred_value VARCHAR(40),
        prefix VARCHAR(20),
        scope VARCHAR(24),
        subtag VARCHAR(24),
        suppress_script VARCHAR(50),
        tag VARCHAR(40),
        type VARCHAR(60)         
        )''')
        conn.commit()

    def _json_to_tuples(self, json_obj: dict) -> list:
        values = list()
        langcode_obj = BabelLangCode()
        langcode_obj.lang_columns = json_obj
        d1 = langcode_obj.lang_columns.copy()
        json_obj = self._jsondata_filtered(json_obj=json_obj)

        for i, v in enumerate(json_obj):
            d1.update({"Index": i})
            d1.update(v)
            values.append(tuple(d1.values()))
            d1 = langcode_obj.lang_columns.copy()
        return values

    def _jsondata_filtered(self, json_obj: dict) -> Generator[dict, None,
                                                              None]:
        return (json_obj.get(i) for i in json_obj if json_obj[i]["Type"] ==
                "language")

    def load_langcode_data(self, json_obj):
        self._create_langcode_table()
        values = self._json_to_tuples(json_obj=json_obj)
        conn = self.db_connect
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO lang_codes(
        lang_id, date_added, comments, deprecated,
        description, macrolanguage, preferred_value, prefix,
        scope, subtag, suppress_script, tag, type) VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
        conn.commit()
        self._create_look_up()

    def _create_look_up(self):
        conn = self.db_connect
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE look_up as SELECT lang_id, description, subtag 
        FROM lang_codes
        """)
        conn.commit()

    def get_langcode(self, language: Tuple[str, str]):
        """
        Method returns language codes from local database. Data is fetched
        with or statement i.e.similar to this a=n or b=m.

        language : tuple(ISO standard country name: str, RFC3066-tag)

        """
        conn = self.db_connect
        cursor = conn.cursor()
        try:
            assert all(map(lambda x: isinstance(x, str), language)) is True, \
                "Input must be str!"
            assert len(language) == 2, "'language' input must be of length 2."
            if not language[0].isalpha():
                language = ("!", language[1])  # ! function as an esc-character

            cursor.execute("SELECT * FROM look_up WHERE description LIKE "
                           "? OR subtag=? LIMIT 20", ('%'+language[0]+'%',
                                                      language[1])
                           )
        except ProgrammingError as error:
            print(f"DB has been error triggered:\n{error}")
            return

        except AssertionError as error:
            print(error)

        else:
            found_in_db = cursor.fetchall()
            conn.commit()
            if not found_in_db:
                warning = UserWarning("DB found no matches.")
                print(warning)
                return None, None

            result = BabelDB.select_lang_code(found_in_db)
            return result

    def _get_column_labels(self, cursor: Cursor, target: Pattern[str] = None) \
            -> \
            list:
        if not target:
            return [i for i in map(lambda x: x[0], cursor.description) if i]
        else:
            pattern = compile(target)
            return [i for i in map(lambda x:x[0], cursor.description) if
                    pattern.fullmatch(i)]

    def pptable(self, column_width: int = 24, nr_rows: int = 5) -> str:
        conn = self.db_connect
        col_w = column_width
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lang_codes')
        headers = self._get_column_labels(cursor,)
        col_names = BabelDB.parse_table(table_data=headers,
                                        columnwidth=col_w, sep="#")
        cursor.execute('SELECT * FROM lang_codes')
        print(col_names)
        data = cursor.fetchall()
        for i, v in enumerate(data, start=1):
            row = BabelDB.parse_table(table_data=v, columnwidth=col_w)
            if i <= nr_rows:
                print(row)
            else:
                break

        return "Done!"

    @staticmethod
    def select_lang_code(db_values: List[tuple] = None):
        LangCode = namedtuple("LangCode", ["lang_id", "iso_standard_name",
                                           "subtag"], defaults=((None, ) * 3))
        user_selected = LangCode()
        option_dict = {}

        print(">>> Pick language by entering a digit (see below)")
        for i, v in enumerate(db_values, 1):
            option_dict.update({i: v})
            print(f"Option - {i}: {v}")
        while True:
            user_picked = input("Please enter a digit: ")
            try:
                user_picked = int(user_picked)
            except (ValueError, TypeError):
                print(f"An invalid entry was passed: {user_picked}")
                continue

            else:
                if option_dict.get(user_picked):
                    return user_selected._make(option_dict.get(user_picked))
                else:
                    print("Try Again!")

    @staticmethod
    def parse_table(table_data, columnwidth, sep: str = "|"):
        table = defaultdict(str)
        for i, rows in enumerate(table_data):
            cell = BabelDB._width_calculator(rows, column_width=columnwidth,
                                             sep=sep)
            table[i] = "".join([table[i], "".join(list(cell))])
        return "".join([table.get(k) for k in table.keys()])

    @staticmethod
    def _width_calculator(
            word: str, column_width: int = 24, spacer: int = 2, sep: str = "|"
    ) -> Generator[str, None, None]:

        word = str(word)

        if column_width <= len(word):
            word = word[(spacer*4*-1):]

        if len(word) % 2:
            word = "".join([word, " "])

        try:
            assert isinstance(word, str)
            empty_space = int(((column_width - (spacer * 2)) - len(word)) *
                              0.5)
            assert(empty_space >= 0)

        except (AssertionError, TypeError):
            width_factor = 2
            word = f"{word}"
            yield f"{width_factor * ' '}{word}{width_factor * ' '}{sep}"

        else:
            yield f"{empty_space *' '}{word}{empty_space * ' '}{sep}"


class ConnectDB(Connection):
    def __init__(self, database: str = None, is_db_connected: bool = True):
        super(ConnectDB, self).__init__(database=database)
        self.is_connected = is_db_connected
        self.database = database

    def __str__(self):
        return "ConnectDB(sqlite3.Connect)"

    def __repr__(self):
        return "demo_db = ConnectDb(database='demo_db.db')"

    @property
    def is_connected(self):
        return self._connection

    @is_connected.setter
    def is_connected(self, state):
        self._connection = state

    def close_connection(self):
        self.is_connected = False
        return super().close()
