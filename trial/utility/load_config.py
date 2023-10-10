import json
import os

# Calculate the absolute path to the config.json file based on the current script's location
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.json')

config_cache = {}  # Dictionary to store cached results

def load_config():
    MYSQL_HOST = os.environ.get('MYSQL_HOST')

    if 'config' not in config_cache:
        with open(config_file_path, 'r') as json_file:
            content = json_file.read()
            config_data = json.loads(content)

            if MYSQL_HOST is not None:
                config_data["database"]["host"] = MYSQL_HOST
            

        config_cache['config'] = config_data
    return config_cache['config']
