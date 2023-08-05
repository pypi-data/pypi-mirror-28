import doctest
import grokcore.security
import re
import unittest
import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi

from pkg_resources import resource_listdir
from zope.testing import renormalizing
from zope.app.wsgi.testlayer import http


class Layer(
        zope.testbrowser.wsgi.TestBrowserLayer,
        zope.app.wsgi.testlayer.BrowserLayer):
    pass


layer = Layer(grokcore.security, allowTearDown=True)


checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])


def suiteFromPackage(name):
    layer_dir = 'functional'
    files = resource_listdir(__name__, '{}/{}'.format(layer_dir, name))
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        dottedname = 'grokcore.security.tests.%s.%s.%s' % (
            layer_dir, name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(
                getRootFolder=layer.getRootFolder,
                http=http,
                ),
            optionflags=(
                doctest.ELLIPSIS +
                doctest.NORMALIZE_WHITESPACE +
                doctest.REPORT_NDIFF +
                renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2))
        test.layer = layer
        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in [
            'role']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
