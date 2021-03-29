import logging
import mysql.connector
from mysql.connector import errorcode
from odd_contract.models import DataEntity
from adapter import _adapter_prefix
from adapter import _table_metadata, _table_table, _table_order_by
from adapter import _column_metadata, _column_table, _column_order_by
from adapter.table import _map_table
from app.abstract_adapter import AbstractAdapter
from config import get_env


def create_adapter() -> AbstractAdapter:
    return MysqlAdapter()


class MysqlAdapter(AbstractAdapter):
    __cloud_prefix = ""
    __connection = None
    __cursor = None

    # replace
    def __init__(self) -> None:
        self.__host = get_env("MYSQLHOST", "localhost")
        self.__port = get_env("MYSQLPORT", "3306")
        self.__database = get_env("MYSQLDATABASE", "")
        self.__user = get_env("MYSQLUSER", "")
        self.__password = get_env("MYSQLPASSWORD", "")
        self.__data_source_oddrn = f"//{self.__cloud_prefix}{_adapter_prefix}{self.__host}"
        super().__init__()

    def get_data_source_oddrn(self) -> str:
        return self.__data_source_oddrn

    def get_datasets(self) -> list[DataEntity]:
        try:
            self.__connect()

            tables = self.__query(_table_metadata, _table_table, _table_order_by)
            columns = self.__query(_column_metadata, _column_table, _column_order_by)

            return _map_table(self.get_data_source_oddrn(), tables, columns)
        except Exception:
            logging.error("Failed to load metadata for tables")
            logging.exception(Exception)
        finally:
            self.__disconnect()
        return []

    def __query(self, columns: str, table: str, order_by: str) -> list[tuple]:
        return self.__execute(f"select {columns} from {table} order by {order_by}")

    def __execute(self, query: str) -> list[tuple]:
        self.__cursor.execute(query)
        records = self.__cursor.fetchall()
        return records

    # replace
    def __connect(self):
        try:
            self.__connection = mysql.connector.connect(
                host=self.__host, port=self.__port, database=self.__database,
                user=self.__user, password=self.__password)
            self.__cursor = self.__connection.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
            else:
                logging.error(err)
            raise DBException("Database error")
        return

    # replace
    def __disconnect(self):
        try:
            if self.__cursor:
                self.__cursor.close()
        except Exception:
            pass
        try:
            if self.__connection:
                self.__connection.close()
        except Exception:
            pass
        return


class DBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
