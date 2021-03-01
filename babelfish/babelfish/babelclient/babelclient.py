import os
from requests import request
from json import JSONDecoder as JsD
from json import JSONDecodeError
from sys import getsizeof


class BabelClient:
    def __str__(self):
        return "BabelClient2.APICaller"

    def __repr__(self):
        return "BabelClient.Response[GET]"

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
    def api_parse_query(
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
            usr, password = cls.get_env_data()
            token = os.environ.get("MY_APIKEY")
            langpair = f"{from_lang}|{to_lang}"
            return f"{stem}key={token}&q={query}&langpair={langpair}&user" \
                   f"={usr}"

    # static methods
    @staticmethod
    def get_env_data():
        return os.environ.get("MY_USERNAME"), os.environ.get("MY_PASSWORD")

    @staticmethod
    def parse_api_keygen():
        stem = "https://api.mymemory.translated.net/keygen?"
        web_auth = ("user=", "&pass=")
        user_data = BabelClient.get_env_data()
        login_data = ["".join(i) for i in list(zip(web_auth, user_data))]

        return "".join((stem, "".join(login_data)))

    @staticmethod
    def _str_to_bytes(text: str = None) -> int:
        return getsizeof(text.encode("utf-8", errors="replace"))



