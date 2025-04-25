#################################################################################
#
# Makefile for lp_graun_sifter
#
#################################################################################

PROJECT_NAME = lp_graun_sifter
REGION = eu-west-2
PYTHON_INTERPRETER = python
PYTHON_VERSION=$(PYTHON_INTERPRETER) --version
WD=$(shell pwd)
PYTHONPATH=${WD}:${WD}/src/${PROJECT_NAME}
SHELL := /bin/bash
PROFILE = default
PIP := pip

## Create python interpreter environment 
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_VERSION) \
	)
	@echo ">>> Some tools, particularly black, may have issues with Python versions 3.12.5 or greater. Consider selecting an earlier Python interpreter."
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Utility variable for invoking Python within the virtual environment
ACTIVATE_ENV := source ./venv/bin/activate

# Execute a given command form within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

# Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

###################################################################################
# Set Up

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install boto3
boto3:
	$(call execute_in_env, $(PIP) install boto3)

## Install moto
moto:
	$(call execute_in_env, $(PIP) install moto)

## Install pytest
pytest:
	$(call execute_in_env, $(PIP) install pytest)
	$(call execute_in_env, $(PIP) install pytest-cov)

## Set up dev requirements
dev-setup: black coverage bandit safety boto3 moto pytest

###################################################################################
# Test

## Run the security tests
security-test:
	$(call execute_in_env, safety scan -r ./requirements.txt --ignore 70612)

	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Check PEP-8 compliance with black
run-black:
	$(call execute_in_env, black  ./src/$(PROJECT_NAME)/*.py ./test/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -v test/)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src --cov-report term-missing test/)

## Run all checks
run-checks: security-test run-black unit-test check-coverage

###################################################################################
# Build

## Standard build option - build a PyPi-style package and zip it
build-lambda-layer:
	@if [[ -d python ]]; then \
		rm -rf python; \
	fi
	$(eval VERSION_NUM := $(shell \
		python -c "import sys; \
				   print(str(sys.version_info.major) + '.' \
				   		 + str(sys.version_info.minor))" \
	))
	mkdir -p python/lib/python$(VERSION_NUM)/site-packages
