"""
    literalquery
    https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    how to print the actual query (with values) not like the statement generated
    by SQLAlchemy
"""
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.orm import Query
from sqlalchemy.sql.sqltypes import DateTime, NullType, String


class StringLiteral(String):
    """Teach SA how to literalize various things."""

    def literal_processor(self, dialect):
        super_processor = super(StringLiteral, self).literal_processor(dialect)

        def process(value):
            if isinstance(value, int):
                return str(value)
            if not isinstance(value, str):
                value = str(value)
            result = super_processor(value)
            if isinstance(result, bytes):
                result = result.decode(dialect.encoding)
            return result

        return process


class LiteralDialect(DefaultDialect):
    colspecs = {
        # prevent various encoding explosions
        String: StringLiteral,
        # teach SA about how to literalize a datetime
        DateTime: StringLiteral,
        # don't format py2 long integers to NULL
        NullType: StringLiteral,
    }


def literalquery(statement):
    """
    NOTE: This is entirely insecure. DO NOT execute the resulting strings.
    """
    if isinstance(statement, Query):
        statement = statement.statement
    return statement.compile(
        dialect=LiteralDialect(),
        compile_kwargs={"literal_binds": True},
    ).string
