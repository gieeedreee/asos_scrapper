# asos_scrapper

This repository is about scraping data collected from an online store and storing it in Heroku Postgres database.
Scraper scrapes online store Asos.com in 3 categories - sales, dresses and shoes, collected at least 3000 samples for each category and store this information of the listing: title, url to item, url of image,  price, category. 

After scrapping all data is transferred to dataframe, which is stored  into the relational database Heroku Postgres in two tables: category and information. 
Two tables are joined and joined data is written to 'all_information.csv' file.
