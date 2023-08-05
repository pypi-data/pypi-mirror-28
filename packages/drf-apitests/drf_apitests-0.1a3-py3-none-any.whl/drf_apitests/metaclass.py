import json
from collections import Mapping
from functools import partial
from pathlib import Path

from django.test import TestCase
from rest_framework import status


def log_to_output_file(test, response):
    dir = Path('_apitest_results') / test.parent.module / test.parent.filename
    dir.mkdir(parents=True, exist_ok=True)
    data = (None if response.status_code == 204 else response.json())
    with (dir / f"{test.slug}.json").open('wt') as fp:
        json.dump(dict(response=data, status=response.status_code),
                  fp, indent=4)


def make_test_func(test):
    """Build the unit test method for the given test case.

    :param test: Test case
    :type test: drf_apitests.apitest.APITestCase
    :return:
    """
    def test_func(self):
        request = getattr(self.client, test.method.lower())
        response = request(test.interpolated_url, data=test.params,
                           format='json')

        statements = list(test.assert_statements())
        if not statements:
            msg = f"Unexpected HTTP response ({response.status_code}): " \
                  f"{response.content}"
            success = (status.HTTP_200_OK, status.HTTP_201_CREATED,
                       status.HTTP_204_NO_CONTENT)
            self.assertIn(response.status_code, success, msg)

        for statement in test.assert_statements():
            statement.do_assertion(self,
                                   response=response,
                                   body=response.data,
                                   status=response.status_code)

        log_to_output_file(test, response)

    test_func.__name__ = test.slug
    test_func.__doc__ = test.method + ' ' + test.interpolated_url
    if 'testing' in test.skip:
        test_func.__unittest_skip__ = True
    return test_func


def make_test_class(document):
    """Build the unit test class for the given test document.

    :param document: Test document
    :type document: drf_apitests.apitest.APITestDocument
    :param base_url:
    :return:
    """
    from drf_apitests.client import CustomAPIClient

    class_attrs = {test.slug: make_test_func(test) for test in document.tests}
    class_attrs['name'] = document.name
    class_attrs['fixtures'] = document.fixtures
    class_attrs['client_class'] = partial(CustomAPIClient, auth=document.auth)
    klass = type(document.filename, (TestCase,), class_attrs)
    klass.__module__ = document.module
    if 'testing' in document.skip:
        klass.__unittest_skip__ = True
    return klass
