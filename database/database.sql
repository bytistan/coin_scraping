CREATE DATABASE CoinDB;
GO

-- Using the CoinDB database
USE CoinDB;

-- Create the coin_scrap_info table
CREATE TABLE coin_scrap_info (
	id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    status INT NOT NULL,
    created_date DATETIME NOT NULL
);

-- Create the coin_scrap_data table
CREATE TABLE coin_scrap_data (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    coin_name NVARCHAR(255) NOT NULL,
    coin_price MONEY NOT NULL,
    rank INT NOT NULL,
    info_id INT NOT NULL, 
    FOREIGN KEY (info_id) REFERENCES coin_scrap_info(id)
);

GO