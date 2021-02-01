"""Get global settings."""
import os


class Settings(object):

    def __init__(self):
        root_dir = os.path.dirname(__file__)
        """Set two global settings dictionary."""
        env_file = f"{root_dir}/.env"
        # envs contains all properties in file .env, use: envs["ENV_NAME"]
        self.envs = self.load_properties(env_file)

        property_file = ''
        test_env = self.envs["TEST_ENV"]
        if test_env == "ci":
            property_file = f"{root_dir}/resources/ci.properties"
        elif test_env == "testonline":
            property_file = f"{root_dir}/resources/testonline.properties"
        # properties contains all properties in file *.properties, use: properties["PROPERTY_NAME"]
        self.properties = self.load_properties(property_file)

    def load_properties(self, filepath, sep='=', comment_char='#'):
        """
        Read the file passed as parameter as a properties file.
        """
        props = {}
        with open(filepath, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
        return props