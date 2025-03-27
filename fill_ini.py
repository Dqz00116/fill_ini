import re
import os
import json
from enum import Enum
import sys

SECTION_REGEX = r"\[(.*?)\]"
KEY_REGEX = r"\w+(?=\s*=)"
VALUE_REGEX = r"=(.*)"


def match_regex(input_str, regex_pattern):
    match = re.match(regex_pattern, input_str)
    return match.group() if match else None


def replace_word_by_regex(s1, s2, regex_pattern, preserve_first_char=False):
    try:
        s1, s2 = str(s1), str(s2)
        match = re.search(regex_pattern, s1)
        if match:
            msg = f"Replace {match.group()[1:]} --> {s2}"
            if preserve_first_char:
                s2 = str(match.group()[0]) + s2
            print(msg)
            return re.sub(regex_pattern, s2, s1)
        else:
            msg = f"Regex not match.\nstr1:{s1},str1:{s2}"
            raise ValueError(msg)
    except ValueError:
        raise


def create_enum_from_json(name, json_data):
    return Enum(name, json_data)


class Filler(object):

    Mode = None

    def __init__(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))

        enum_config_path = os.path.join(dir_path, 'enum_config.json')

        with open(
            enum_config_path,
            "r",
            encoding="utf-8",
        ) as enum_json:
            enum_dict = json.load(enum_json)
            Filler.Mode = create_enum_from_json("Mode", enum_dict["Mode"])

        config_path = os.path.join(dir_path, 'config.json')
        with open(
            config_path,
            "r",
            encoding="utf-8",
        ) as load_json:
            json_dict = json.load(load_json)
            self._engine_path = json_dict["Path"]
            self._fill_map = json_dict["Ini"]
            self._mode = Filler.Mode[json_dict["Mode"]]

    def fill_ini(self) -> None:
        def get_section_name(section) -> str:
            return str(section).replace("[", "").replace("]", "")

        for file_name, fill_info in self._fill_map.items():
            engine_path = os.path.normpath(self._engine_path)
            file_path = os.path.join(engine_path, "Config", f"{file_name}.ini")
            print(f"-----------Start to read ini file from ({file_path})-----------")

            with open(file_path, "r", encoding="utf-8") as file:
                context = ""
                cur_section_name = ""
                cur_key_set = set()

                for line in file:
                    section_match = match_regex(line, SECTION_REGEX)
                    if section_match is not None:
                        if len(cur_key_set) > 0:
                            msg = (
                                f"{cur_section_name} Not found all key. ini_value_dict:"
                                + ", ".join(str(element) for element in cur_key_set)
                            )
                            raise ValueError(msg)

                        section_name = get_section_name(section_match)
                        if section_name in fill_info.keys():
                            cur_section_name = section_name
                            cur_key_set = set(fill_info.get(cur_section_name).keys())
                            msg = f"Match section: {cur_section_name}"
                            print(msg)
                    else:
                        key = str(match_regex(line, KEY_REGEX))
                        if key is not None and key in cur_key_set:
                            print(f"Update key: {key} in section ({cur_section_name})")
                            value = fill_info[section_name][key]
                            replace_value = (
                                value[self._mode.name]
                                if isinstance(value, dict)
                                else value
                            )

                            line = replace_word_by_regex(
                                line, replace_value, VALUE_REGEX, True
                            )
                            cur_key_set.remove(key)

                    context += line

            print(f"-----------Start to write ini file to ({file_path})-----------")
            with open(file_path, "w+", encoding="utf-8") as file:
                file.write(context)


if __name__ == "__main__":
    filler = Filler()
    filler.fill_ini()
    print(f"Finished.")
    sys.exit(0)
