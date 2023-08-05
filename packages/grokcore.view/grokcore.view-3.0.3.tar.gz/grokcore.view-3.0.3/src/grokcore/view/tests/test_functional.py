import doctest
import grokcore.view
import grokcore.view.testing
import os.path
import re
import unittest
import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi

from pkg_resources import resource_listdir
from zope.testing import renormalizing


class Layer(
        zope.testbrowser.wsgi.TestBrowserLayer,
        zope.app.wsgi.testlayer.BrowserLayer):
    pass


layer = Layer(grokcore.view, allowTearDown=True)


checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])


def suiteFromPackage(name):
    layer_dir = 'functional'
    files = resource_listdir(__name__, '{}/{}'.format(layer_dir, name))
    suite = unittest.TestSuite()
    getRootFolder = layer.getRootFolder
    globs = dict(
        bprint=grokcore.view.testing.bprint,
        getRootFolder=getRootFolder,
        http=zope.app.wsgi.testlayer.http,
        wsgi_app=layer.make_wsgi_app
        )
    optionflags = (
        renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2 +
        doctest.ELLIPSIS +
        doctest.NORMALIZE_WHITESPACE +
        doctest.REPORT_NDIFF
        )

    for filename in files:
        if filename == '__init__.py':
            continue

        test = None
        if filename.endswith('.py'):
            dottedname = 'grokcore.view.tests.%s.%s.%s' % (
                layer_dir, name, filename[:-3])
            test = doctest.DocTestSuite(
                dottedname,
                checker=checker,
                extraglobs=globs,
                optionflags=optionflags)
            test.layer = layer
        elif filename.endswith('.txt'):
            test = doctest.DocFileSuite(
                os.path.join(layer_dir, name, filename),
                optionflags=optionflags,
                globs=globs)
            test.layer = layer
        if test is not None:
            suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in [
            'contentprovider',
            'directoryresource',
            'static',
            'url',
            'view']:
        suite.addTest(suiteFromPackage(name))
    return suite
