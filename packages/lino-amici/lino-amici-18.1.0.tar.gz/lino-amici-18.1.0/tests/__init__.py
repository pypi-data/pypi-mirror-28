"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

SETUP_INFO = {}

# load SETUP_INFO:
fn = ROOTDIR.child('lino_amici', 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))

from lino.utils.pythontest import TestCase

class PackagesTests(TestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])

class SpecsTests(TestCase):
    
    def test_overview(self):
        self.run_simple_doctests('docs/specs/overview.rst')


