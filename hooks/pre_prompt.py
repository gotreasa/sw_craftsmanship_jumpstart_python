# Standard Library
import unittest, os, urllib.request

class TestPrerequisites(unittest.TestCase):
    def test_gh_is_installed(self):
        """🧪 Asserting GitHub CLI is installed"""
        return_value=os.system('command -v gh')
        self.assertEqual(return_value, 0, "❗️ Github CLI (gh) needs to be installed")

    def test_gh_is_authenticated(self):
        """🧪 Asserting GitHub CLI is authenticated"""
        return_value=os.system('gh auth status')
        self.assertEqual(return_value, 0, "❗️ Github CLI (gh) needs to be authenticated")

    def test_git_is_installed(self):
        """🧪 Asserting Git CLI is installed"""
        return_value=os.system('command -v git')
        self.assertEqual(return_value, 0, "❗️ Git CLI (git) needs to be installed")

    def test_pycharm_is_installed(self):
        """🧪 Asserting PyCharm is added to the path"""
        return_value=os.system('command -v pycharm')
        self.assertEqual(return_value, 0, "❗️ pycharm needs to be added to the system path")

print('\n\n⌛️ Suite of prerequisite tests being run\n')
unittest.main(verbosity=2)
print('Completed prerequisite checks')
