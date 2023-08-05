"""Test setup for grokcore.chameleon.
"""
import re
import doctest
import unittest
import zope.interface
import zope.component
import grokcore.chameleon

from zope.traversing.interfaces import ITraversable
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.publisher.interfaces.browser import IBrowserRequest
from grokcore.chameleon.tests import FunctionalLayer
from zope.testing import renormalizing

FLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


@zope.interface.implementer(ITraversable, IAbsoluteURL)
class DummyResource(object):
    """ Dummy resource implementation. """

    def __init__(self, request, name=''):
        self.request = request
        self.name = name

    def traverse(self, name, furtherPath):
        name = '%s/%s' % (self.name, name)
        return DummyResource(self.request, name=name)

    def __str__(self):
        return 'dummy:%s' % self.name

def setUpStatic(test):
    # Register a dummy resource for static folder.
    zope.component.provideAdapter(
        factory=DummyResource,
        adapts=(IBrowserRequest,),
        provides=zope.interface.Interface,
        name='grokcore.chameleon.tests.cpt_fixture'
        )
    return


checker = renormalizing.RENormalizing([
    (re.compile(
        r"IOError: \[Errno 2\] No such file or directory: "),
        r'FileNotFoundError: [Errno 2] No such file or directory: ')
    ])


def test_suite():
    """Get a testsuite of all doctests.
    """
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        'README.txt',
        checker=checker,
        setUp=setUpStatic,
        package=grokcore.chameleon,
        globs=dict(
            getRootFolder=FunctionalLayer.getRootFolder,
            ),
        optionflags=FLAGS,
        )
    readme.layer = FunctionalLayer
    suite.addTest(readme)
    suite.addTest(
        doctest.DocTestSuite(
            'grokcore.chameleon.tests.templatefile',
            checker=checker,
            setUp=setUpStatic,
            optionflags=FLAGS,
            )
        )
    return suite
