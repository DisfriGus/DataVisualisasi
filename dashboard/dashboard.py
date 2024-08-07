import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Function to load data from Google Drive


def load_data(url):
    return pd.read_csv(url)


# Load data
product_url = "https://drive.google.com/uc?export=download&id=1cTXgDwn_v0blae8croPgKyaIPA2caRbK"
orderItems_url = "https://drive.google.com/uc?export=download&id=1g23VYdO7KUAD8KVfH5wrv4eBsWKu-fiV"
orders_url = "https://drive.google.com/uc?export=download&id=1OcqLHPojDb0FwjPGC4Dz9IvH0vFFTOWD"
reviews_url = "https://drive.google.com/uc?export=download&id=15l4uI0-UsUSh2d5D0vTk5CO237rQ0Sgh"
catName_url = "https://drive.google.com/uc?export=download&id=1Zd1OKFP4UCT9NAwdSfV02LVNmwEKNKr5"

product_df = load_data(product_url)
orderItems_df = load_data(orderItems_url)
orders_df = load_data(orders_url)
reviews_df = load_data(reviews_url)
catName_df = load_data(catName_url)

st.title("E-Commerce Public Data Analysis")
st.header("Dio Irsaputra Siregar")

product_df['product_category_name'] = product_df['product_category_name'].fillna(
    '-')
product_df['product_name_lenght'] = product_df['product_name_lenght'].fillna(
    product_df['product_name_lenght'].mean())
product_df['product_description_lenght'] = product_df['product_description_lenght'].fillna(
    product_df['product_description_lenght'].mean())
product_df['product_photos_qty'] = product_df['product_photos_qty'].fillna(
    product_df['product_photos_qty'].mean())
product_df['product_weight_g'] = product_df['product_weight_g'].fillna(
    product_df['product_weight_g'].mean())
product_df['product_length_cm'] = product_df['product_length_cm'].fillna(
    product_df['product_length_cm'].mean())
product_df['product_height_cm'] = product_df['product_height_cm'].fillna(
    product_df['product_height_cm'].mean())
product_df['product_width_cm'] = product_df['product_width_cm'].fillna(
    product_df['product_width_cm'].mean())
st.write(product_df.info())

# Cleaning Data Order
orders_df = orders_df[orders_df['order_status'] == 'delivered']

# Cleaning Data Review
reviews_df['review_comment_title'] = reviews_df['review_comment_title'].fillna(
    '-')
reviews_df['review_comment_message'] = reviews_df['review_comment_message'].fillna(
    '-')

st.header("Data Overview")
st.subheader("Product Data")
st.write(product_df.head())
st.subheader("Order Items Data")
st.write(orderItems_df.head())
st.subheader("Orders Data")
st.write(orders_df.head())
st.subheader("Reviews Data")
st.write(reviews_df.head())
st.subheader("Category Names Data")
st.write(catName_df.head())

st.header("Exploratory Data Analysis (EDA)")

# Merging Data
orders_orderItems_df = pd.merge(
    left=orderItems_df, right=product_df, how="left", left_on="product_id", right_on="product_id")
orders_orderItems_review_df = pd.merge(
    left=orders_orderItems_df, right=reviews_df, how="inner", left_on="order_id", right_on="order_id")

# Filtering Data
orders_orderItems_review_df_under3 = orders_orderItems_review_df[
    orders_orderItems_review_df['review_score'] < 3]
orders_orderItems_review_df_up3 = orders_orderItems_review_df[
    orders_orderItems_review_df['review_score'] >= 3]

# Percentage Calculation
percentage_under3 = orders_orderItems_review_df_under3['review_id'].count(
) / orders_orderItems_review_df['review_id'].count() * 100
percentage_up3 = orders_orderItems_review_df_up3['review_id'].count(
) / orders_orderItems_review_df['review_id'].count() * 100

st.subheader("Distribution of Ratings")
st.write(f"Persentase rating dibawah 3: {percentage_under3:.2f}%")
st.write(f"Persentase rating 3 dan diatas: {percentage_up3:.2f}%")

# Visualization for Question 1
data = {
    'category': ['Rating 3 Ke Atas', 'Rating Dibawah 3'],
    'count': [orders_orderItems_review_df_up3['review_id'].count(), orders_orderItems_review_df_under3['review_id'].count()]
}
rating_df = pd.DataFrame(data)
total_count = rating_df['count'].sum()
rating_df['percentage'] = (rating_df['count'] / total_count) * 100

fig1, ax1 = plt.subplots()
ax1.pie(rating_df['percentage'], labels=rating_df['category'],
        autopct='%1.1f%%', startangle=140)
ax1.set_title('Distribusi Rating Kategori')
st.pyplot(fig1)

# Visualization for Question 2
orders_orderItems_review_product_df = pd.merge(left=orders_orderItems_review_df_under3,
                                               right=product_df,
                                               how="inner",
                                               left_on="product_id",
                                               right_on="product_id")
orders_orderItems_review_product_df = pd.merge(left=orders_orderItems_review_product_df,
                                               right=catName_df,
                                               how="left",
                                               left_on="product_category_name_x",
                                               right_on="product_category_name")

item_counts = orders_orderItems_review_product_df['product_category_name_english'].value_counts(
)
fig2, ax2 = plt.subplots(figsize=(20, 10))
positions = np.arange(len(item_counts)) * 1.5
bars = ax2.bar(positions, item_counts, align='center', color='red')
ax2.set_xticks(positions)
ax2.set_xticklabels(item_counts.index, rotation=90, ha='right')
ax2.set_xlabel('Item', fontsize=14)
ax2.set_ylabel('Jumlah', fontsize=14)
ax2.set_title('Diagram Batang Jumlah Per Item', fontsize=16)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
for bar in bars:
    ax2.annotate(str(bar.get_height()), (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                 ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
plt.tight_layout()
st.pyplot(fig2)

st.header("Conclusion")
st.write("""
- 16.1% Kategori Product yang memiliki review dibawah 3 dengan total 18109 item
- Kategori Produk yang memiliki review dibawah 3 paling banyak adalah bed_bath_table yang jumlah sebanyak 2112 item dan Kategori produk yang memiliki review dibawah 3 paling sedikit adalah fashion_childrens_clothes dan security_and_services denga jumlah 1 item
""")
