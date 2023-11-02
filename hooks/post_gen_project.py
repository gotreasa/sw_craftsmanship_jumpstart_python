#!/usr/bin/env python
from cProfile import run
import os
import subprocess
import sys
import unittest
import urllib.request


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

kata_name = "{{ cookiecutter.directory_name }}"


def run_command(command):
    completed_process = subprocess.run(
        command, cwd=PROJECT_DIRECTORY, shell=True, check=True, timeout=360
    )
    if completed_process.returncode != 0:
        raise Exception(
            f"Command {command} failed with return code {completed_process.returncode}"
        )

def open_pycharm():
    print("👩🏻‍💻 time to code!")
    run_command("pycharm .")

if __name__ == "__main__":
    print("👷🏻 Creating virtual environment...")
    run_command("pipenv install --dev")

    print("🧪 running dry test cycle...")
    run_command("pipenv run tests")

    print("😻 git repo creation...")
    run_command(f"gh repo create {kata_name} --public")

    print("😻 Git initializing...")
    run_command("git init")

    print("🐍 Creating local quality gate with git hooks...")
    run_command("pipenv run install_pre_hooks")

    print("😻 Git add remote...")
    run_command(
        f"git remote add origin git@github.com:{{cookiecutter.github_username}}/{kata_name}.git"
    )

    print("😻 Git branch main...")
    run_command("git branch -M main")

    print("😻 git add all the items in the repo...")
    run_command("git add --all")

    print("😻 git commit the jumpstart...")
    run_command(f'git commit -m "feat: jumpstart {kata_name} with cookiecutter"')

    print("😻 git push the jumpstart...")
    run_command("git push -u origin main")
    
has_errors = False
class TestJumpstart(unittest.TestCase):
    def test_docs_exist(self):
        """🧪 Asserting that documentation files exist"""
        self.assertTrue(os.path.isfile('README.md'), "❗️ README.md is missing")
        self.assertTrue(os.path.isfile('docs/NOTES.md'), "❗️ NOTES.md is missing")
        self.assertTrue(os.path.isfile('LICENSE'), "❗️ LICENSE is missing")

    def test_pytest_configuration_exists(self):
        """🧪 Asserting that the pytest configuration is set up"""
        self.assertTrue(os.path.isfile('pytest.ini'), "❗️ The pytest.ini is missing")

    def test_pipfile_json_exists(self):
        """🧪 Asserting that the Pipfile is set up"""
        self.assertTrue(os.path.isfile('Pipfile'), "❗️ The Pipfile is missing")

    def test_pipfile_lock_json_exists(self):
        """🧪 Asserting that the Pipfile.lock is set up"""
        self.assertTrue(os.path.isfile('Pipfile.lock'), "❗️ The package install failed to produce a Pipfile.lock")

    def test_dummy_py_exists(self):
        """🧪 Asserting that the modules/dummy.py is set up"""
        self.assertTrue(os.path.isfile('modules/dummy.py'), "❗️ The source file is missing")

    def test_unit_test_exists(self):
        """🧪 Asserting that the tests/unit/test_0_installer_runner.py is set up"""
        self.assertTrue(os.path.isfile('tests/unit/test_0_installer_runner.py'), "❗️ The test file is missing")

    def test_repository_url_returns_ok(self):
        """🧪 Check that the Github repository is set up correctly"""
        try:
            response = urllib.request.urlopen("https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.directory_name}}/")
            self.assertEqual(response.getcode(), 
            200, 
            "❗️ The repository doesn't exist on github.com")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 
            200, 
            "❗️ There was an error finding the repository on Github")

    def test_dummy_file_is_available_on_the_repository(self):
        """🧪 Check that the dummy.py file is available on Github"""
        try:
            response = urllib.request.urlopen("https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.directory_name}}/blob/main/modules/dummy.py")
            self.assertEqual(response.getcode(), 
            200, 
            "❗️ The dummy.py file is not available on Github")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 
            200, 
            "❗️ There was an error finding the dummy.py file on Github")

    def test_git_config_exists(self):
        """🧪 Asserting that the git configuration files are correctly set up"""
        self.assertTrue(os.path.isfile('.git/config'), "❗️ The git configuration is missing")
        self.assertTrue(os.path.isfile('.gitignore'), "❗️ .gitignore configuration is missing")
    
    def test_git_origin_setup(self):
        """🧪 Asserting that git origin has been set up"""
        result=subprocess.run('git remote show', stdout=subprocess.PIPE, shell=True, check=True)
        self.assertIn("origin", str(result.stdout), "❗️ The Git origin is not set up")

    def tearDown(self):
        global has_errors
        if hasattr(self._outcome, 'errors'):
            # Python 3.4 - 3.10  (These two methods have no side effects)
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)
        else:
            # Python 3.11+
            result = self._outcome.result
        ok = all(test != self for test, text in result.errors + result.failures)
        if not ok:
            has_errors = True

    @classmethod
    def tearDownClass(cls):
        global has_errors
        if has_errors:
            print('🧹 Removing the GitHub repository due to the failure')
            os.system("gh repo delete github.com/{{cookiecutter.github_username}}/{{cookiecutter.directory_name}} --yes")
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization" : "Bearer {{cookiecutter._sonar_token}}"
            }
            payload = {
                "project": "{{cookiecutter.github_username}}_{{cookiecutter.directory_name}}",
            }
            data = urllib.parse.urlencode(payload)
            data = data.encode('utf-8')
            request = urllib.request.Request("https://sonarcloud.io/api/projects/delete", data, headers, method="POST")
            urllib.request.urlopen(request)
            
            print('❗️ Cookiecutter exited with a failure')
        else:
            open_pycharm()
            print('✅ Completed')
            print("👋🏿 bye bye! 🐍")

unittest.main(verbosity=2)
