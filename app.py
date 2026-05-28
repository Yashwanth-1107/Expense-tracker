import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Expense Tracker")

# Add Expense Section
title = st.text_input("Enter Title")

amount = st.number_input("Enter Amount")

category = st.selectbox(
    "Select Category",
    ["Food", "Travel", "Shopping"]


)

if st.button("Add Expense"):

    payload = {
        "title": title,
        "amount": amount,
        "category": category
    }

    response = requests.post(
        "http://127.0.0.1:8000/expenses",
        json=payload
    )

    st.success(response.json()["message"])

# View Expenses Section
if st.button("View Expenses"):

    response = requests.get(
        "http://127.0.0.1:8000/expenses"
    )

    data = response.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

st.subheader("Delete Expense")

delete_id = st.number_input(
    "Enter Expense ID",
    min_value=1,
    step=1
)

if st.button("Delete Expense"):

    response = requests.delete(
        f"http://127.0.0.1:8000/expenses/{delete_id}"
    )

    st.success(response.json()["message"])

st.subheader("Update Expense")

update_id = st.number_input(
    "Enter Expense ID to Update",
    min_value=1,
    step=1
)

new_title = st.text_input("New Title")

new_amount = st.number_input(
    "New Amount",
    min_value=0.0
)

new_category = st.selectbox(
    "New Category",
    ["Food", "Travel", "Shopping"]
)

if st.button("Update Expense"):

    payload = {
        "title": new_title,
        "amount": new_amount,
        "category": new_category
    }

    response = requests.put(
        f"http://127.0.0.1:8000/expenses/{update_id}",
        json=payload
    )

    st.success(response.json()["message"])

st.subheader("Search Expenses")

search_category = st.selectbox(
    "Select Category to Search",
    ["Food", "Travel", "Shopping"]
)

if st.button("Search"):

    response = requests.get(
        f"http://127.0.0.1:8000/search?category={search_category}"
    )

    data = response.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

st.subheader("Expense Analytics")

if st.button("Calculate Total Expense"):

    response = requests.get(
        "http://127.0.0.1:8000/expenses"
    )

    data = response.json()

    total = sum(item["amount"] for item in data)

    st.success(f"Total Expense: ₹{total}")

if st.button("Category Wise Totals"):

    response = requests.get(
        "http://127.0.0.1:8000/expenses"
    )

    data = response.json()

    df = pd.DataFrame(data)

    category_totals = df.groupby("category")["amount"].sum()

    st.write(category_totals)

st.subheader("Sort Expenses")

sort_option = st.selectbox(
    "Sort By",
    ["price_asc", "price_desc", "latest"]
)

if st.button("Sort Expenses"):

    response = requests.get(
        f"http://127.0.0.1:8000/sort?sort_by={sort_option}"
    )

    data = response.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

if st.button("Show Expense Chart"):

    response = requests.get(
        "http://127.0.0.1:8000/expenses"
    )

    data = response.json()

    df = pd.DataFrame(data)

    category_totals = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()

    ax.pie(
        category_totals,
        labels=category_totals.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig)