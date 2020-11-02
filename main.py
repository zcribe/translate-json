import json

import requests


def request_translation(translation_string, from_language, target_language, email):
    r = requests.get(
        f"https://api.mymemory.translated.net/get?q={translation_string}&langpair={from_language}|{target_language}&de={email}"
    )
    return json.loads(r.text)["responseData"]["translatedText"]


def read_in_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def translate_line(line, from_lang, to_lang, email):
    return request_translation(line, from_lang, to_lang, email)


def translate_dictionary(dict, from_lang, to_lang, email):
    local_dict = dict
    dict_items = local_dict.items()
    for key, value in dict_items:
        translated = translate_line(value, from_lang, to_lang, email)
        local_dict[key] = translated
    return local_dict


def write_out_json(dict, filename: str, target_lang):
    split_filename = filename.split(".")
    split_filename.insert(1, f"-translated-{target_lang}.")
    split_filename = "".join(split_filename)
    with open(split_filename, "w") as f:
        json.dump(dict, f)


def translate_file(filename: str, target_langs, from_lang, email):
    for lang in target_langs:
        print(f"Translating to: {lang}")
        dict = read_in_json(filename)
        translated_dict = translate_dictionary(dict, from_lang, lang, email)
        write_out_json(translated_dict, filename, lang)


def run():
    filename = "common.json"
    translate_file(
        filename, ["ru", "eng"], "et", "mail@mail.ee"
    )


if __name__ == "__main__":
    run()
