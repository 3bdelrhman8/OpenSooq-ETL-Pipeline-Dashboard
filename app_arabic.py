import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="OpenSooq Market Tracker", layout="wide")
st.title("Arabic Market Price Tracker (OpenSooq)")


engine = create_engine("mysql+pymysql://root:Ahmed258%23@localhost/arabic_market")
df = pd.read_sql_query("SELECT * FROM opensooq_iphones", engine)

import re # تأكد من إضافة هذا السطر في أعلى الملف مع باقي الواردات (imports)

# ... (الأسطر الأولى الخاصة بإعداد الصفحة وعنوانها) ...

engine = create_engine("mysql+pymysql://root:Ahmed258%23@localhost/arabic_market")
df = pd.read_sql_query("SELECT * FROM opensooq_iphones", engine)

# 1. إضافة كود الفلترة هنا (بعد السطر 10 مباشرة)
df_filtered = df[(df['Price_Cleaned'] >= 3000) & (df['Price_Cleaned'] <= 120000)].copy()

# 2. إضافة دالة استخراج الموديل
def extract_iphone_model(text):
    match = re.search(r'(1[1-7])', str(text))
    if match:
        return f"iPhone {match.group(1)}"
    return "Other"

df_filtered['Model'] = df_filtered['Product'].apply(extract_iphone_model)

# 3. تحديث حساب المؤشرات لاستخدام df_filtered (بدلاً من الأسطر 12، 13، 14 القديمة)
avg_price = df_filtered['Price_Cleaned'].mean()
min_price = df_filtered['Price_Cleaned'].min()
max_price = df_filtered['Price_Cleaned'].max()

# يمكنك بعد ذلك إكمال باقي الكود الخاص بعرض هذه المؤشرات (st.metric) والرسوم البيانية

avg_price = df['Price_Cleaned'].mean()
min_price = df['Price_Cleaned'].min()
max_price = df['Price_Cleaned'].max()

st.subheader("Market Metrics: iPhone (EGP)")
col1, col2, col3 = st.columns(3)
col1.metric("Average Market Price", f"{avg_price:,.0f} EGP")
col2.metric("Lowest Price", f"{min_price:,.0f} EGP")
col3.metric("Highest Price", f"{max_price:,.0f} EGP")

st.subheader("Extracted Market Data (MySQL)")
st.dataframe(df, use_container_width=True)

st.subheader("Top 5 Best Deals Right Now")
best_deals = df.sort_values(by='Price_Cleaned', ascending=True).head(5)
st.table(best_deals[['Product', 'Price_Cleaned', 'Date_Scraped']])