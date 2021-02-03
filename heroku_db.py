import psycopg2 as psycopg2
import pandas as pd


def connect_database():
    """
    Connection to work with the remote database on Heroku platform.
    :return: connection
    """
    connection = psycopg2.connect(
        database="d22k9v8fan3kou",
        user="ngssnfxllikhbg",
        password="bcf05d8915c2eefdc890f6968ea5803b5ebd4be7f115b34c56590315eca147c2",
        host="ec2-54-73-253-140.eu-west-1.compute.amazonaws.com",
        port="5432"
    )

    return connection


def drop_tables():
    connect = connect_database()
    cur = connect.cursor()

    cur.execute('''
        DROP TABLE IF EXISTS categories CASCADE
        ''')

    cur.execute('''
        DROP TABLE IF EXISTS information CASCADE
        ''')

    connect.commit()


def create_tables():
    """
    Create tables in database.
    :return: None
    """
    connect = connect_database()
    cur = connect.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id serial PRIMARY KEY,
        category varchar(255)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS information (
        id serial PRIMARY KEY,
        title varchar(1000),
        url_item varchar(1000),
        url_image varchar(1000),
        price NUMERIC(5,2),
        categoryId INT,
        FOREIGN KEY (categoryId) REFERENCES categories(id)
    );
    ''')

    connect.commit()


def insert_into_tables_category():
    """
    Insert information into created tables
    :return: None
    """
    connect = connect_database()
    cur = connect.cursor()

    cur.execute('''
        INSERT INTO categories (category) VALUES ('sale');
        INSERT INTO categories (category) VALUES ('dresses');
        INSERT INTO categories (category) VALUES ('shoes');
        ''')

    connect.commit()


def insert_into_table_information(total_items):
    """
    Creating column list for insertion (cols) and insert DataFrame records one by one into created tables.
    :return: None
    """
    connect = connect_database()
    cur = connect.cursor()

    for i, row in total_items.iterrows():
        sql = "INSERT INTO information (title, url_item, url_image, price, categoryId) VALUES (" + "%s," * (len(row) - 1) + "%s)"
        cur.execute(sql, tuple(row))

    connect.commit()


def export_to_csv():
    """
    Execute query, fetch all the records and export it to csv file.
    :return: csv file.
    """
    connect = connect_database()
    cur = connect.cursor()
    cur.execute('''
            SELECT information.id, information.title, information.url_item, 
            information.url_image, information.price, categories.category
            FROM information
            JOIN categories
            ON information.categoryid = categories.id
            ''')

    all_information = cur.fetchall()
    pd.DataFrame(all_information).to_csv("all_information.csv",
                                         header=['id', 'title', 'url_item', 'url_image', 'price', 'category'],
                                         index=False)

    connect.commit()

