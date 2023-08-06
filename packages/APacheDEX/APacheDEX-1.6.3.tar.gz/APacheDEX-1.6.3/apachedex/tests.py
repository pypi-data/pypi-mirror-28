import unittest
import sys
from StringIO import StringIO
import apachedex


class MalformedInputTestCase(unittest.TestCase):
  def setUp(self):
    self._original_sys_argv = sys.argv
    self._original_sys_stdin = sys.stdin
    self._original_sys_stderr = sys.stderr
    self._original_sys_stdout = sys.stdout
    sys.stderr = StringIO()
    sys.stdout = StringIO()

  def tearDown(self):
    sys.argv = self._original_sys_argv
    sys.stdin = self._original_sys_stdin
    sys.stderr = self._original_sys_stderr
    sys.stdout = self._original_sys_stdout

  def test_timestamp_mixed_in_timestamp(self):
    sys.argv = ['apachedex', '--base=/', '-']
    sys.stdin = StringIO(
    # this first line is valid, but second is not
    '''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754
127.0.0.1 - - [14/Jul/2017:127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754''')
    apachedex.main()

    self.assertNotIn('Malformed line at -:1', sys.stderr.getvalue())
    self.assertIn('Malformed line at -:2', sys.stderr.getvalue())

