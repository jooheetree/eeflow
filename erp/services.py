from datetime import datetime

import cx_Oracle
import os
from cx_Oracle import Connection, Cursor


class OracleService:
    def __init__(self, columns: list, table: str, where: str = ''):
        self.result: list = []
        self.cursor: Cursor = self.init_env().cursor()
        query: str = self.create_query(columns, table)
        self.get_result(query, columns)

    def init_env(self) -> Connection:
        os.environ["NLS_LANG"] = ".AL32UTF8"
        dsn_tns = cx_Oracle.makedsn('155.1.19.32', '1521', service_name='KCDB')
        return cx_Oracle.connect(user=r'SYSTEM', password='Kcfeed12#$', dsn=dsn_tns)

    def get_result(self, query: str, columns: list) -> None:
        self.cursor.execute(query)
        rows: list = self.cursor.fetchall()
        max_len = len(columns) - 1
        for row in rows:
            dict_temp: dict = {}
            for i, column in enumerate(columns):
                column_name: str = list(columns[i].values())[0]
                value = row[i]

                if type(row[i]) == str:
                    value = value.strip()

                if type(row[i]) == datetime:
                    value = value.strftime('%Y-%m-%d')

                dict_temp[column_name] = value

                if max_len == i:
                    self.result.append(dict_temp)

    def create_query(self, columns: list, table: str) -> str:
        select_query: str = 'select '
        from_query: str = f'from {table} '
        where_query: str = "where rpsfx = 001"
        for column in columns:
            for k, v in column.items():
                select_query += f'{k} as {v} ,'

        return select_query[0:-1] + from_query + where_query
