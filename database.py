import pyodbc
from helper import read_json

class Model:
    def __init__(self):
        self.coin_info_table = {
            "table":"coin_scrap_info",
            "columns":[
                "status",
                "created_date"
            ]
        }

        self.coin_scrap_table = {
            "table":"coin_scrap_data",
            "columns":[
                "coin_name",
                "coin_price",
                "rank",
                "info_id",
            ]
        }

class Database(Model):
    def __init__(self):
        super().__init__()
        self.info = read_json("info.json")
        self.conn = self.connect_database(self.create_conn_string(read_json("info.json")))
        self.cursor = self.conn.cursor()

    def conn_control(self):
        return self.conn if True else False

    def connect_database(self,conn_string):
        conn = pyodbc.connect(conn_string)
        return conn if conn else None
    
    def create_conn_string(self,info):
        connection_string = f"""
            DRIVER={{{info["driver"]}}};
            SERVER={info["server_name"]};
            DATABASE={info["database_name"]};
            Trust_Connection=yes;
        """

        if info["username"] and info["password"]:
            connection_string += f"UID={info["username"]};"
            connection_string += f"PWD={info["password"]}; "

        return connection_string
    
    def insert_query_maker(self,table_name,cols):
        column,v = "",""

        for index,col in enumerate(cols):
            column += col
            v += "?"
            if index != len(cols)-1:
                column += ","
                v += ","

        return f"""
            INSERT INTO dbo.{table_name} ({column})
            VALUES ({v})
        """
    
    def update_query_maker(self,table_name, cols, condition_cols):
        set_clause = ", ".join([f"{col} = ?" for col in cols])
        condition_clause = " AND ".join([f"{col} = ?" for col in condition_cols])

        return f"""
            UPDATE dbo.{table_name}
            SET {set_clause}
            WHERE {condition_clause}
        """

    def get_all(self,table_name):
        self.cursor.execute(f"SELECT * FROM dbo.{table_name}")
        return self.cursor.fetchall()
    
    def add(self,data,table_info):
        self.cursor.execute(
            self.insert_query_maker(table_info["table"],table_info["columns"]),
            data
        )

        self.conn.commit()
    
    def update(self,data,table_info):
            
        self.cursor.execute(
            self.update_query_maker(table_info["table"],["status"],["id"]),
            data
        )

        self.conn.commit()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
        print("[-] Disconnected from database.")