PYTHON := poetry run python
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
MYPY := $(PYTHON) -m mypy
PYLINT := $(PYTHON) -m pylint
PYTEST := $(PYTHON) -m pytest

test: test-format mypy pylint doctest pytest

mypy:
	$(MYPY) pyspdx/ tests/

test-format:
	$(BLACK) --check pyspdx/ tests/
	$(ISORT) --check pyspdx/ tests/


pylint:
	$(PYLINT) pyspdx/ tests/

doctest:
	$(PYTEST) --doctest-modules pyspdx/

pytest:
	$(PYTEST) tests/
