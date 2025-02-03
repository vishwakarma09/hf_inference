from smolagents import Tool

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    insert,
    inspect,
    text,
)


class SqlEngine(Tool):
    name = "SQL Engine"
    description = """
    This is a tool that can be used to perform SQL queries on a database."""
    inputs = {
        "task": {
            "type": "string",
            "description": "The task to perform. This can be from one of the following options: 'create table' to create new table, 'insert rows' to insert rows into a table, 'query' to query the table, 'get columns info' to get the columns information of a table.",
        },
        "table_name": {
            "type": "string",
            "description": "The name of the table to perform the task on.",
        },
        "columns": {
            "type": "list",
            "description": "The columns to create the table with. Each column should be a tuple of the form (name, type).",
        },
        "rows": {
            "type": "list",
            "description": "The rows to insert into the table. Each row should be a dictionary with the column names as keys.",
        },
        "query_str": {
            "type": "string",
            "description": "The query to perform on the table.",
        },
    }
    output_type = "string"

    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def create_table(self, table_name, columns):
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine)

    def insert_rows(self, table_name, rows):
        table = self.metadata.tables[table_name]
        with self.engine.begin() as connection:
            for row in rows:
                stmt = insert(table).values(**row)
                connection.execute(stmt)

    def query(self, query_str):
        with self.engine.connect() as connection:
            result = connection.execute(text(query_str))
            return result.fetchall()

    def get_columns_info(self, table_name):
        inspector = inspect(self.engine)
        columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table_name)]
        return columns_info

    """ implement the forward method """
    def forward(self, task, table_name, columns, rows, query_str):
        """ depending on the task, call the appropriate method """
        if task == "create table":
            self.create_table(table_name, columns)
        elif task == "insert rows":
            self.insert_rows(table_name, rows)
        elif task == "query":
            self.query(query_str)
        elif task == "get columns info":
            self.get_columns_info(table_name)
        else:
            raise ValueError(f"Task {task} not recognized.")
        



# engine = create_engine("sqlite:///experiment_4/courses.db:")
# metadata_obj = MetaData()

# # create city SQL table
# table_name = "receipts"
# receipts = Table(
#     table_name,
#     metadata_obj,
#     Column("receipt_id", Integer, primary_key=True),
#     Column("customer_name", String(16), primary_key=True),
#     Column("price", Float),
#     Column("tip", Float),
# )
# metadata_obj.create_all(engine)

# rows = [
#     {"receipt_id": 1, "customer_name": "Alan Payne", "price": 12.06, "tip": 1.20},
#     {"receipt_id": 2, "customer_name": "Alex Mason", "price": 23.86, "tip": 0.24},
#     {"receipt_id": 3, "customer_name": "Woodrow Wilson", "price": 53.43, "tip": 5.43},
#     {"receipt_id": 4, "customer_name": "Margaret James", "price": 21.11, "tip": 1.00},
# ]
# for row in rows:
#     stmt = insert(receipts).values(**row)
#     with engine.begin() as connection:
#         cursor = connection.execute(stmt)

# # inspect the table
# inspector = inspect(engine)
# columns_info = [(col["name"], col["type"]) for col in inspector.get_columns("receipts")]

# table_description = "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
# print(table_description)