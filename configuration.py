import json
import os
from abc import ABC
from copy import deepcopy
from enum import Enum
from typing import Union, List

import yaml


class ConfigurationType(Enum):
    MEMORY = 'memory'
    JSON = 'json'
    YAML = 'yaml'
    SIMPLE = 'simple'


class ConfigurationSection(ABC):

    def get(self, key: str):
        pass

    def get_or_default(self, key: str, default):
        pass

    def set(self, key: str, value: Union[str, int, bool, float, List[Union[str, int, bool, float]]]) -> bool:
        pass

    def set_default(self, key: str, value: Union[str, int, bool, float, List[Union[str, int, bool, float]]]) -> bool:
        if not self.contains(key):
            self.set(key, value)
            return True
        return False

    def remove(self, key: str) -> bool:
        pass

    def contains(self, key: str) -> bool:
        pass

    def dict_copy(self) -> dict:
        pass


class MemoryConfigurationSection(ConfigurationSection):
    _separator: str
    _content: dict

    def __init__(self, content: Union[None, dict], separator: str = '*'):
        super().__init__(type)
        if content is None:
            content = dict()
        self._separator = separator
        self._content = content

    def get(self, key: str):
        return self.get_or_default(key, None)

    def get_or_default(self, key: str, default):
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return default
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return default
                    cache_dict = cache_dict[sub]
                else:
                    return default

            if last_key in cache_dict:
                value = cache_dict[last_key]
                if isinstance(value, dict):
                    return MemoryConfigurationSection(value, separator=self._separator)
                else:
                    return value
            else:
                return default
        else:
            if key in self._content:
                return self._content[key]
            else:
                return default

    def set_default(self, key: str, value: Union[
        str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if self.contains(key):
            return True
        else:
            return self.set(key, value)

    def set(self, key: str,
            value: Union[
                None, str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if value is None:
            return self.remove(key)
        if isinstance(value, ConfigurationSection):
            value = value.dict_copy()
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return False
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return False
                    cache_dict = cache_dict[sub]
                else:
                    new_dict = dict()
                    cache_dict[sub] = new_dict
                    cache_dict = new_dict
            cache_dict[last_key] = value
            return True
        else:
            self._content[key] = value
            return True

    def remove(self, key: str) -> bool:
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return False
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return False
                    cache_dict = cache_dict[sub]
                else:
                    return False
            if last_key in cache_dict:
                cache_dict.pop(last_key)
                return True
            else:
                return False
        else:
            if key in self._content:
                self._content.pop(key)
                return True
            else:
                return False

    def contains(self, key: str) -> bool:
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return False
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return False
                    cache_dict = cache_dict[sub]
                else:
                    return False
            if last_key in cache_dict:
                return True
            else:
                return False
        else:
            if key in self._content:
                return True
            else:
                return False

    def dict_copy(self) -> dict:
        pass


class Configuration(ABC):
    _type: ConfigurationType

    def __init__(self, type: ConfigurationType):
        self._type = type

    def get(self, key: str):
        pass

    def get_or_default(self, key: str, default):
        pass

    def set(self, key: str,
            value: Union[str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        pass

    def set_default(self, key: str, value: Union[
        str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if not self.contains(key):
            self.set(key, value)
            return True
        return False

    def remove(self, key: str) -> bool:
        pass

    def contains(self, key: str) -> bool:
        pass

    def save(self):
        pass

    def load(self):
        pass

    def dict_copy(self) -> dict:
        pass

    def get_type(self) -> ConfigurationType:
        return self._type

    def __str__(self):
        return self.dict_copy()


class MemoryConfiguration(Configuration, ABC):
    _separator: str
    _content: dict

    def __init__(self, content: Union[None, dict] = None, separator: str = '*',
                 type: ConfigurationType = ConfigurationType.MEMORY):
        super().__init__(type)
        if content is None:
            content = dict()
        self._separator = separator
        self._content = content

    def get(self, key: str):
        return self.get_or_default(key, None)

    def get_or_default(self, key: str, default):
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return default
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return default
                    cache_dict = cache_dict[sub]
                else:
                    return default
            if last_key in cache_dict:
                value = cache_dict[last_key]
                if isinstance(value, dict):
                    return MemoryConfigurationSection(value, separator=self._separator)
                else:
                    return value
            else:
                return default
        else:
            if key in self._content:
                return self._content[key]
            else:
                return default

    def set_default(self, key: str, value: Union[
        str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if self.contains(key):
            return True
        else:
            return self.set(key, value)

    def set(self, key: str,
            value: Union[
                None, str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if value is None:
            return self.remove(key)
        if isinstance(value, ConfigurationSection):
            value = value.dict_copy()
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return False
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return False
                    cache_dict = cache_dict[sub]
                else:
                    new_dict = dict()
                    cache_dict[sub] = new_dict
                    cache_dict = new_dict
            cache_dict[last_key] = value
            return True
        else:
            self._content[key] = value
            return True

    def remove(self, key: str) -> bool:
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return False
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return False
                    cache_dict = cache_dict[sub]
                else:
                    return False
            if last_key in cache_dict:
                cache_dict.pop(last_key)
                return True
            else:
                return False
        else:
            if key in self._content:
                self._content.pop(key)
                return True
            else:
                return False

    def contains(self, key: str) -> bool:
        key = key.lstrip(self._separator).lstrip(self._separator)
        if len(key) <= 0:
            return False
        if self._separator in key:
            split_str = key.split(self._separator, count(key, self._separator) - 1)
            cache_split_str_last_object = split_str[len(split_str) - 1]
            split_str[len(split_str) - 1] = cache_split_str_last_object.split(self._separator)[0]
            last_key = key.rsplit(self._separator, 1)[1]
            cache_dict = self._content
            for sub in split_str:
                if sub in cache_dict:
                    if not isinstance(cache_dict[sub], dict):
                        return False
                    cache_dict = cache_dict[sub]
                else:
                    return False
            if last_key in cache_dict:
                return True
            else:
                return False
        else:
            if key in self._content:
                return True
            else:
                return False

    def save(self):
        pass

    def load(self):
        pass

    def dict_copy(self) -> dict:
        return deepcopy(self._content)


class JsonConfiguration(MemoryConfiguration):
    """
    Don't use separator character in key, because this is a character to split!
    Default separator character: *
    """

    _file: str

    def __init__(self, file: str, separator: str = '*'):
        super().__init__(None, separator=separator, type=ConfigurationType.JSON)
        self._file = file
        self.load()

    def save(self):
        with open(self._file, 'w') as configuration_file:
            configuration_file.write(json.dumps(self._content))

    def load(self):
        self._content = dict()
        if os.path.exists(self._file) and os.path.isfile(self._file):
            with open(self._file, 'r') as configuration_file:
                self._content = json.loads(configuration_file.read())

    def dict_copy(self) -> dict:
        return deepcopy(self._content)


class YamlConfiguration(MemoryConfiguration):
    """
    Don't use the separator character in key, because this is a character to split!
    Default separator character: .

    How to use this? Check the bukkit api in Java! https://bukkit.fandom.com/wiki/Configuration_API_Reference
    """

    _file: str

    def __init__(self, file: str, separator: str = '.'):
        super().__init__(None, separator=separator, type=ConfigurationType.YAML)
        self._file = file
        self.load()

    def save(self):
        with open(self._file, 'w') as configuration_file:
            yaml.dump(self._content, configuration_file)

    def load(self):
        self._content = dict()
        if os.path.exists(self._file) and os.path.isfile(self._file):
            with open(self._file, 'r') as configuration_file:
                self._content = yaml.load(configuration_file)

    def dict_copy(self) -> dict:
        return deepcopy(self._content)


class SimpleConfiguration(Configuration):
    """
    Key cannot contains ' '
    But value can
    """

    _file: str
    _content: dict

    def __init__(self, file: str):
        super().__init__(ConfigurationType.SIMPLE)
        self._file = file
        self.load()

    def get(self, key: str):
        return self.get_or_default(key, None)

    def get_or_default(self, key: str, default):
        key = key.replace(' ', '')
        if key in self._content:
            return self._content[key]
        return default

    def set(self, key: str,
            value: Union[str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if value is None:
            return self.remove(key)
        self._content[key.replace(' ', '')] = value
        return True

    def set_default(self, key: str, value: Union[
        str, int, bool, float, List[Union[str, int, bool, float]], ConfigurationSection]) -> bool:
        if self.contains(key):
            return True
        else:
            return self.set(key, value)

    def remove(self, key: str) -> bool:
        return self._content.pop(key.replace(' ', ''))

    def contains(self, key: str) -> bool:
        return key.replace(' ', '') in self._content

    def save(self):
        string_content = ''
        for key in self._content.keys():
            string_content += str(key) + ' ' + str(self._content[key]) + '\n'
        with open(self._file, 'w') as configuration_file:
            configuration_file.write(string_content)

    def load(self):
        self._content = dict()
        if os.path.exists(self._file) and os.path.isfile(self._file):
            with open(self._file, 'r') as configuration_file:
                temp_dict = dict()
                string_content = configuration_file.read()
                for key_value in string_content.split('\n'):
                    if ' ' in key_value:
                        split_string = key_value.split(' ', 1)
                        if len(split_string[0]) > 0 and len(split_string[1]) > 0:
                            temp_dict[split_string[0]] = split_string[1]
                self._content = temp_dict

    def dict_copy(self) -> dict:
        return deepcopy(self._content)


def count(to_be_count: str, char: str) -> int:
    return int((len(to_be_count) - len(to_be_count.replace(char, ''))) / len(char))


def convert(config: Configuration, type: ConfigurationType) -> Configuration:
    ...
