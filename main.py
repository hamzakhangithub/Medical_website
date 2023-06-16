from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from datetime import date

app = FastAPI()

# Update your database connection parameters here
db_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "customers",
}


def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Successfully connected to the database")
        return connection
    except Error as e:
        print("Error connecting to the database", e)
        raise e


class MedicalItem(BaseModel):
    item_id: int
    item_name: str
    category: str
    price: float
    stock_quantity: int


class MedicalItemUpdate(BaseModel):
    item_name: str
    category: str
    price: float
    stock_quantity: int


@app.get("/medical_items")
def get_medical_items():
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Medical_Items")
        medical_items = cursor.fetchall()
    return medical_items


@app.post("/medical_items", status_code=status.HTTP_201_CREATED)
def create_medical_item(medical_item: MedicalItem):
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO Medical_Items(item_id, item_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s, %s)""",
            (
                medical_item.item_id,
                medical_item.item_name,
                medical_item.category,
                medical_item.price,
                medical_item.stock_quantity,
            ),
        )
        connection.commit()
        cursor.execute(
            "SELECT * FROM Medical_Items WHERE item_id = %s", (medical_item.item_id,)
        )
        new_medical_item = cursor.fetchone()
    return {"data": new_medical_item}


@app.get("/medical_items/{id}")
async def get_medical_item(id: int, response: Response):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Medical_Items WHERE item_id = %s", (id,))
            medical_item = cursor.fetchone()
    except Error as e:
        print(f"The error '{e}' occurred")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}

    if medical_item:
        return {"Medical_item_detail": medical_item}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Medical item with id {id} not found"}


@app.put("/medical_items/{id}")
def update_medical_item(id: int, item: MedicalItemUpdate):
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)

        # Update the medical_items record
        cursor.execute(
            """
            UPDATE Medical_Items
            SET item_name = %s, category = %s, price = %s, stock_quantity = %s
            WHERE item_id = %s
        """,
            (item.item_name, item.category, item.price, item.stock_quantity, id),
        )
        connection.commit()

    if cursor.rowcount:
        return {"message": f"Medical item with id {id} has been updated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical item with id {id} does not exist",
        )


@app.delete("/medical_items/{id}")
def delete_medical_item(id: int, response: Response):
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM Medical_Sales WHERE item_id = %s", (id,))
        cursor.execute("DELETE FROM Medical_Items WHERE item_id = %s", (id,))
        connection.commit()

    if cursor.rowcount:
        return {"message": f"Medical item with id {id} has been deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medical item with id {id} does not exist",
        )
