# Standard Library
import re, sys, unittest, os, urllib.request


MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

kata_name = "{{ cookiecutter.kata_name}}"

kata_dir = "{{ cookiecutter.directory_name }}"

if not re.match(MODULE_REGEX, kata_name):
    print(
        f"ERROR: The project directory ({kata_name}) is not a valid Python module name. Please do not use a - and use _ instead"
    )

    # Exit to cancel project
    sys.exit(1)


def assertNotEmpty(self, obj, message):
    self.assertTrue(obj, message)

class TestInputIsValid(unittest.TestCase):
    def test_cookiecutter_values_defined(self):
        cookie_parameters=[
            ["kata_name", "{{cookiecutter.kata_name}}"],
            ["directory_name", "{{cookiecutter.directory_name}}"],
            ["github_username", "{{cookiecutter.github_username}}"],
        ]
        for parameter in  cookie_parameters:
            with self.subTest(f"🧪 Check that {parameter[0]} is defined", parameter=parameter):
                f"""🧪 Check that {parameter[0]} is defined"""
                assertNotEmpty(self, parameter[1], f"❗️ The parameter {parameter[0]} does not have a value")

    def test_repository_url_returns_missing(self):
        """🧪 Check that the Github repository is not already set up"""
        try:
            response = urllib.request.urlopen("https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.kata_name}}.git")
            self.assertEqual(response.getcode(), 
            404, 
            "❗️ The repository already exists on github.com")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 
            404, 
            "❗️ There was an error connecting with Github")

print('\n\n⌛️ Suite of valid input tests being run\n')
unittest.main(verbosity=2)
print('Completed valid input checks')
