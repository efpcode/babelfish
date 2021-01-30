from rm_not_useful import BabelFiler
from googletrans import Translator as GTranslator
from translate import Translator



# Todo list
# 1. Create child class to BabelFiler.
# 2. Create recipe function.
# 3. See if things can be refactor

# Inherent class
class BabelFish(BabelFiler):
    def __init__(self, src_file: str, output_file: str, trans_lang: str,
                 inter_mode: bool
                 ):
        self.inter_mode = inter_mode
        super().__init__(src_file, output_file, trans_lang)

    def translate(self):
        self.make_dir()
        self.make_file()
        babel = GTranslator()
        if self.inter_mode:
            text_input = self.interactive_writing()
            self.write_to_file(babel.translate(
                text_input, dest=self.trans_lang).text)

            return "Done!"
        else:
            f_lines = self.read_file(self.src_file)
            temp = "\n".join(f_lines)
            counter = 0
            while True:
                print("This many time run: ", counter+1)
                try:
                    text = babel.translate(
                        temp, dest=self.trans_lang).text
                except AttributeError:
                    babel = Translator(to_lang=self.trans_lang)
                    text = babel.translate("\n".join(temp))
                    self.write_to_file(text)


                else:
                    break

                finally:
                    return "Finished!"




