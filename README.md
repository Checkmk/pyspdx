# pyspdx

Short library to validate SPDX expressions. I have not found any working implementation in python and I wanted to mess around with pyparsing anyways.

I meanwhile found a similar library https://pypi.org/project/license-expression/.

## API / Usage
This lib only exposes two functions:

```
from pyspdx import validate, tokenize

validate("MIT")  # Valid, does nothing
validate("NotValid") # Throws ValueError
validate("(Apache-2.0 OR MIT) AND BSD-3-Clause") # Valid
validate("(DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2 OR (Apache-2.0 AND PostgreSQL OR OpenSSL)) AND (BSD-3-Clause OR Apache-2.0 WITH 389-exception)") # Valid

assert tokenize("MIT") == ["MIT"]
```

## Used Sources
- https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
- https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html
