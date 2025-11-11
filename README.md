# strawberry utils

[![codecov](https://codecov.io/gh/Arfey/strawberry-utils/graph/badge.svg?token=CSUCQA6L3Y)](https://codecov.io/gh/Arfey/strawberry-utils)

## OnlyOnceExecution

Prevents expensive or unsafe fields from being resolved more than once per request,
improving performance and ensuring data consistency.

Ensure your context includes an `only_once_set` attribute, initialized as an empty set:

```python
from dataclasses import dataclass, field

@dataclass
class Context:
    only_once_set: set[str] = field(default_factory=set)
```

Then, apply the extension to your field:

```python
import strawberry
from strawberry_utils.extensions.only_once_execution import OnlyOnceExecution

@strawberry.type
class Query:
    @strawberry.field(extensions=[OnlyOnceExecution()])
    async def not_optimized_field(self) -> str:
        return 'not optimized'
```

If the same field is requested multiple times in a single query, an error will be raised.
