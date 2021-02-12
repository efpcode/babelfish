from sqlite3 import connect, OperationalError, ProgrammingError
from pathlib import Path
from typing import List, Generator
from ..babelio.babelfiler import BabelFiler
from distutils.util import strtobool
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
        return f"BabelDB.dbMethods()"

    def __str__(self):
        return f"BabelDB.func([GET,POST,DELETE])"

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
    def db_connect(self):
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

    def db_close(self):
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
            password BLOB NOT NULL, 
            salt BLOB NOT NULL)'''
        )
        conn.commit()
        conn.close()

    def db_userdata_insert(self, data: List[tuple] = None) -> object:
        conn = self.db_connect
        cursor = conn.cursor()
        put_data = data
        cursor.executemany(
            'INSERT INTO user_data(username, email, password, salt) VALUES ('
            '?, '
            '?, '
            '?, '
            '?)',
            put_data
        )
        conn.commit()
        return conn

    def pptable(self, column_width: int = 24) -> str:
        conn = self.db_connect
        col_w = column_width
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_data')
        headers = [i[0] for i in cursor.description]
        col_names = BabelDB.parse_table(lines=headers, columnwidth=col_w)
        cursor.execute('SELECT * FROM user_data')
        print("".join(col_names))
        for i in cursor.fetchall():
            row = BabelDB.parse_table(i, columnwidth=col_w)
            print("".join(row))
        return "Done!"

    @staticmethod
    def parse_table(lines, columnwidth: int = 24, sep: str = "|") -> \
            Generator[str, None, None]:
        chr_space = [
            BabelDB._width_calculator(str(i), column_width=columnwidth) for
            i in lines
        ]
        yield "".join([f"{chr_space[i] * ' '}{v}{chr_space[i] * ' '}"
                       f"{sep}" for i, v in enumerate(lines)])

    @staticmethod
    def _width_calculator(
            word: str, column_width: int = 24, spacer: int = 2
    ) -> int:
        if len(word) % 2:
            word = "".join([word, " "])

        try:
            width_factor = int(
                (abs(column_width/2 - (len(word) + spacer)))*0.5
            )
            assert(width_factor >= 0)
        except AssertionError:
            print("Setting default width factor: 5 character\n")
            width_factor = 5
            return width_factor

        except TypeError as error:
            print("Could not complete calculation please make sure that "
                  "inputs are of the correct type [int, str, int] -> "
                  f"was set to width factor: 5 \n{error}: "
                  f"{column_width, word, spacer}")
            width_factor = 5
            return width_factor

        else:
            return width_factor
