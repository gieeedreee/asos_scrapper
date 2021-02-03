import pandas as pd
import requests
from bs4 import BeautifulSoup

import heroku_db


def collect_information (items_per_category: int, category_list: list, items_per_page: int) -> pd.DataFrame:
    """
    Function for scraping Asos.com website according to specified parameters.
    :param category_list: list of categories to scrape
    :param items_per_page: number of items per page on website
    :param items_per_category: quantity of items per each category to scrape
    :return:
    """
    pages = round(items_per_category / items_per_page)
    title, price, url_item, url_image = ([] for i in range(4))

    for item in category_list:
        for page_no in range(pages):
            page = requests.get(f"https://www.asos.com/women/{item}&page={page_no}",
                                headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(page.content, "html.parser")

            try:
                title.extend([value.text for value in soup.find_all("div", class_="_3J74XsK")])
                url_item.extend([value["href"] for value in soup.find_all("a", class_="_3TqU78D")])
                price.extend([value.text for value in soup.find_all("span", class_="_16nzq18")])
                url_image = soup.find('img', class_='_2r9Zh0W')['src']
            except:
                pass

    return pd.DataFrame({
        "title": title,
        "url_item": url_item,
        "url_image": url_image,
        "price_£": price,
    })


def main():
    items_per_category = 3000
    category_list = ['sale/cat/?cid=7046', 'dresses/cat/?cid=8799', 'shoes/cat/?cid=4172']
    items_per_page = 72
    pages = round(items_per_category / items_per_page)
    items_for_category = items_per_page * pages

    total_items = collect_information(items_per_category, category_list, items_per_page)
    # Rename and change 'price' type
    total_items['price_£'] = total_items['price_£'].str.replace('[\£]', '').astype(float)

    # Add category to dataframe 'total_items'
    total_items['categoryid'] = ''
    total_items.iloc[0:items_for_category]["categoryid"] = '1'
    total_items.iloc[items_for_category:(items_for_category * 2)]["categoryid"] = '2'
    total_items.iloc[(items_for_category * 2):(items_for_category * 3)]["categoryid"] = '3'

    heroku_db.connect_database()
    heroku_db.drop_tables()
    heroku_db.create_tables()
    heroku_db.insert_into_tables_category()
    heroku_db.insert_into_table_information(total_items)
    heroku_db.export_to_csv()


if __name__ == "__main__":
    main()
