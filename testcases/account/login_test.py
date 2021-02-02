import pytest
from httprunner import HttpRunner, Config, Step, RunRequest, Parameters

from runway.testcase_file import TestCaseFile
from runway.api_helper import APIHelper


class Login(HttpRunner):

    testcase_file = TestCaseFile(__file__)
    csv_relative_path = testcase_file.relate_csv()
    helper = APIHelper()
    common_parameters = helper.get_common_global_request_parameters()

    @pytest.mark.parametrized(
        "param",
        Parameters(
            {
                "id-email-password": f"${{P({csv_relative_path})}}"
            }
        )
    )
    def test_start(self, param):
        super().test_start(param)

    config = (
        Config("Login - $id")
        .base_url("${get_cloud_service_url()}")
    )

    teststeps = [
        Step(
            RunRequest("login")

        )
    ]