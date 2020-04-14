from datetime import datetime

import cx_Oracle
import os
from cx_Oracle import Connection, Cursor


class OracleService:
    def __init__(self):
        self.con: Connection = self.init_env()
        self.cursor: Cursor = self.con.cursor()

    def init_env(self) -> Connection:
        os.environ["NLS_LANG"] = ".AL32UTF8"
        dsn_tns = cx_Oracle.makedsn('155.1.19.32', '1521', service_name='KCDB')
        return cx_Oracle.connect(user=r'SYSTEM', password='Kcfeed12#$', dsn=dsn_tns)

    def get_result(self, query: str, columns: list) -> list:
        result: list = []
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
                    result.append(dict_temp)
        return result

    def create_select_query(self, columns: list, table: str, wheres: list) -> str:
        select_query: str = 'select '
        from_query: str = f'from {table} '
        where_query: str = "where 1 = 1 "

        if wheres:
            for where in wheres:
                where_query += f' and {where}'

        for column in columns:
            for k, v in column.items():
                select_query += f'{k} as {v} ,'

        return select_query[0:-1] + from_query + where_query + 'order by RPICU desc , RPSEQ , RPSFX'

    def execute_insert_query(self, table: str, columns: list, values: list) -> None:
        assert len(columns) == len(values)
        query: str = f" INSERT INTO {table} "
        column_query: str = '('
        value_query: str = ' VALUES ('

        for column in columns:
            column_query += f'{column},'

        column_query = column_query[0:-1] + ')'

        for value in values:
            value_query += f'{value},'

        value_query = value_query[0:-1] + ')'
        self.cursor.execute(query + column_query + value_query)
        self.con.commit()

    def execute_delete_query(self, table: str, wheres: int) -> None:
        query: str = f" DELETE FROM {table} "
        where_query: str = f" WHERE BATNO = {wheres} "
        self.cursor.execute(query + where_query)
        self.con.commit()
