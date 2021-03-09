from typing import Iterator, Union, Any, DefaultDict
from collections import defaultdict
from babelfish.babelfish.babelclient.babelclient import BabelClient
from babelfish.babelfish.babelio.babelfiler import BabelFiler
from itertools import chain


class BabelLangCode:
    LANG_REGISTRARY_URL: str = \
        "https://www.iana.org/assignments/language-subtag-registry/language" \
        "-subtag-registry"

    def __init__(self, lang_code_url: str = None, columns: dict = None):
        self.lang_columns = columns
        self.lang_code = lang_code_url

    @property
    def lang_code(self) -> str:
        return self._lang_code

    @lang_code.setter
    def lang_code(self, url: str = None):
        self._lang_code = url

    @property
    def lang_columns(self) -> dict:
        return self._lang_columns
    
    @lang_columns.setter
    def lang_columns(self, json_like_dict: dict = None) -> None:
        try:
            assert isinstance(json_like_dict, dict), "Input for columns " \
                                                     "must be a " \
                                                     "dictionary!"
        except AssertionError as error:
            print(error)
            self._lang_columns = None

        else:
            all_keys = (json_like_dict.get(i).keys() for i in json_like_dict)
            columns = list(set(chain.from_iterable(all_keys)))
            columns = sorted(columns)
            columns.insert(0, "Index")
            t_columns = tuple(columns)
            d_columns = dict.fromkeys(t_columns)
            self._lang_columns = d_columns

    def get_langcode_response(self) -> object:
        return BabelClient.api_get_response(url=self.lang_code)

    @staticmethod
    def parse_langcode_response(response) -> Iterator[str]:
        try:
            response.headers
        except AttributeError as error:
            print(error)
            return f"Cannot parse response."
        else:
            r_decoded = response.content.decode("utf8")
            r_gen = (
                i.strip("\n").strip().split("\n") for i in r_decoded.split(
                    "%%") if i
            )
            return r_gen

    @staticmethod
    def _str_parser(langcode_str: list) -> list:
        """
        Function makes an effort of ordering messy string [['k:v', 'k:v'..],
        ['k:v', 'k:v'] ...]
        to -> [index,{k:v}] for easier parsing.
        """
        tmp_list = list()
        for i, langcode_str in enumerate(langcode_str):
            for item in langcode_str:
                if item.split(":", 1).count("") < 1:
                    a, *b = item.split(":", 1)
                    if b:
                        b = "".join(b)
                    if not b:
                        b = a
                        a = "Comments"

                    # Special case line with : between sentences.
                    if "phonemes" in a:
                        special_case = [a, b]
                        a = "Comments"
                        b = "".join(special_case)
                    tmp_list.append([i, {a.strip(): b.strip()}])
        return tmp_list

    @staticmethod
    def _str_to_jsonlike(lang_codes_parsed):
        """Takes list formatted [index, {k:v, k1:v1 ..}] and converts it
        to {index : {k:v}}, easier to parse to json-object.
        """
        d_json = defaultdict(dict)
        for i, item in lang_codes_parsed:
            for k, v in dict(item).items():
                if k in d_json[i]:
                    value = d_json[i].get(k)
                    d_json[i].update({k: f"{value} {v}"})
                else:
                    d_json[i].update({k: "".join(v)})
        return d_json

    @staticmethod
    def from_str_to_dict(language_codes: Iterator[str]) -> \
            Union[str, DefaultDict[Any, list]]:

        """Function parses response from LANG_REGISTRARY_URL to dictionary.
        """

        try:
            next(language_codes)

        except TypeError as error:
            print(error)
            return "Argument 'language_codes' must be an iterable/sequence"
        else:
            l_lang_codes = list(language_codes)
            l_codes = BabelLangCode._str_parser(l_lang_codes)
            lang_dict = BabelLangCode._str_to_jsonlike(l_codes)
            return lang_dict

    @staticmethod
    def make_json(ordered_dict: DefaultDict) -> str:
        return BabelFiler.create_json(ordered_dict=ordered_dict)

    @staticmethod
    def open_json(path_to_file: str, at_cwd: bool = False):
        return BabelFiler.read_json(filename=path_to_file, cwd=at_cwd)
