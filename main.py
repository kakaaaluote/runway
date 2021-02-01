from shutil import copy, rmtree

import json
import os

from settings import Settings

TESTSUITES_PATH = "testsuites"
TESTCASES_PATH = "testcases"
TESTSUITE_JSON_PATH = "testsuites/suite_json"

setting_object = Settings()
envs = setting_object.envs
properties = setting_object.properties


def copy_testcase(src, testsuite_dir):
    """
    Copy testcase to testsuite directory, hierarchy of directory was kept.

    :param src: path of source testcase. The path should not contain "testcases/".
    :param testsuite_dir: path of testsuite.

    :return: None
    """
    src_testcase_dir = os.path.split(src)[0]
    dst_testcase_dir = f"{testsuite_dir}/{src_testcase_dir}"  # TODO: test
    os.makedirs(dst_testcase_dir)
    copy(f"testcases/{src}", dst_testcase_dir)


def collect_testcases():
    """
    Collect all testcases specified in testsuite (.json).

    1. Testsuite (.json) start with "SKIP" will be ignored.
    2. Create directory with the same name as testsuite under "testsuites" (remove if exists).
    3. Get all testcases path (relative to directory "testcases", path should not contain "testcases/").
    4. Copy testcases to testsuite directory, testcases hierarchy was kept.

    e.g.
        * testsuite.json: "testsuites/suite_json/core400s.json",
        * testcase: "testcases/account/register_test.py"

        1. In "testsuites/suite_json/core400s.json", testcase path is supposed to be "account/register_test.py".
        2. Create directory "core400s" under "testsuites/".
        3. Create directory "account" under "testsuites/core400s/".
        4. Copy "register_test.py" to "testsuites/core400s/".

    :return: None
    """
    assert os.path.exists(TESTSUITE_JSON_PATH), f"Directory {TESTSUITE_JSON_PATH} not exists."

    for testsuite_json in os.listdir(TESTSUITE_JSON_PATH):
        # file name starting with "SKIP" will be ignored.
        if not testsuite_json.startswith("SKIP"):
            # create directory to store testcases.
            testsuite_basename = os.path.splitext(testsuite_json)[0]
            testsuite_dir = f"{TESTSUITES_PATH}/{testsuite_basename}"
            # remove dir if already exists.
            if os.path.exists(testsuite_dir):
                rmtree(testsuite_dir)
            os.mkdir(testsuite_dir)

            with open(f"{TESTSUITE_JSON_PATH}/{testsuite_json}", encoding="utf-8") as f:
                testsuite = json.load(f)
            testcases = testsuite["testcases"].keys()

            for testcase in testcases:
                copy_testcase(testcase, testsuite_dir)


def collect_testcase_data(testcase, tails):
    """
    Collect test data for single testcase, used as data-driven test.

    1. The *header* contains two parts: id and parameters. e.g.: "id, email, password"
        * id: value corresponding to testcase in suite config, equal to "tail".
        * parameters: keys corresponding to testcase in parameter_prefix.json.
    2. Each line below the header contains the true data which would run a testcase instance.
       Query property file, the key is: prefix + id (tail).

    :param testcase: fullname relative to "testcases", e.g. "account/register_test.py"
    :param tails: a list of tail. e.g. ["core400s", "core400s.share"]
    :return: a list of test data. e.g. ['id,password,email', 'core400s,123456,2020090601@cloudtest.com']
    """
    testcase_data = []
    with open("resources/parameter_prefix.json", encoding="utf-8") as f:
        prefix_dict = json.load(f)
    testcase_prefix_dict = prefix_dict[testcase]
    header = ["id"] + list(testcase_prefix_dict.keys())
    testcase_data.append(",".join(str(x) for x in header))

    for tail in tails:
        line = [tail]
        for key_to_prefix in header[1:]:
            key = testcase_prefix_dict[key_to_prefix] + "." + tail
            value = properties[key]
            line.append(value)
        testcase_data.append(",".join(str(x) for x in line))

    return testcase_data


def collect_testsuite_data(testsuite):
    """
    Collect test data for specified test suite.

    Test data for testcases specified in test suite would be stored in csv file.
    The csv filename and path relative to environment variable TEST_DATA_DIR is same as source testcases.

    Note:
        Names of testcase python file in "suite_name.json" and "parameter_prefix.json" must be correct.

    :param testsuite: dirname relative to root directory, for instance, "testsuites/suite_json/core400s.json"
    :return: None
    """

    # remove test data directory if exists.
    test_data_dir = envs["TEST_DATA_DIR"]
    if os.path.exists(test_data_dir):
        rmtree(test_data_dir)  # rmtree("data/test_data_dir") will only delete directory "test_data_dir".
    os.mkdir(test_data_dir)

    # get all testcases in this testsuite.
    with open(testsuite, encoding="utf-8") as f:
        testsuite = json.load(f)
    testcases = testsuite["testcases"].keys()

    for testcase in testcases:
        tails = testsuite["testcases"][testcase]
        testcase_data = collect_testcase_data(testcase, tails)
        dirname = os.path.dirname(testcase)  # get "account" when "account/register_test.py"
        csv_file_dirname_relative_to_root = f"{test_data_dir}/{dirname}"
        if not os.path.exists(csv_file_dirname_relative_to_root):
            os.makedirs(csv_file_dirname_relative_to_root)

        csv_file_basename = os.path.splitext(os.path.basename(testcase))[0] + ".csv"
        csv_file_fullname = os.path.join(csv_file_dirname_relative_to_root, csv_file_basename)
        with open(csv_file_fullname, "w", encoding="utf-8") as f:
            f.writelines("\n".join(testcase_data))


if __name__ == "__main__":
    collect_testsuite_data("testsuites/suite_json/core400s.json")
