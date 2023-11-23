# {{cookiecutter.kata_name}}

[![License: AGPL](https://img.shields.io/badge/License-AGPL-blue.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.directory_name}}/blob/main/LICENSE)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project={{cookiecutter.sonar_org}}_{{cookiecutter.directory_name}}&metric=alert_status)](https://sonarcloud.io/dashboard?id={{cookiecutter.sonar_org}}_{{cookiecutter.directory_name}})
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project={{cookiecutter.sonar_org}}_{{cookiecutter.directory_name}}&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id={{cookiecutter.sonar_org}}_{{cookiecutter.directory_name}})
[![Build Status](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.directory_name}}/actions/workflows/cicd.yml/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.directory_name}}/actions/workflows/cicd.yml)
[![Can I Deploy main to test](https://{{cookiecutter.pact_flow_username}}.pactflow.io/pacticipants/{{cookiecutter.directory_name}}_app/branches/main/latest-version/can-i-deploy/to-environment/test/badge)](https://{{cookiecutter.pact_flow_username}}.pactflow.io/hal-browser/browser.html#https://{{cookiecutter.pact_flow_username}}.pactflow.io/pacticipants/{{cookiecutter.directory_name}}_app/branches/main/latest-version/can-i-deploy/to-environment/test/badge)

Welcome to the Python Template created via a cookiecutter recipe. The project template is designed for a development via a `Double Loop approach` (BDD-TDD) using pytest and several other pytest libs.