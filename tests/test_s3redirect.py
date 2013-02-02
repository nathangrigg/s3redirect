#!/usr/bin/python

import unittest
import s3redirect as redirect
from mock import patch
from StringIO import StringIO

class TestRedirect(unittest.TestCase):
    def test_clean_key_remove_slash(self):
        expected = "key"
        actual = redirect.clean_key_name("/key")
        self.assertEqual(expected, actual)

    def test_clean_key_add_index(self):
        expected = "dir/index.html"
        actual = redirect.clean_key_name("dir/")
        self.assertEqual(expected, actual)

    def test_clean_key_options_off(self):
        expected = "/blah/"
        actual = redirect.clean_key_name("/blah/", remove_slash=False, index="")
        self.assertEqual(expected, actual)

    def test_parse_file_basic(self):
        expected = [("key/name", "/redirect/location")]
        f = StringIO("key/name /redirect/location")
        with patch("sys.stderr", new_callable=StringIO) as stderr:
            actual = list(redirect.redirect_pairs(f))
            self.assertEqual('', stderr.getvalue())
        self.assertEqual(expected, actual)

    def test_parse_file_ignore_comments_and_blanks(self):
        expected = [("key/name", "/redirect/location")]
        f = StringIO("\n\n#comment\n key/name /redirect/location \n#comment\n")
        with patch("sys.stderr", new_callable=StringIO) as stderr:
            actual = list(redirect.redirect_pairs(f))
            self.assertEqual('', stderr.getvalue())
        self.assertEqual(expected, actual)

    def test_parse_file_missing_redirect(self):
        expected = []
        f = StringIO("foo")
        with patch("sys.stderr", new_callable=StringIO) as stderr:
            actual = list(redirect.redirect_pairs(f))
            self.assertNotEqual('', stderr.getvalue())
        self.assertEqual(expected, actual)

    def test_parse_file_invalid_redirect(self):
        expected = []
        f = StringIO("foo ftp://bar")
        with patch("sys.stderr", new_callable=StringIO) as stderr:
            actual = list(redirect.redirect_pairs(f))
            self.assertNotEqual('', stderr.getvalue())
        self.assertEqual(expected, actual)

    def test_parse_file_extra_fields(self):
        expected = [("foo", "/bar")]
        f = StringIO("foo /bar baz")
        with patch("sys.stderr", new_callable=StringIO) as stderr:
            actual = list(redirect.redirect_pairs(f))
            self.assertNotEqual('', stderr.getvalue())
        self.assertEqual(expected, actual)

