import pytest
from httprunner import HttpRunner, Config, Step, RunRequest, Parameters

from runway.testcase_file import TestCaseFile
from runway.api_helper import APIHelper


class TestRegister(HttpRunner):

    testcase_file = TestCaseFile(__file__)
    csv_relative_path = testcase_file.relate_csv()
    helper = APIHelper()
    common_parameters = helper.get_common_global_request_parameters()

    @pytest.mark.parametrize(
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
        Config("Register VeSync account - $id")
        .base_url("${get_cloud_service_url()}")
    )

    teststeps = [
        Step(
            RunRequest("send register request")
            .post("/cloud/v1/user/register")
            .with_headers(**{"Content-Type": "application/json;charset=UTF-8"})
            .with_json({
                **common_parameters,
                "method": "register",
                "token": "",
                "accountID": "",
                "email": "$email",
                "password": "$password"
            })
            .validate()
            .assert_equal("status_code", 200)
        )
    ]


if __name__ == "__main__":
    TestRegister().test_start()
