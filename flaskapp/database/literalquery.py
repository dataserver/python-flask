from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.sql.expression import Select
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
    Return a string representation of the given statement,
    with all bind parameters replaced with literal values.

    https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    how to print the actual query (with values) not like the statement generated
    by SQLAlchemy
    ! NOTE: This is entirely insecure. DO NOT execute the resulting strings.
    """
    import sqlalchemy.orm

    if isinstance(statement, sqlalchemy.orm.Query):
        statement = statement.statement
    return statement.compile(
        dialect=LiteralDialect(),
        compile_kwargs={"literal_binds": True},
    ).string


def literal_binded_query(statement: Select):
    """
    Return a string representation of the given statement,
    with all bind parameters replaced with literal values.

    ! NOTE: This is entirely insecure. DO NOT execute the resulting strings.
    Returns:
        str: SQLAlchemy Select statement with all bind parameters replaced with literal values.
    """

    def inline_parameters(compiled, params):
        for key, value in params.items():
            compiled = compiled.replace(f":{key}", f"'{str(value)}'")
        return compiled

    compiled = statement.compile()
    sql_with_values = inline_parameters(str(compiled), compiled.params)

    return sql_with_values


def print_sql(statement: Select):
    """
    Print the SQL statement with all bind parameters replaced with literal values.

    Args:
        statement (Select): SQLAlchemy Select statement.
    """
    sql = literal_binded_query(statement)
    print("\n\n")
    print(sql)
