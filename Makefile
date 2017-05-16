ARTIFACT_URL := https://downloads.dcos.io/dcos/testing/master/dcos_generate_config.sh
DCOS_DOCKER_REPOSITORY := https://github.com/adamtheturtle/dcos-docker.git
DCOS_DOCKER_BRANCH := macos-DCOS-15645

ARTIFACT_PATH := /tmp/dcos_generate_config.sh
DCOS_DOCKER_CLONE_PATH := /tmp/dcos-docker

# Run various linting tools.
lint:
	flake8 .
	isort --recursive --check-only
	yapf --diff --parallel --recursive . | python -c 'import sys; result = sys.stdin.read(); assert not result, result;'
	mypy src/ tests/
	pydocstyle

# Attempt to clean leftovers by the test suite.
clean:
	docker stop $$(docker ps -a -q --filter="name=dcos-") | :
	docker rm --volumes $$(docker ps -a -q --filter="name=dcos-") | :
	# We skip errors because this does not exist in legacy versions of
	# Docker
	- docker volume prune --force
	sudo rm -rf /tmp/dcos-docker-*

# Fix some linting errors.
fix-lint:
	yapf --in-place --parallel --recursive .
	isort --recursive --apply

clean-dcos-docker:
	- rm -rf $(DCOS_DOCKER_CLONE_PATH)

clean-artifact:
	- rm -rf $(ARTIFACT_PATH)

download-dcos-docker:
	git clone -b $(DCOS_DOCKER_BRANCH) $(DCOS_DOCKER_REPOSITORY) $(DCOS_DOCKER_CLONE_PATH)

download-artifact:
	curl -o $(ARTIFACT_PATH) $(ARTIFACT_URL)

clean-dependencies: clean-dcos-docker clean-artifact

download-dependencies: download-artifact download-dcos-docker
