"""pyparsing code for SPDX

https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
"""

import pyparsing as pp

from pyspdx.license_exceptions import LICENSE_EXCEPTION_LIST
from pyspdx.licenseids import LICENSE_ID_LIST

IDSTRING = pp.Word(pp.alphanums + "-.")
LICENSE_ID = pp.one_of(LICENSE_ID_LIST, caseless=True, asKeyword=True)
LICENSE_EXCEPTION = pp.one_of(LICENSE_EXCEPTION_LIST, caseless=True, asKeyword=True)
LICENSE_REF = pp.Opt("DocumentRef-" + IDSTRING + ":") + "LicenseRef-" + IDSTRING

SIMPLE_EXPRESSION = LICENSE_ID ^ pp.Combine(LICENSE_ID + "+") ^ LICENSE_REF
WITH_EXPRESSION = SIMPLE_EXPRESSION + "WITH" + LICENSE_EXCEPTION

LICENSE_EXPRESSION = pp.infix_notation(
    WITH_EXPRESSION ^ SIMPLE_EXPRESSION,
    [
        ("AND", 2, pp.opAssoc.LEFT),
        ("OR", 2, pp.opAssoc.LEFT),
    ],
    lpar=pp.Literal("("),
    rpar=pp.Literal(")"),
)
