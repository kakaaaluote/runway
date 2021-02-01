import time
import uuid

from loguru import logger

from settings import Settings

setting_object = Settings()
envs = setting_object.envs
properties = setting_object.properties


class APIHelper(object):
    """Class representing an api."""

    @staticmethod
    def get_new_trace_id(id_type="timestamp"):
        """Returns trace id based on id type."""
        if id_type == "timestamp":
            return time.time() * 1000
        elif id_type == "uuid":
            return uuid.uuid4().hex

    def get_common_global_request_parameters(self):
        """
        Returns part of common global request parameters.

        Including:
            traceId
            acceptLanguage
            appVersion
            phoneBrand
            phoneOS
            timeZone
            debugMode

        Not including:
            method
            token
            accountID

        :return: a dictionary of parameters
        """
        trace_id = self.get_new_trace_id()
        logger.debug(f"trace id: {trace_id}")
        parameters = {
            "traceId": f"{trace_id}",
            "acceptLanguage": properties["acceptLanguage"],
            "appVersion": properties["appVersion"],
            "phoneBrand": properties["phoneBrand"],
            "phoneOS": properties["phoneOS"],
            "timeZone": properties["timeZone"],
            "debugMode": properties["debugMode"]
        }
        logger.debug(f"common global parameters: {parameters}")
        return parameters

    @staticmethod
    def get_cloud_service_url():
        """Returns url of cloud service."""
        return properties["cloud.service.url"]
