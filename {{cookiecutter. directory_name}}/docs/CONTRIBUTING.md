# Contributing

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to {{cookiecutter.kata_name}}.
These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it are governed by a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to contribute to {{cookiecutter.kata_name}}

To start to develop within this project open up the NOTES.md and note down what you're going to work on during the pompodoro. Follow the instructions below on starting the tests in watch mode. Follow the TDD rules of writing a failing test, then writing just enough code to get it to pass, and commit. If you can clarify the code without changing the functionality then refactor, keeping the tests passing.

### Test Driven Development

To get 100% test coverage we do test-driven development.

#### Unit tests

To start unit test-driven development run:

```bash
pipenv run watchTestUnit
```

#### API tests

For API testing we're using pact. There is the test_\*_consumer.py, along with the need for a pactflow account. When you're creating the repository using the cookiecutter, you should have had to have set up your pactflow account - [https://pactflow.io/try-for-free/](https://pactflow.io/try-for-free/). You only need to add tests to the consumer file. When you run the consumer tests it will generate a pact JSON file, and then when the provider is run it will spin up the app and verify the server passes the consumer tests.

To run the consumer tests in watch mode:

```sh
pipenv run watchTestApi
```

To run the provider tests:

```sh
make fake_ci
```

### Commit Guidelines

The project uses the commitizen tool for standardizing changelog style commit
messages so you should follow it as so:

```bash
git add .              # add files to staging
pipenv run commit      # use the wizard for the commit message
```

Alternatively, you can write your commit messages yourself in the following format:

```sh
type(scope?): subject  #scope is optional; multiple scopes are supported (current delimiter options: "/", "\" and ",")
```

Full details of Commitlint are available on (https://github.com/commitizen-tools/commitizen/blob/master/docs/tutorials/writing_commits.md)[https://github.com/commitizen-tools/commitizen/blob/master/docs/tutorials/writing_commits.md]

### Deploying the App

The app has a Dockerfile which can easily be built by running `docker compose build api`, and then to deploy it run `docker compose up api`. The app will be available on [http://localhost:9080/api-docs](http://localhost:9080/api-docs).