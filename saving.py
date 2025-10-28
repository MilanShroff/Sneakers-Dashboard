import mysql.connector
from mysql.connector import Error
from Beautiful import sneakers 


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='sneakers_db',
            user='root',
            password=''
        )
        if connection.is_connected():
            print("Connection to MySQL database established successfully.")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sneakers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            price FLOAT,
            location VARCHAR(255),
            shipping_cost FLOAT,
            `condition` VARCHAR(50),
            brand VARCHAR(100),
            UNIQUE (title, price, location)
        )
        """
        cursor.execute(create_table_query)
        print("Sneakers table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_sneaker_data(connection, sneakers):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT IGNORE INTO sneakers (title, price, location, shipping_cost, `condition`, brand)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        inserted_count = 0
        for sneaker in sneakers:
            if sneaker['title'] == "Shop on eBay" or sneaker['title'] == "N/A":
                continue 

            data = (
                sneaker['title'],
                sneaker['price'],
                sneaker['location'],
                sneaker['shipping_cost'],
                sneaker['condition'],
                sneaker['brand']
            )
            cursor.execute(insert_query, data)
            inserted_count += 1

        connection.commit()
        print(f"{inserted_count} new records inserted into the database.")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()


def main():
    if sneakers:
        connection = create_connection()

        if connection:
            create_table(connection)
            insert_sneaker_data(connection, sneakers)
            connection.close()
        else:
            print("Failed to establish connection to MySQL.")
    else:
        print("No data available to insert. Exiting...")


if __name__ == '__main__':
    main()
