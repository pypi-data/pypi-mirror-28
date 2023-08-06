
"""
<Program Name>
  test_in_toto_sign.py
<Author>
  Sachit Malik <i.sachitmalik@gmail.com>
  Lukas Puehringer <luk.puehringer@gmail.com>
<Started>
  Wed Jun 21, 2017
<Copyright>
  See LICENSE for licensing information.
<Purpose>
  Test in_toto_sign command line tool.
"""

import os
import sys
import json
import shutil
import logging
import tempfile
import unittest

from mock import patch
from in_toto import log, exceptions
from in_toto.in_toto_sign import main as in_toto_sign_main

WORKING_DIR = os.getcwd()

# Suppress all the user feedback that we print using a base logger
logging.getLogger().setLevel(logging.CRITICAL)

class TestInTotoSignTool(unittest.TestCase):
  """Test in_toto_sign's main() - requires sys.argv patching; error logs/exits
  on Exception. """

  @classmethod
  def setUpClass(self):
    # Backup original cwd
    self.working_dir = os.getcwd()

    # Find demo files
    demo_files = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "demo_files")

    # Create and change into temporary directory
    self.test_dir = os.path.realpath(tempfile.mkdtemp())
    os.chdir(self.test_dir)

    # Copy demo files to temp dir
    for file_path in os.listdir(demo_files):
      shutil.copy(os.path.join(demo_files, file_path), self.test_dir)

    self.layout_path = "demo.layout.template"
    self.link_path = "package.2f89b927.link"
    self.alice_path = "alice"
    self.alice_pub_path = "alice.pub"
    self.bob_path= "bob"
    self.bob_pub_path = "bob.pub"
    self.carl_path= "carl"
    self.carl_pub_path = "carl.pub"

  @classmethod
  def tearDownClass(self):
    """Change back to initial working dir and remove temp dir. """
    os.chdir(self.working_dir)
    shutil.rmtree(self.test_dir)


  def _test_cli_sys_exit(self, cli_args, status):
    """Test helper to mock command line call and assert return value. """
    with patch.object(sys, "argv", ["in_toto_sign.py"]
        + cli_args), self.assertRaises(SystemExit) as raise_ctx:
      in_toto_sign_main()
    self.assertEqual(raise_ctx.exception.code, status)


  def test_sign_and_verify(self):
    """Test signing and verifying Layout and Link metadata with
    different combinations of arguments. """

    # Sign Layout with multiple keys and write to "tmp.layout"
    self._test_cli_sys_exit([
        "-f", self.layout_path,
        "-k", self.alice_path, self.bob_path,
        "-o", "tmp.layout",
        ], 0)

    # Verify "tmp.layout" (requires all keys)
    self._test_cli_sys_exit([
        "-f", "tmp.layout",
        "-k", self.alice_pub_path, self.bob_pub_path,
        "--verify",
        ], 0)

    # Sign Layout "tmp.layout", appending new signature, write to "tmp.layout"
    self._test_cli_sys_exit([
        "-f", "tmp.layout",
        "-k", self.carl_path,
        "-a"
        ], 0)

    # Verify "tmp.layout" (has three signatures now)
    self._test_cli_sys_exit([
        "-f", "tmp.layout",
        "-k", self.alice_pub_path, self.bob_pub_path, self.carl_pub_path,
        "--verify"
        ], 0)

    # Sign Link, replacing old signature,
    # and write to same file as input (verbosely)
    self._test_cli_sys_exit([
        "-f", self.link_path,
        "-k", self.bob_path,
        "-o", self.link_path,
        "-v"
        ], 0)

    # Verify Link
    self._test_cli_sys_exit([
        "-f", self.link_path,
        "-k", self.bob_pub_path,
        "--verify", "-v"
        ], 0)

    # Replace signature to Link and store to new file using passed
    # key's (alice) id as infix
    self._test_cli_sys_exit([
        "-f", self.link_path,
        "-k", self.alice_path
        ], 0)
    # Verify Link with alice's keyid as infix
    self._test_cli_sys_exit([
        "-f", "package.556caebd.link",
        "-k", self.alice_pub_path,
        "--verify"
        ], 0)

  def test_fail_signing(self):
    """Fail signing with an invalid key. """
    self._test_cli_sys_exit([
        "-f", self.layout_path,
        "-k", self.carl_path, self.link_path,
        ], 2)


  def test_fail_verification(self):
    """Fail signature verification. """
    # Fail with wrong key (not used for signing)
    self._test_cli_sys_exit([
        "-f", self.layout_path,
        "-k", self.carl_pub_path,
        "--verify"
        ], 1)

    # Fail with wrong key (not a valid pub key)
    self._test_cli_sys_exit([
        "-f", self.layout_path,
        "-k", self.carl_path,
        "--verify"
        ], 2)


  def test_bad_args(self):
    """Fail with wrong combination of arguments. """

    # Conflicting "verify" and signing options (--verify -o)
    self._test_cli_sys_exit([
        "-f", self.layout_path,
        "-k", "key-not-used",
        "--verify",
        "-o", "file-not-written"
        ], 2)

    # Conflicting "verify" and signing options (--verify -oa)
    self._test_cli_sys_exit([
        "-f", self.layout_path,
        "-k", "key-not-used",
        "--verify",
        "-a",
        ], 2)

    # Wrong "append" option for Link metadata
    self._test_cli_sys_exit([
        "-f", self.link_path,
        "-k", "key-not-used",
        "-a"
        ], 2)

    # Wrong multiple keys for Link metadata
    self._test_cli_sys_exit([
        "-f", self.link_path,
        "-k", self.alice_path, self.bob_path,
        ], 2)

  def test_bad_metadata(self):
    """Fail with wrong metadata. """

    # Not valid JSON
    self._test_cli_sys_exit([
        "-f", self.alice_pub_path,
        "-k", "key-not-used",
        ], 2)

    # Valid JSON but not valid Link or Layout
    open("tmp.json", "w").write(json.dumps({}))
    self._test_cli_sys_exit([
        "-f", "tmp.json",
        "-k", "key-not-used",
        ], 2)

if __name__ == "__main__":
  unittest.main(buffer=True)
