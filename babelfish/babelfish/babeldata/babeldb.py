from sqlite3 import connect, OperationalError, ProgrammingError
from sqlite3 import Connection, Cursor
from pathlib import Path
from typing import List, Generator, Tuple, Any, Union, Pattern
from ..babelio.babelfiler import BabelFiler
from distutils.util import strtobool
from random import choices, randint
from string import ascii_letters
from collections import defaultdict
from re import compile
from ..babeldata.babellangcode import BabelLangCode
"""
TODO Lists
* Create table method
* Create update method
* Create insert method
* Think about SQL Injection attacks do not use string concat for SQL commands!
* Hash passwords with salt use 'secretes' module and hashlib. 
"""


class BabelDB:
    """General db object methods"""

    def __init__(self, db_name: str = None, db_connect: bool = True,
                 ) -> None:
        self.db_name = db_name
        self.db_connect = db_connect

    def __repr__(self):
        return f"BabelDB('test', True)"

    def __str__(self):
        return f"class BabelDB.Methods([GET, POST, DELETE, UPDATE]) Local " \
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

            except OperationalError as error:
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

    @property
    def db_connect(self) -> Union[bool, Connection]:
        return self._db_connect

    @db_connect.setter
    def db_connect(self, db_bool):
        if db_bool:
            conn = connect(self.db_name)
            cursor = conn.cursor()

            try:
                self._create_userdata_table()
                cursor.execute("SELECT * FROM user_data")
                cursor.fetchone()

            except ProgrammingError as dbError:
                self._db_connect = False
                print(dbError)

            else:
                self._db_connect = conn
        else:
            self._db_connect = False

    def db_close(self) -> str:
        if self.db_connect:
            print("closing connection")
            self.db_connect.close()
            self.db_connect = False
            return "Connection to db closed."
        return "No db connection was found!"

    def _create_userdata_table(self):
        conn = connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS user_data
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, 
            email TEXT NOT NULL,
            data BLOB NOT NULL, 
            salt BLOB NOT NULL)'''
        )
        conn.commit()
        conn.close()

    def _create_langcode_table(self):
        conn = connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lang_codes 
        (lang_id INTEGER PRIMARY KEY NOT NULL,
        date DATE NOT NULL,
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
        conn.close()

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

    def db_insert_langcode_data(self, json_obj):
        values = self._json_to_tuples(json_obj=json_obj)
        conn = self.db_connect
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO lang_codes(
        lang_id, date, comments, deprecated,
        description, macrolanguage, preferred_value, prefix,
        scope, subtag, suppress_script, tag, type) VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
        conn.commit()
        return conn

    def db_userdata_insert(self, data: List[tuple] = None) -> object:
        conn = self.db_connect
        cursor = conn.cursor()
        put_data = data
        print(data)
        cursor.executemany(
            'INSERT INTO user_data(username, email, data, salt) VALUES ('
            ' ?, ?, ?, ?)',  put_data)
        conn.commit()
        return conn

    def db_get_userdata(self, col_row: Tuple[str, str]) -> Tuple[Any, Any]:
        """Method returns a single row from a column in user_data table.
        Parameters
        ----------
        col_row : (column header: str, row label: str)
        """

        conn = self.db_connect
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM user_data")
        pattern = compile(col_row[0])
        cond = self._get_column_labels(cursor, target=pattern)
        if not cond:
            return 'Column header was not found!', False

        cursor.execute(f"SELECT * FROM user_data WHERE {col_row[0]} = ?",
                       (col_row[1]))
        data = cursor.fetchall()
        return data, cursor

    def _get_column_labels(self, cursor: Cursor, target: Pattern[str] = None) \
            -> \
            list:
        if not target:
            return [i for i in map(lambda x: x[0], cursor.description) if i]
        else:
            pattern = compile(target)
            return [i for i in map(lambda x:x[0], cursor.description) if
                    pattern.fullmatch(i)]

    def pptable(self, column_width: int = 24) -> str:
        conn = self.db_connect
        col_w = column_width
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_data')
        headers = self._get_column_labels(cursor,)
        col_names = BabelDB.parse_table(table_data=headers,
                                        columnwidth=col_w, sep="#")
        cursor.execute('SELECT * FROM user_data')
        print(col_names)
        data = cursor.fetchall()
        for i, v in enumerate(data, start=1):
            row = BabelDB.parse_table(table_data=v, columnwidth=col_w)
            if i <= 5:
                print(row)
            else:
                break

        return "Done!"

    @staticmethod
    def mock_data():
        tmp_list = list()
        while True:
            sample = "".join(choices(ascii_letters, k=randint(1, 11)))
            tmp_list.append(sample)
            if len(tmp_list) == 4:
                break
        return tuple(tmp_list)

    @staticmethod
    def create_mockdata():
        user_data = list()
        for i in range(0, 11):
            sample = BabelDB.mock_data()
            user_data.append(sample)
        return user_data

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
            print("Setting default width factor to: 2 character\n")
            width_factor = 2
            word = f"{word}"
            yield f"{width_factor * ' '}{word}{width_factor * ' '}{sep}"

        else:
            yield f"{empty_space *' '}{word}{empty_space * ' '}{sep}"
