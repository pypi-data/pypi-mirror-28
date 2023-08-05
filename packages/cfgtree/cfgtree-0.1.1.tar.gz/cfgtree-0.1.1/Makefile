.PHONY: build docs

MODULE:=cfgtree


all: dev style checks requirements dists test docs release-note


dev: update-pip pipenv-install-dev ln-venv

update-pip:
	# Freeze the version of pip and pipenv for setup reproductibility
	pip3 install -U --user 'pip==9.0.1' 'pipenv==9.0.1' 'setuptools>=36.6.0'

pipenv-install-dev:
	@echo "Setting up development environment"
	pipenv install --dev

install-local:
	pipenv install --skip-lock

install-system:
	pipenv install --system

ln-venv:
	@# this target creates a .venv link to your virtual env binaries
	@# useful for some editors that does not know how to find the venv automatically
	@ln -sf $$(pipenv --venv) .venv
	@cd .venv/lib && ln -sf python$$(pipenv run python --version | cut -f2 -d' '|cut -c1-3) python


style: isort autopep8 yapf

isort:
	pipenv run isort -y

autopep8:
	pipenv run autopep8 --in-place --recursive setup.py $(MODULE)

yapf:
	pipenv run yapf --style .yapf --recursive -i $(MODULE)


checks: flake8 pylint

flake8:
	pipenv run python setup.py flake8

pylint:
	pipenv run pylint --rcfile=.pylintrc --output-format=colorized $(MODULE)


shell:
	pipenv shell


dists: requirements sdist bdist wheels

build: dists

sdist:
	pipenv run python setup.py sdist

bdist:
	pipenv run python setup.py bdist

wheels:
	pipenv run python setup.py bdist_wheel



test:
	pipenv run pytest $(MODULE)

test-coverage:
	pipenv run py.test -v --cov $(MODULE) --cov-report term-missing


requirements:
	# needed until PBR supports `Pipfile`
	pipenv run pipenv_to_requirements

pypi-publish: build
	pipenv run python setup.py upload -r pypi

update:
	pipenv update

githook: style requirements

push: githook
	git push origin --all
	git push origin --tags

reno-new:
	pipenv run reno new slug

reno-lint:
	pipenv run reno lint

release-note:
	pipenv run reno report

release-note-github:
	pipenv run reno report | pandoc -f rst -t markdown

docs:
	pipenv run make -C docs html

clean:
	pipenv --rm ; true
	find . -name '__pycache__' -delete
	find . -name "*.pyc" -exec rm -f {} \;
	rm -f *.log
	rm -f *.log.*
	rm -rf .eggs *.egg-info
	rm -rf dist/ build/
	rm -rf .venv
	rm -rf docs/_build

# aliases to gracefully handle typos on poor dev's terminal
check: checks
devel: dev
develop: dev
doc: docs
dist: dists
install: install-system
pypi: pypi-publish
styles: style
wheel: wheels
