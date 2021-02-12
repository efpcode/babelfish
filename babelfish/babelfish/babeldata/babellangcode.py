"""Todo list
* Need to find a better way to parse lang-registry response.
* Single entry looks like this:

    File-Date: 2020-12-18
    %%
    Type: language
    Subtag: aa
    Description: Afar
    Added: 2005-10-16
    %%

Can be fixed with a str.split('%') after r.content.decode("utf8") ->
'\nType: language\nSubtag: aa\nDescription: Afar\nAdded: 2005-10-16\n'
that can be fixed with: foo.strip('\n').split('\n') ->
['Type: language', 'Subtag: aa', 'Description: Afar', 'Added: 2005-10-16']
-> converted to dict -> json.

But this is not optimal.. and will cost a lot.
"""
from babelfish.babelfish.babelclient.babelclient import BabelClient

lang_codes = 'https://www.iana.org/assignments/language-subtag-registry' \
            '/language-subtag-registry'



class BabelLangCode:
    def __init__(self, lang_code_url: str = None):
        self.lang_code = lang_code_url

    @property
    def lang_code(self) -> str:
        return self._lang_code

    @lang_code.setter
    def lang_code(self, url: str =lang_codes):
        self._lang_code = url

    def get_langcode_reg(self) -> object:
        return BabelClient.api_get_response(url=self.lang_code)
