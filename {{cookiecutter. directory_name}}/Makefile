include .env
PACTICIPANT := "{{cookiecutter.directory_name}}_app"
PACT_BROKER_BASE_URL := https://{{cookiecutter.pact_flow_username}}.pactflow.io
PACT_CLI="docker run --network host --rm -v ${PWD}:${PWD} -e PACT_BROKER_BASE_URL -e PACT_BROKER_TOKEN -e PACT_BROKER_PUBLISH_VERIFICATION_RESULTS pactfoundation/pact-cli:latest"

# Only deploy from master
ifeq ($(GIT_BRANCH),master)
	DEPLOY_TARGET=deploy
else
	DEPLOY_TARGET=no_deploy
endif

all: test

## ====================
## CI tasks
## ====================

ci: test publish_pacts test_provider can_i_deploy $(DEPLOY_TARGET)

# Run the ci target from a developer machine with the environment variables
# set as if it was on GitHub Actions.
# Use this for quick feedback when playing around with your workflows.
fake_ci: .env
	CI=true \
	GIT_COMMIT=`git rev-parse --short HEAD`+`date +%s` \
	GIT_BRANCH=`git rev-parse --abbrev-ref HEAD` \
	PACT_BROKER_PUBLISH_VERIFICATION_RESULTS=true \
	PACT_BROKER_BASE_URL=$(value PACT_BROKER_BASE_URL) \
	PACT_BROKER_TOKEN=$(value PACT_BROKER_TOKEN) \
	make ci

publish_pacts: .env
	@"${PACT_CLI}" publish ${PWD}/pacts --consumer-app-version ${GIT_COMMIT} --branch ${GIT_BRANCH}

	## =====================
## Build/test tasks
## =====================

test:
	pipenv run ApiTests

test_provider: .env
		docker-compose up --abort-on-container-exit --exit-code-from pact_verifier
		docker-compose logs pact_verifier

## =====================
## Deploy tasks
## =====================

deploy: deploy_app record_deployment record_release

no_deploy:
	@echo "Not deploying as not on master branch"

can_i_deploy: .env
	@echo "can_i_deploy"
	@"${PACT_CLI}" broker can-i-deploy \
	  --pacticipant ${PACTICIPANT} \
	  --version ${GIT_COMMIT} \
	  --to-environment test \
	  --retry-while-unknown 0 \
	  --retry-interval 10

deploy_app:
	@echo "Deploying to prod"

record_release: .env
	@"${PACT_CLI}" broker record-release \
	  --pacticipant ${PACTICIPANT} \
	  --version ${GIT_COMMIT} \
	  --environment test

record_deployment: .env
	@"${PACT_CLI}" broker record-deployment --pacticipant ${PACTICIPANT} --version ${GIT_COMMIT} --environment production

## ======================
## Misc
## ======================

.env:
	touch .env
