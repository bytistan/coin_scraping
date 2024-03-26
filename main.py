import requests
from bs4 import BeautifulSoup
from database import Database
from datetime import datetime

class Main:
    def __init__(self):
        self.url = "https://coinmarketcap.com/"
        self.database = Database() # You have to give database information in info.json

        self.info_default = {
            "coin_name":[2,"p"],
            "price":[3,"span"]
        }

        self.info_not_load = {
            "coin_name":[2,"a"],
            "price":[3,None]
        }

    def scrap_default(self,tr):
        return [tr.find_all("td")[value[0]].find(value[1]).text.replace("$","") for value in self.info_default.values()]

    def scrap_not_load(self,tr):
        return [tr.find_all("td")[value[0]].find(value[1]).text if value[1] else tr.find_all("td")[value[0]].text.replace("$","") for value in self.info_not_load.values()]

    def fix_data(self,data,values):
        for v in values:
            data.append(v)

        data[1] = float(data[1].replace(",",""))
        return data 
    
    def scrap(self,soup,db,info_id):
        for index,tr in enumerate(soup.find("table").find("tbody").find_all("tr")):
            if len(tr) == 11: 
                data = self.scrap_default(tr)

                db.add(
                    tuple(self.fix_data(data,[index,info_id])),
                    db.coin_scrap_table
                )

            if len(tr) == 5: 
                data = self.scrap_not_load(tr)

                db.add(
                    tuple(self.fix_data(data,[index,info_id])),
                    db.coin_scrap_table
                )

    def run(self):
        if self.database.conn_control():
            print("[+] Successfully connected to the database.")
        else:
            print("[-] Failed to connect to database. Check the info.json file")
            return False 
        
        r = requests.get(self.url)

        if r.status_code == 200:
            print(f"[+] Successfully connected to the {self.url}.")
        else:
            print("[-] Failed to connect from the website.")
            return False 
        
        self.database.add(
            (0,datetime.now()),
            self.database.coin_info_table
        )

        coin_info_table_id = self.database.get_all(self.database.coin_info_table["table"])[-1][0]

        soup = BeautifulSoup(r.text,"html.parser")
        self.scrap(soup,self.database,coin_info_table_id)

        self.database.update((1,coin_info_table_id),self.database.coin_info_table)

        print("[+] Data successfully saved to database.")

if __name__ == '__main__':

    main = Main()

    try:
        main.run()
    except Exception as e:
        print(f"[-] ERROR {e}")
    finally:
        main.database.close_conn()