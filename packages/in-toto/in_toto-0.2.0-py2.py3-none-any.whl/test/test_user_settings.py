"""
<Program Name>
  test_user_settings.py

<Author>
  Lukas Puehringer <lukas.puehringer@nyu.edu>

<Started>
  Oct 26, 2017

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Test in_toto/user_settings.py

"""

import os
import sys
import unittest
import logging
import shutil
import tempfile
import in_toto.settings
import in_toto.user_settings

# Suppress all the user feedback that we print using a base logger
logging.getLogger().setLevel(logging.CRITICAL)

class TestUserSettings(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.working_dir = os.getcwd()

    # We use `rc_test` as test dir because it has an `.in_totorc`, which
    # is loaded (from CWD) in `user_settings.set_settings` related tests
    self.test_dir = os.path.join(os.path.dirname(__file__), "rc_test")
    os.chdir(self.test_dir)

    os.environ["IN_TOTO_ARTIFACT_EXCLUDE_PATTERNS"] = "e:n:v"
    os.environ["IN_TOTO_ARTIFACT_BASE_PATH"] = "e/n/v"
    os.environ["IN_TOTO_not_whitelisted"] = "parsed"
    os.environ["NOT_PARSED"] = "ignored"



  @classmethod
  def tearDownClass(self):
    os.chdir(self.working_dir)


  def test_get_rc(self):
    """ Test rcfile parsing in CWD. """
    rc_dict = in_toto.user_settings.get_rc()

    # Parsed (and split) and used by `set_settings` to monkeypatch settings
    self.assertListEqual(rc_dict["ARTIFACT_EXCLUDE_PATTERNS"], ["r", "c", "file"])

    # Parsed but ignored in `set_settings` (not in case sensitive whitelist)
    self.assertEquals(rc_dict["artifact_base_path"], "r/c/file")
    self.assertEquals(rc_dict["new_rc_setting"], "new rc setting")


  def test_get_env(self):
    """ Test environment variables parsing, prefix and colon splitting. """
    env_dict = in_toto.user_settings.get_env()

    # Parsed and used by `set_settings` to monkeypatch settings
    self.assertEquals(env_dict["ARTIFACT_BASE_PATH"], "e/n/v")

    # Parsed (and split) but overriden by rcfile setting in `set_settings`
    self.assertListEqual(env_dict["ARTIFACT_EXCLUDE_PATTERNS"],
        ["e", "n", "v"])

    # Parsed but ignored in `set_settings` (not in case sensitive whitelist)
    self.assertEquals(env_dict["not_whitelisted"], "parsed")

    # Not parsed because of missing prefix
    self.assertFalse("NOT_PARSED" in env_dict)


  def test_set_settings(self):
    """ Test precedence of rc over env and whitelisting. """
    in_toto.user_settings.set_settings()

    # From envvar IN_TOTO_ARTIFACT_BASE_PATH
    self.assertEquals(in_toto.settings.ARTIFACT_BASE_PATH, "e/n/v")

    # From RCfile setting (has precedence over envvar setting)
    self.assertListEqual(in_toto.settings.ARTIFACT_EXCLUDE_PATTERNS,
        ["r", "c", "file"])

    # Not whitelisted rcfile settings are ignored by `set_settings`
    self.assertTrue("new_rc_setting" in in_toto.user_settings.get_rc())
    self.assertRaises(AttributeError, getattr, in_toto.settings,
        "NEW_RC_SETTING")

    # Not whitelisted envvars are ignored by `set_settings`
    self.assertTrue("not_whitelisted" in in_toto.user_settings.get_env())
    self.assertRaises(AttributeError, getattr, in_toto.settings,
        "not_whitelisted")

if __name__ == "__main__":
  unittest.main()
