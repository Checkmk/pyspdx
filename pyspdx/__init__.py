"""Code to validate SPDX expressions"""

from pyparsing.exceptions import ParseException

from pyspdx.parsing import LICENSE_EXPRESSION


def validate(spdx_str: str) -> None:
    """validate if a SPDX string is valid, raise a ValueError if not

    >>> validate("MIT")
    >>> validate("(Apache-2.0 OR MIT) AND BSD-3-Clause")
    >>> validate("MUT")
    Traceback (most recent call last):
    ...
    ValueError: 'MUT' is not a valid SPDX expression
    >>> validate("MIT WITH LLVM-exception AND APACHE-2.0")
    >>> validate("DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2")
    """
    tokenize(spdx_str)


def tokenize(spdx_str: str) -> list[str]:
    try:
        return LICENSE_EXPRESSION.parse_string(spdx_str, parse_all=True).as_list(
            flatten=True
        )
    except ParseException:
        raise ValueError(f"{spdx_str!r} is not a valid SPDX expression") from None
