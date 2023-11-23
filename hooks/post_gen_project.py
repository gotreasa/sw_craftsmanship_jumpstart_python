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
        raise EnvironmentError(
            f"Command {command} failed with return code {completed_process.returncode}"
        )

def setup_github_action_secrets():
    print("ℹ️ Setup Github Action Secrets")
    os.system('gh secret set PACT_BROKER_TOKEN --body "{{cookiecutter._pact_broker_token}}"')
    os.system('gh secret set SNYK_TOKEN --body "{{cookiecutter._snyk_token}}"')
    os.system('gh secret set SONAR_TOKEN --body "{{cookiecutter._sonar_token}}"')
    print("👌 Completed setting up Github Action Secrets")

def setup_sonar():
    project_name="{{cookiecutter.github_username}}_{{cookiecutter.directory_name}}"
    project_organization="{{cookiecutter.sonar_org}}"
    project_key="{{cookiecutter.github_username}}_{{cookiecutter.directory_name}}"
    print("ℹ️ Setting up the sonar configuration")

    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization" : "Bearer {{cookiecutter._sonar_token}}"
        }

        payload = {
            "project": project_key,
            "organization": project_organization,
            "name": project_name,
            "newCodeDefinitionType": "previous_version",
            "newCodeDefinitionValue": "previous_version",
            "mainBranch": "main"
        }
        data = urllib.parse.urlencode(payload)
        data = data.encode('utf-8')
        request = urllib.request.Request("https://sonarcloud.io/api/projects/create", data, headers, method="POST")
        urllib.request.urlopen(request)

    except urllib.error.HTTPError as error:
            print("💥 There was an error", error)
            sys.exit(1)
    print("👌 Completed setting up the sonar configuration")

def write_tokens_to_env_file():
    print("ℹ️ Saving the tokens in the environment file")
    open_file = open(".env", "a")
    open_file.writelines([
        "PACT_BROKER_TOKEN={{cookiecutter._pact_broker_token}}\n",
        "SONAR_TOKEN={{cookiecutter._sonar_token}}\n", 
        "SNYK_TOKEN={{cookiecutter._snyk_token}}\n",])
    open_file.close()
    print("👌 Completed saving the environment file")

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
    run_command("pipenv run installHooks")

    print("😻 Git add remote...")
    run_command(
        f"git remote add origin git@github.com:{{cookiecutter.github_username}}/{kata_name}.git"
    )

    print("😻 Git branch main...")
    run_command("git branch -M main")

    setup_github_action_secrets()
    setup_sonar()
    write_tokens_to_env_file()

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

    def test_sonar_token_was_added_to_env_file(self):
        """🧪 Check that SONAR_TOKEN was added to the .env file"""
        
        with open(".env", "r") as file:
            string='SONAR_TOKEN={{cookiecutter._sonar_token}}\n'
            found=False
            for line_number, line in enumerate(file):  
                if string == line:
                    found=True
                    break
            self.assertTrue(found, "❗️ The .env was not updated with SONAR_TOKEN")

    def test_snyk_token_was_added_to_env_file(self):
        """🧪 Check that SNYK_TOKEN was added to the .env file"""
        
        with open(".env", "r") as file:
            string='SNYK_TOKEN={{cookiecutter._snyk_token}}\n'
            found_snyk_token=False
            for line_number, line in enumerate(file):  
                if string == line:
                    found_snyk_token=True
                    break
            self.assertTrue(found_snyk_token, "❗️ The .env was not updated with SNYK_TOKEN")

    def test_pact_broker_token_was_added_to_env_file(self):
        """🧪 Check that PACT_BROKER_TOKEN was added to the .env file"""
        
        with open(".env", "r") as file:
            string='PACT_BROKER_TOKEN={{cookiecutter._pact_broker_token}}\n'
            found=False
            for line_number, line in enumerate(file):  
                if string == line:
                    found=True
                    break
            self.assertTrue(found, "❗️ The .env was not updated with PACT_BROKER_TOKEN")

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

    def test_sonar_cloud_setup(self):
        """🧪 Check that the Sonar Cloud configuration is in place"""
        try:
            response = urllib.request.urlopen("https://sonarcloud.io/dashboard?id={{cookiecutter.sonar_org}}_{{cookiecutter.directory_name}}")
            self.assertEqual(response.getcode(), 
            200, 
            "❗️ Sonar Cloud is not set up correctly")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 
            200, 
            "❗️ There was aan error finding the Sonar project page")

    def test_github_secrets(self):
        """🧪 Check that Github secrets are correctly set"""

        items=['SNYK_TOKEN', 'SONAR_TOKEN', 'PACT_BROKER_TOKEN']
        is_found = {}
        for item in items:
            is_found[item] = False
        with subprocess.Popen('gh secret list', stdout=subprocess.PIPE, shell=True, universal_newlines=True) as process:
            for line in process.stdout:
                for item in items:
                    if item in line:
                        is_found[item]=True
                        break
            self.assertTrue(all(is_found.values()), "❗️ There is at least one secret is missing")

    def test_pre_commit_hooks_setup(self):
        """🧪 Asserting that Pre-Commit hooks are set up"""
        self.assertTrue(os.path.isfile('.git/hooks/commit-msg'), "❗️ commit-msg is missing")
        self.assertTrue(os.access('.git/hooks/commit-msg', os.X_OK), "❗️ commit-msg is not executable")
        self.assertTrue(os.path.isfile('.git/hooks/pre-commit'), "❗️ pre-commit is missing")
        self.assertTrue(os.access('.git/hooks/pre-commit', os.X_OK), "❗️ pre-commit is not executable")
        self.assertTrue(os.path.isfile('.git/hooks/pre-push'), "❗️ pre-push is missing")
        self.assertTrue(os.access('.git/hooks/pre-push', os.X_OK), "❗️ pre-push is not executable")

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
