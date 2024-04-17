import sqlite3

class DatabaseWrapper:
  """
  Base class for database interactions (CRUD operations).
  """
  def __init__(self, db_path):
    self.conn = None  # Initialize connection as None
    self.cursor = None
    self._table_name = ''
    self.db_path = db_path
    self._connect()  # Attempt connection in the constructor

  def _connect(self):
    """
    Attempts to connect to the database and creates it if it doesn't exist
    (using sqlite3).
    """
    self.conn = sqlite3.connect(self.db_path)
    self.cursor = self.conn.cursor()

  def _create_table(self, table_name):
    """
    Creates a table if it doesn't exist, reading the schema from a file.
  
    Args:
      table_name: The name of the table to create.
    """
    #abs path not good
    with open(f'H:/Slavery/Crypto Project/Database/schema/{table_name}.sql', 'r') as schema_file:
      schema = schema_file.read()
    self.cursor.execute(schema)
    self.conn.commit()

  def insert(self, table_name, data):
    """
    Inserts a new entry into a table.

    Args:
      table_name: The name of the table.
      data: A dictionary containing key-value pairs for column data.

    Returns:
      True if the entry was inserted successfully, False otherwise.
    """
    # Implement duplicate key check logic (optional)
    # ... (consider using cursor.execute("SELECT 1 FROM table_name WHERE ..."))

    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    self.cursor.execute(query, list(data.values()))
    self.conn.commit()
    return self.cursor.lastrowid if self.cursor.lastrowid else False # if a row was inserted return its id else return false

  def get(self, table_name, criteria=None):
    """
    Retrieves data from a table based on criteria.

    Args:
      table_name: The name of the table.
      criteria: A dictionary with key-value pairs representing conditions (optional).

    Returns:
      A list of dictionaries containing retrieved data (empty list if none found).
    """
    query = f"SELECT * FROM {table_name}"
    if criteria:
      where_clause = ' AND '.join([f"{key} = ?" for key in criteria])
      query += f" WHERE {where_clause}"
    self.cursor.execute(query, list(criteria.values()) if criteria else [])
    return self.cursor.fetchall()

  def update(self, table_name, data, criteria):
    """
    Updates data in a table based on criteria.

    Args:
      table_name: The name of the table.
      data: A dictionary containing key-value pairs for columns to update.
      criteria: A dictionary with key-value pairs representing conditions.

    Returns:
      True if data was updated successfully, False otherwise.
    """
    set_clause = ', '.join([f"{key} = ?" for key in data])
    where_clause = ' AND '.join([f"{key} = ?" for key in criteria])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    self.cursor.execute(query, list(data.values()) + list(criteria.values()))
    self.conn.commit()
    return self.cursor.rowcount > 0  # Check if at least one row was updated

  def delete(self, table_name, criteria):
    """
    Deletes entries from a table based on criteria.

    Args:
      table_name: The name of the table.
      criteria: A dictionary with key-value pairs representing conditions.

    Returns:
      True if entries were deleted successfully, False otherwise.
    """
    where_clause = ' AND '.join([f"{key} = ?" for key in criteria])
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    self.cursor.execute(query, list(criteria.values()))
    self.conn.commit()
    return self.cursor.rowcount > 0  # Check if at least one row was deleted

  def close(self):
    """
    Closes the database connection if it exists.
    """
    if self.conn:
      self.conn.close()
