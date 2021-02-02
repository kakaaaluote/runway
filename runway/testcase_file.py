import os
import pathlib
from loguru import logger

from settings import Settings

setting_object = Settings()
envs = setting_object.envs
properties = setting_object.properties


class TestCaseFile(object):
    """Class representing a testcase python file."""

    def __init__(self, testcase_abspath):
        """
        Initiates an instance.
        :param testcase_abspath: absolute path of a testcase python file, which can obtained by __file__.
        """
        self.abs_path = testcase_abspath
        logger.debug(f"test case file abspath: {self.abs_path}")

    def get_testcase_relative_path(self):
        """Returns relative path to 'testcases/'. (not including 'testcases/')"""
        abs_path = pathlib.Path(self.abs_path).as_posix()
        dirname = os.path.dirname(abs_path)
        if dirname.endswith("testcases"):
            return ""
        return dirname.split("testcases/")[1]

    def relate_csv(self):
        """
        Returns csv file relative path to root directory where debugtalk.py was located.
        :return: csv file relative path
        """
        test_data_dir = envs["TEST_DATA_DIR"]
        dirname = self.get_testcase_relative_path()
        csv_filename = os.path.splitext(os.path.basename(self.abs_path))[0] + ".csv"
        csv_relative_path = os.path.join(test_data_dir, dirname, csv_filename)
        csv_relative_path = pathlib.Path(csv_relative_path).as_posix()
        logger.debug(f"csv file relative (root_dir) path: {csv_relative_path}")

        return csv_relative_path


if __name__ == "__main__":
    tf = TestCaseFile("d:/testrunner/testcases/register_test.py")
    p = tf.relate_csv()
    print(p)