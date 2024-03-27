## Usage

First you need to install some python package.

```bash
pip install -r requirements.txt
```

If you are using SSMS, you need to go to your database and run ```database/database.sql``` query.

You need to edit the ```info.json``` file for the script to connect to your database. If you are using localhost just leave username and password null.

NOTE : Don't change ```database_name```.

### Example

```json
{
    "driver":"SQL SERVER",
    "server_name":"DESKTOP-5U9NF4F",
    "database_name":"CoinDB",
    "username":null,
    "password":null
}
```

Finally, you can easily run the script.

```bash
python main.py
```

Your database should look like this

```bash
+-------------------+
| coin_scrap_info   |
+----+--------+---------------------+
| id | status |   created_date       |
+----+--------+---------------------+
|  1 |   ...  | 2024-03-28 12:34:56 |
|  2 |   ...  | 2024-03-28 12:45:01 |
|  3 |   ...  | 2024-03-28 13:02:18 |
| ...|   ...  |         ...         |
+----+--------+---------------------+

+-----------------------+
| coin_scrap_data       |
+----+--------------+------------+------+---------+
| id | coin_name    | coin_price | rank | info_id |
+----+--------------+------------+------+---------+
|  1 | Bitcoin      | 70048.17   |   1  |    1    |
|  2 | Ethereum     | 2155.72    |   2  |    1    |
|  3 | Binance Coin | 375.69     |   3  |    1    |
| ...|   ...        |   ...      | ...  |   ...   |
+----+--------------+------------+------+---------+
```

## Be Careful When Scraping Data

- [x] You can scrape data for personal use or non-commercial purposes.

- [ ] Excessive data scraping using automated bots or web scrapers.

- [ ] Selling the data or using it for commercial purposes.

- [ ] Any activity that could damage or crash CoinMarketCap's infrastructure.
