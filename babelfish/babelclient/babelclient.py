import os
from requests import request
from json import JSONDecoder as JsD
from json import JSONDecodeError
from sys import getsizeof
from typing import Tuple


class BabelClient:

    DEMO_URL = "https://api.mymemory.translated.net/get?q=Hello%20World" \
               "!&langpair=en|it"

    def __str__(self):
        return "BabelClient.APICaller"

    def __repr__(self):
        return f"demo_api_response = BabelClient.api_get_response(url" \
               f"='{BabelClient.DEMO_URL}')"

    @classmethod
    def api_get_response(cls, url: str = None) -> object:
        j_object = JsD()
        response = request("GET", url=url)
        try:
            assert len(response.content) > 0, "Connection or other issue."
        except AssertionError as error:
            print(error)
            return False
        try:
            parse_response = {
                k: v for k, v in j_object.decode(response.text).items() if
                k in ("responseDetails", "translatedText", "responseStatus",
                      "key")
            }

        except JSONDecodeError:
            return response

        # Exit for api token
        if "key" in parse_response.keys():
            os.environ["MY_APIKEY"] = parse_response.get("key")
            return response

        try:
            assert (parse_response["responseStatus"] != "200")

        except AssertionError as error:
            print(f"User was not able to contact 'MyMemory' server"
                  f"\nError code returned from server: -->"
                  f" {parse_response['responseStatus']}\n"
                  f"Error code caused by: {parse_response['responseDetails']}"
                  f"\nAssertion criteria was not passed: {error}"
                  )
        else:
            return response

    @classmethod
    def api_set_query(
            cls, query: str = None, from_lang: str = None,
            to_lang: str = None
    ) -> object:
        """
        """
        try:
            assert (cls._str_to_bytes(query) <= 500)

        except AssertionError as error:
            error_msg = f"""The argument called 'query' exceeded the upper 
            limit of 500 bytes:\n{error}"""
            return error_msg

        else:
            stem = "https://api.mymemory.translated.net/get?"
            token = os.environ.get("MY_APIKEY")
            langpair = f"{from_lang}|{to_lang}"
            return f"{stem}key={token}&q={query}&langpair={langpair}"

    @staticmethod
    def parse_response(response: request) -> dict:
        translation = dict()
        read_json = JsD()
        max_match = {"match": 0}
        r_json = read_json.decode(response.content.decode("utf8",
                                                          "unicode_backslash"))
        try:
            assert int(r_json['responseStatus']) == 200, "Response was invalid"
        except AssertionError as error:
            print(error)
            return r_json
        else:

            machine_tr, human_tr = [r_json.get(i) for i in r_json.keys()
                                    if i in ['responseData', 'matches']]

            if machine_tr.get('translatedText'):
                translation.update({"machine_translation": machine_tr.get(
                                    "translatedText")})
                return translation
            else:
                for i in human_tr:
                    if i.get("match") > max_match.get("match"):
                        max_match = i
                translation.update({"human_translation": max_match.get(
                    'translation')})
                return translation

    # Static Methods

    @staticmethod
    def set_api_login() -> Tuple[str, str]:
        while True:
            try:
                os.environ["MY_USERNAME"], os.environ["MY_PASSWORD"]
            except KeyError as error:
                print(f"Environmental variables missing:{error}")
                print(f"Please enter your credentials for MyMemory API")
                api_username = input("Enter your username: ")
                api_password = input("Enter your password")
                os.environ["MY_USERNAME"] = api_username
                os.environ["MY_PASSWORD"] = api_password
                continue
            else:
                return os.environ.get("MY_USERNAME"), os.environ.get(
                    "MY_PASSWORD")

    @staticmethod
    def api_set_keygen():
        stem = "https://api.mymemory.translated.net/keygen?"
        web_auth = ("user=", "&pass=")
        user_data = BabelClient.set_api_login()
        login_data = ["".join(i) for i in list(zip(web_auth, user_data))]

        return "".join((stem, "".join(login_data)))

    @staticmethod
    def _str_to_bytes(text: str = None) -> int:
        return getsizeof(text.encode("utf-8", errors="replace"))
