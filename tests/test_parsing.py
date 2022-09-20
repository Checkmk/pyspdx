"""unittests for pyspdx/parsing.py"""

from typing import List

import pytest
from pyparsing.exceptions import ParseException

from pyspdx.parsing import (
    LICENSE_EXCEPTION,
    LICENSE_EXPRESSION,
    LICENSE_ID,
    LICENSE_REF,
    SIMPLE_EXPRESSION,
    WITH_EXPRESSION,
)


def test_license_ref() -> None:
    assert LICENSE_REF.parse_string(
        "LicenseRef-MIT-Style-2", parse_all=True
    ).as_list() == ["LicenseRef-", "MIT-Style-2"]
    assert LICENSE_REF.parse_string(
        "DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2", parse_all=True
    ).as_list() == ["DocumentRef-", "spdx-tool-1.2", ":", "LicenseRef-", "MIT-Style-2"]


def test_license_id() -> None:
    assert LICENSE_ID.parse_string("MIT", parse_all=True).as_list() == ["MIT"]
    assert LICENSE_ID.parse_string("mit", parse_all=True).as_list() == ["MIT"]
    with pytest.raises(ParseException):
        LICENSE_ID.parse_string("MIT2", parse_all=True)


def test_license_exception() -> None:
    assert LICENSE_EXCEPTION.parse_string(
        "389-exception", parse_all=True
    ).as_list() == ["389-exception"]
    assert LICENSE_EXCEPTION.parse_string(
        "389-eXCEPTion", parse_all=True
    ).as_list() == ["389-exception"]
    with pytest.raises(ParseException):
        LICENSE_EXCEPTION.parse_string("MIT", parse_all=True)


@pytest.mark.parametrize(
    "expression,result",
    [
        ("Apache-2.0 WITH 389-exception", ["Apache-2.0", "WITH", "389-exception"]),
        ("Apache-2.0 WITH LLVM-exception", ["Apache-2.0", "WITH", "LLVM-exception"]),
        ("MIT", []),
    ],
)
def test_with_license_exception(expression: str, result: List[str]) -> None:
    if result:
        assert (
            WITH_EXPRESSION.parse_string(expression, parse_all=True).as_list() == result
        )
    else:
        with pytest.raises(ParseException):
            LICENSE_EXCEPTION.parse_string(expression, parse_all=True)


@pytest.mark.parametrize(
    "expression,result",
    [
        ("MIT", ["MIT"]),
        ("MIT and BSD", []),
        ("LicenseRef-MIT-Style-2", ["LicenseRef-", "MIT-Style-2"]),
        ("389-exception", []),
        (
            "DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2",
            ["DocumentRef-", "spdx-tool-1.2", ":", "LicenseRef-", "MIT-Style-2"],
        ),
    ],
)
def test_simple_expression(expression: str, result: List[str]) -> None:
    if not result:
        with pytest.raises(ParseException):
            SIMPLE_EXPRESSION.parse_string(expression, parse_all=True)
    else:
        assert (
            SIMPLE_EXPRESSION.parse_string(expression, parse_all=True).as_list()
            == result
        )


@pytest.mark.parametrize(
    "expression,successful",
    [
        ("MIT AND MIT", True),
        ("MIT WITH 389-exception", True),
        ("MIT OR MIT", True),
        ("MIT OR MIT AND MIT", True),
        ("MIT OR (MIT AND MIT)", True),
        ("(MIT OR MIT) AND MIT", True),
        ("(MIT OR MIT AND MIT", False),
        ("MIT", True),
        ("FOO", False),
        ("DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2", True),
        ("MIT+", True),
        ("MIT +", False),
        (
            "(DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2 OR MIT)",
            True,
        ),
        (
            "(Apache-2.0 WITH 389-exception OR BSD-3-Clause)",
            True,
        ),
        (
            "(BSD-3-Clause OR Apache-2.0 WITH 389-exception)",
            True,
        ),
        ("(MIT OR MIT) AND MIT OR MIT", True),
        (
            "(DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2 OR MIT) AND (BSD-3-Clause OR Apache-2.0 WITH 389-exception)",
            True,
        ),
        (
            "(DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2 OR (Apache-2.0 AND PostgreSQL OR OpenSSL)) AND (BSD-3-Clause OR Apache-2.0 WITH 389-exception)",
            True,
        ),
    ],
)
def test_compound_expression(expression: str, successful: bool) -> None:
    if successful:
        # No exception
        LICENSE_EXPRESSION.parse_string(expression, parse_all=True)
        return

    with pytest.raises(ParseException):
        LICENSE_EXPRESSION.parse_string(expression, parse_all=True)
