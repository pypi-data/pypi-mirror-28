import json
from logging import getLogger
from functools import reduce
from typing import Union, Dict, List

logger = getLogger('http_server.tools.config_loader')


class ConfigLoader:
    __active_configs = {}
    __config_locations = {}
    __main_config_key = 'main'
    __main_config_path = 'configs/server.json'

    @staticmethod
    def __find_element_in_dict_object(dict_object:dict, key_path:str):
        try:
            return reduce(lambda d, key: d[key], key_path.split('/'), dict_object)
        except KeyError:
            return None

    # @staticmethod
    # def __load_config(config_path, config_key, logging_enabled):

    @staticmethod
    def __load_main_config(main_config_path:str=None):
        logger.info("Loading main configuration")
        if (main_config_path):
            logger.debug("Overriding default config path: {configPath}".format(configPath=main_config_path))
            ConfigLoader.__main_config_path = main_config_path

        logger.debug("Config is used: {configPath}".format(configPath=ConfigLoader.__main_config_path))
        try:
            main_config_file = open(ConfigLoader.__main_config_path)
            main_config = json.load(main_config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            message = "Critical error. Cannot read configuration file. Exiting now."
            logger.critical(message, exc_info=True)
            exit(1)
        else:
            main_config_file.close()

        logger.debug(json.dumps(main_config, indent=4, sort_keys=True))
        ConfigLoader.__active_configs[ConfigLoader.__main_config_key] = main_config
        ConfigLoader.__config_locations[ConfigLoader.__main_config_key] = ConfigLoader.__main_config_path
        logger.debug("Main config loaded successfully")

    @staticmethod
    def __load_config(key, path) -> bool:
        try:
            logger.info("Loading configuration: '{key}' -> {path}".format(key=key, path=path))

            config_file = open(path)
            config = json.load(config_file)
            config_file.close()

            logger.debug(json.dumps(config, indent=4, sort_keys=True))
            ConfigLoader.__active_configs[key] = config
            ConfigLoader.__config_locations[key] = path
            logger.debug("Config '{key}' loaded successfully".format(key=key))
            return True

        except:
            logger.error('Error while loading configuration', exc_info=True)
            return False

    @staticmethod
    def reload_config(config_name:str) -> bool:
        if (config_name in ConfigLoader.__config_locations):
            old_config = ConfigLoader.__active_configs[config_name]
            if (not ConfigLoader.__load_config(config_name, ConfigLoader.__config_locations[config_name])):
                ConfigLoader.__active_configs[config_name] = old_config
                return False
            else:
                return True

        return False

    @staticmethod
    def reload_configs():
        for config_name in ConfigLoader.__active_configs:
            ConfigLoader.reload_config(config_name)

    @staticmethod
    def load_configs(main_config_path:str=None, config_paths:Union[None, List[str], Dict[str,str]]=None):
        ConfigLoader.__load_main_config(main_config_path)
        if (config_paths is None):
            pass
        elif (isinstance(config_paths, list)):
            config_dir = ConfigLoader.get_from_config('configDirectory')
            for _config_name in config_paths:
                ConfigLoader.__load_config(_config_name, config_dir + ConfigLoader.get_from_config(f'{_config_name}Config'))
        elif (isinstance(config_paths, dict)):
            for _config_name in config_paths:
                ConfigLoader.__load_config(_config_name, config_paths[_config_name])
        else:
            raise ValueError(f"config_paths argument: got: {type(config_paths)}; expected: either List[str], Dict[str,str] or None")


    @staticmethod
    def get_from_config(path: str, config_name: str='main'):
        if (config_name in ConfigLoader.__active_configs):
            return ConfigLoader.__find_element_in_dict_object(ConfigLoader.__active_configs[config_name], path)
        return None
