import os
import unittest
import xmlrunner
import HTMLTestRunner
import pathlib

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    if not os.path.exists("reports"):
        os.makedirs("reports")
    try:
        file = open("reports/index.html", 'r')
    except IOError:
        file = open("reports/index.html", 'w')
    file = open("reports/index.html", 'wb')
    testRunner = HTMLTestRunner.HTMLTestRunner(
        stream=file,
        title='My unit test',
        description='This demonstrates the report output by HTMLTestRunner.'
    )
    package_tests = test_loader.discover(
        start_dir="./", pattern='*_testing.py')

    testRunner.run(package_tests)
