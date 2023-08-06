import json
from collections import Mapping
from functools import partial
from pathlib import Path

from django.db import connection
from django.db import reset_queries
from django.test import TestCase, override_settings
from rest_framework import status


def log_to_output_file(test, response, queries):
    dir = Path('_apitest_results') / test.parent.module / test.parent.filename
    dir.mkdir(parents=True, exist_ok=True)
    data = (None if response.status_code == 204 else response.json())
    with (dir / f"{test.slug}.json").open('wt') as fp:
        json.dump(dict(response=data, status=response.status_code,
                       queries=queries),
                  fp, indent=2, ensure_ascii=False)


def make_test_func(test):
    """Build the unit test method for the given test case.

    :param test: Test case
    :type test: drf_apitests.apitest.APITestCase
    :return:
    """

    @override_settings(DEBUG=True)
    def test_func(self):
        reset_queries()
        request = getattr(self.client, test.method.lower())
        response = request(test.interpolated_url, data=test.params,
                           format='json')
        test.perform_assertions(self, response)
        log_to_output_file(test, response, connection.queries)

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
