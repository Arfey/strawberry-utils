from dataclasses import (
    dataclass,
    field,
)
from unittest import TestCase

import strawberry

from strawberry_utils.extensions.only_once_execution import OnlyOnceExecution


class TestOnlyOnceExecution(TestCase):
    def setUp(self):

        @dataclass
        class Context:
            only_once_set: set[str] = field(default_factory=set)

        self.context = Context()

        @strawberry.type
        class OnlyOnceExecutionQueryType:
            @strawberry.field(extensions=[OnlyOnceExecution()])
            def test(self) -> str:
                return "test"

        self.schema = strawberry.schema.Schema(
            query=OnlyOnceExecutionQueryType
        )

    def test_only_once_execution(self):
        data = self.schema.execute_sync(
            "query { test }", context_value=self.context
        )
        assert data.data == {"test": "test"}

    def test_only_once_execution_error(self):
        with self.assertLogs("strawberry.execution", level="ERROR") as logger:
            data = self.schema.execute_sync(
                "query { test test2: test }", context_value=self.context
            )
            assert (
                data.errors[0].message
                == "Field 'NoneType.test' has already been resolved"
            )

            self.assertEqual(len(logger.output), 1)
