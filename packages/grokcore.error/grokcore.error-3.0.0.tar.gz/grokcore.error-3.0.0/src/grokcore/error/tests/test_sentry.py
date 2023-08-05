import unittest
import mock

from zope.publisher.browser import TestRequest

from grokcore.error.sentry import SentryAwareLoggingErrorReporting
from grokcore.error.zcml import errorreportingutility

import sys
if sys.version_info.major == 2:
    def bytes(arg, encoding):
        return str(arg)


class ZcmlTestCase(unittest.TestCase):

    def test_errorreportingutility(self):
        _context = mock.Mock()
        errorreportingutility(
            _context, factory=SentryAwareLoggingErrorReporting)
        _context.action.assert_called()

    def test_make_extra(self):
        request = TestRequest()
        reporter = SentryAwareLoggingErrorReporting()
        result = reporter.make_extra(request)
        expect = {'sentry.interfaces.Http': {
            'host': None,
            'headers': {'Host': '127.0.0.1'},
            'cookies': None,
            'env': {'CONTENT_LENGTH': '0',
                    'SERVER_URL': 'http://127.0.0.1',
                    'GATEWAY_INTERFACE': 'TestFooInterface/1.0'},
            'url': 'http://127.0.0.1',
            'data': bytes('', encoding='utf-8'),
            'method': 'GET',
            'query_string': None}}
        self.assertEqual(expect, result)

    def test_make_extra_principal(self):
        class MockPrincipal(object):
            id = 'foo'

        request = TestRequest()
        request.setPrincipal(MockPrincipal())
        reporter = SentryAwareLoggingErrorReporting()
        result = reporter.make_extra(request)
        self.assertTrue('sentry.interfaces.User' in result)
        self.assertEqual('foo', result['sentry.interfaces.User']['id'])

    def test_make_extra_request_none(self):
        reporter = SentryAwareLoggingErrorReporting()
        result = reporter.make_extra(None)
        self.assertEqual(result, None)

    def test_make_extra_request_no_httprequest(self):
        reporter = SentryAwareLoggingErrorReporting()
        result = reporter.make_extra(object())
        self.assertEqual(result, None)
