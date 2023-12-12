#!/usr/bin/env python
# Standard Libraries only
import unittest, os, stat

COOKIECUTTER_RC_PATH = os.path.expanduser('~') + '/.cookiecutterrc'

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

    def test_pipenv_is_installed(self):
        """🧪 Asserting pipenv is installed"""
        return_value=os.system('command -v pipenv')
        self.assertEqual(return_value, 0, "❗️ pipenv needs to be installed")

    def test_pycharm_is_installed(self):
        """🧪 Asserting PyCharm is added to the path"""
        return_value=os.system('command -v pycharm')
        self.assertEqual(return_value, 0, "❗️ pycharm needs to be added to the system path")
        
    def test_cookiecutterrc_setup(self):
        """🧪 Asserting that CookieCutter RC file is setup correctly"""
        self.assertTrue(os.path.isfile(COOKIECUTTER_RC_PATH), "❗️ ~/.cookiecutterrc is missing")
        st = os.stat(COOKIECUTTER_RC_PATH)
        self.assertTrue(bool(st.st_mode & stat.S_IRUSR), "❗️ ~/.cookiecutterrc does not have owner read permission. Permission needs to be set to 600.")
        self.assertTrue(bool(st.st_mode & stat.S_IWUSR), "❗️ ~/.cookiecutterrc does not have owner write permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IXUSR), "❗️ ~/.cookiecutterrc should not have owner execute permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IRGRP), "❗️ ~/.cookiecutterrc should not have group read permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IWGRP), "❗️ ~/.cookiecutterrc should not have group write permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IXGRP), "❗️ ~/.cookiecutterrc should not have group execute permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IROTH), "❗️ ~/.cookiecutterrc should not give others read permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IWOTH), "❗️ ~/.cookiecutterrc should not give others write permission. Permission needs to be set to 600.")
        self.assertFalse(bool(st.st_mode & stat.S_IXOTH), "❗️ ~/.cookiecutterrc should not give others execute permission. Permission needs to be set to 600.")
        private_tokens = [
            '"_pact_broker_token": "',
            '"_sonar_token": "',
            '"_snyk_token": "',
        ]
        
        for token in private_tokens:
            with open(COOKIECUTTER_RC_PATH, "r") as file:
                found=False
                for line_number, line in enumerate(file):  
                    if token in line:
                        found=True
                        break
                self.assertTrue(found, f'❗️ The ~/.cookiecutterrc was not updated with {token}..."')

print('\n\n⌛️ Suite of prerequisite tests being run\n')
unittest.main(verbosity=2)
print('Completed prerequisite checks')
