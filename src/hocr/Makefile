.DEFAULT_GOAL := help
.PHONY: help api-docs
.SILENT: api-docs

# dockerbuild dir (cpu/gpu)
DOCKERBUILD_FOLDER=gpu

# run environment (dev:0 / server: 1)
RUN_ENV=1

help: ## This prints help text for all the existing commands
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%25s:\033[0m %s\n", $$1, $$2}'

www:  ## Makes documentation from all the subsystems
	atk-webgen.sh .

publish: ## Publishes the documentation
	echo "Not yet done"

install-dev: clean install-models ## Installs the modules for dev purposes
	pip install --extra-index-url https://pypi.own3.aganitha.ai -e .

install-prod: clean ## Installs the modules in prod setting
	pip install --extra-index-url https://pypi.own3.aganitha.ai .

install-models: ## Installs the models for the project at ATK_PROJECTS_FOLDER
	@echo "No models to install"

install: install-prod install-models ## Production ready installation for root

test: install ## Runs the tests
	cd examples && make test

uninstall: ## Uninstalls the module
	pip uninstall -y ocr

pip-freeze: ## Freeze python package requirements

		pip freeze | cat requirements.txt - | sort | uniq > all_reqs.txt

		sed -i '' '/^#/d' all_reqs.txt
		sed -i '' '/^-e/d' all_reqs.txt

		cp all_reqs.txt requirements.txt
		cp all_reqs.txt dockerbuild/cpu/python_requirements.txt
		cp all_reqs.txt dockerbuild/gpu/python_requirements.txt

		# Replace tensorflow with tensorflow-gpu if found
		sed -i -e 's/tensorflow/tensorflow-gpu/g' dockerbuild/gpu/python_requirements.txt

		@grep -q 'tensorflow' requirements.txt 2>/dev/null || true

		# Removing tensorflow from outer requirements.txt since, we cannot rely on pip-freeze from dev-box to tell
		# which cpu/gpu version of tensorflow is needed.
		sed -i '' '/^tensorflow/d' requirements.txt 2>/dev/null || true

		# Clean up
		rm all_reqs.txt dockerbuild/gpu/python_requirements.txt-e

		@echo "Removing tensorflow in requirements.txt. If you need tensorflow, manually install it."

bundle:  ## Create a python bundle
		echo "Bundling python package"
		python setup.py sdist bdist_wheel

dirty-check: ## Checks to see if there are any uncommitted changes
	@git diff --exit-code

tag-check: ## Checks to see for presence of version tag pointing to the latest commit
	@test `git describe --tag` = `cat VERSION`
	@git ls-remote --exit-code --tags origin `cat VERSION`

pip-push: clean bundle dirty-check tag-check ## Pushes the module to the Pypi server
		echo "Pushing to local Pypi server"
		twine upload --repository aganitha-own3 dist/*
		make clean

clean:
	rm -rf build/*
	rm -rf dist/*
	rm -rf *.egg-info
	find . -name "__pycache__" -exec rm -rf {} \+

sphinx-setup:
		(rm -rf ref_docs/source/*.rst)
		(pandoc --from=markdown --to=rst --output=ref_docs/source/readme.rst README.md)
		(cat ref_docs/source/readme.rst ref_docs/source/index.rst.tmpl > temp && mv temp ref_docs/source/index.rst)
		(rm -rf ref_docs/source/readme.rst)

api-docs: sphinx-setup ## Generate Sphinx API docs
		(cd ref_docs && ./build_start.sh && ${MAKE} html)


publish-api-docs: api-docs ## Publish sphinx api docs
		cd ref_docs/build/html && python -m http.server

create_dockerfile: dockerbuild/dockerfile_config.yaml ## Create Dockerfile, build_image.sh using template
		atk-docker.sh dockerfile dockerbuild/dockerfile_config.yaml dockerbuild/$(DOCKERBUILD_FOLDER)

create_container_runner: dockerbuild/run_container_config.yaml ## Create run_container.sh using template
		atk-docker.sh container dockerbuild/run_container_config.yaml dockerbuild/$(DOCKERBUILD_FOLDER) $(RUN_ENV)

build_image: dockerbuild/$(DOCKERBUILD_FOLDER)/Dockerfile dockerbuild/$(DOCKERBUILD_FOLDER)/build_image.sh ## Run generated build_image.sh
		atk-docker.sh build_image dockerbuild/$(DOCKERBUILD_FOLDER)

run_container: dockerbuild/$(DOCKERBUILD_FOLDER)/run_container.sh ## Run generated run_container.sh
		atk-docker.sh run_container dockerbuild/$(DOCKERBUILD_FOLDER)

create_docker_env: create_dockerfile create_container_runner ## Create Dockerfile,build_image.sh and run_container.sh
