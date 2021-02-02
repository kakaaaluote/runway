from httprunner import __version__
from runway.api_helper import APIHelper

api_helper = APIHelper()


def get_httprunner_version():
    return __version__


def get_cloud_service_url():
    return api_helper.get_cloud_service_url()
