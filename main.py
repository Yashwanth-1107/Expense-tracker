from fastapi import FastAPI
from db import conn, cursor

app = FastAPI()

@app.post("/expenses")
def add_expense(expense: dict):

    query = """
    INSERT INTO expenses(title, amount, category)
    VALUES(%s, %s, %s)
    """

    values = (
        expense["title"],
        expense["amount"],
        expense["category"]
    )

    cursor.execute(query, values)
    conn.commit()

    return {"message": "Expense Added Successfully"}

# GET ALL EXPENSES
@app.get("/expenses")
def get_expenses():

    query = "SELECT * FROM expenses"

    cursor.execute(query)

    data = cursor.fetchall()

    return data

# GET SINGLE EXPENSE
@app.get("/expenses/{expense_id}")
def get_single_expense(expense_id: int):

    query = "SELECT * FROM expenses WHERE expense_id = %s"

    cursor.execute(query, (expense_id,))

    data = cursor.fetchone()

    return data

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    query = "DELETE FROM expenses WHERE expense_id = %s"

    cursor.execute(query, (expense_id,))

    conn.commit()

    return {"message": "Expense Deleted Successfully"}


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: dict):

    query = """
    UPDATE expenses
    SET title=%s, amount=%s, category=%s
    WHERE expense_id=%s
    """

    values = (
        expense["title"],
        expense["amount"],
        expense["category"],
        expense_id
    )

    cursor.execute(query, values)

    conn.commit()

    return {"message": "Expense Updated Successfully"}

@app.get("/search")
def search_expense(category: str):

    query = "SELECT * FROM expenses WHERE category=%s"

    cursor.execute(query, (category,))

    data = cursor.fetchall()

    return data

@app.get("/sort")
def sort_expenses(sort_by: str):

    if sort_by == "price_asc":
        query = "SELECT * FROM expenses ORDER BY amount ASC"

    elif sort_by == "price_desc":
        query = "SELECT * FROM expenses ORDER BY amount DESC"

    elif sort_by == "latest":
        query = "SELECT * FROM expenses ORDER BY created_at DESC"

    else:
        query = "SELECT * FROM expenses"

    cursor.execute(query)

    data = cursor.fetchall()

    return data