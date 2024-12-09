import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_excel("Amazon Sales data.xlsx")

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['days_taken'] = (df['Ship Date'] - df['Order Date'])/ np.timedelta64(1, 'D')

df.drop(columns=['Order ID'],inplace=True)


df_yr = df.copy()
df_yr['ord_year'] = df_yr['Order Date'].dt.year
df_yr['ord_month'] = df_yr['Order Date'].dt.month
df_yr['ord_weekday'] = df_yr['Order Date'].dt.dayofweek # monday =0, sunday=6

latest_yr = df_yr[((df_yr['ord_year'] == 2017) | ((df_yr['ord_year'] == 2016) & (df_yr['ord_month'] > 5)))]
prev_yr = df_yr[((df_yr['ord_year'] == 2015) & (df_yr['ord_month'] > 5)) | ((df_yr['ord_year'] == 2016) & (df_yr['ord_month'] <= 5))]

st.set_page_config(page_title='Sales Analysis Dashboard', layout='wide', page_icon='📈')

st.title("Amazon Sales Analysis Dashboard!")
st.write("This dashboard summarizes sales analysis over years, months and year-month.")

st.markdown("<hr style='border: 2px solid #ccc;'>", unsafe_allow_html=True)
st.subheader('Metrics')


# KPIs
total_rev = df_yr[df_yr['ord_year'] == 2017]['Total Revenue'].sum()
total_profit = df_yr[df_yr['ord_year'] == 2017]['Total Profit'].sum()
total_prdts = df_yr[df_yr['ord_year'] == 2017]['Units Sold'].sum()

col1, col2, col3 = st.columns(3)
with col1:
 st.metric(label="Total Revenue 💵 in 2017", value=total_rev, delta=10, delta_color="normal")
  
with col2:
    st.metric(label="Total Profit 💰 in 2017", value=total_profit, delta=10, delta_color="normal")

with col3:
    st.metric(label="Total Units Sold 📦 in 2017", value=total_prdts, delta=10, delta_color="normal")
    
st.markdown("<hr style='border: 0.5px solid #ccc;'>", unsafe_allow_html=True)

option = st.sidebar.selectbox("Select an Option", ["Year", "Month", "Month-Year"])

if option == 'Year':
    
    latest_profit = latest_yr.groupby('ord_month')['Total Profit'].sum().reset_index()
    prev_profit = prev_yr.groupby('ord_month')['Total Profit'].sum().reset_index()
    
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(prev_profit['ord_month'], prev_profit['Total Profit'], label='2015-16', color='lime', ls='--')
    plt.plot(latest_profit['ord_month'], latest_profit['Total Profit'], label='2016-17', color='green')
    plt.title('Previous Year vs Current Year - Monthly Total Profit')
    plt.xlabel('Month')
    plt.ylabel('Total Profit Sum')
    plt.legend()
    
    latest_prdts = latest_yr.groupby('ord_month')['Units Sold'].sum().reset_index()
    prev_prdts = prev_yr.groupby('ord_month')['Units Sold'].sum().reset_index()

    plt.subplot(1,2,2)
    plt.plot(prev_prdts['ord_month'], prev_prdts['Units Sold'], label='2015-16', color='plum', ls='--')
    plt.plot(latest_prdts['ord_month'], latest_prdts['Units Sold'], label='2016-17', color='orchid')
    plt.title('Previous Year vs Current Year - Monthly Units Sold')
    plt.xlabel('Month')
    plt.ylabel('Total Units Sold')
    plt.legend()
    st.pyplot(plt)

    fig1, fig2, fig3= st.columns(3)

    with fig1:
        st.subheader('Top Item Types based on Total Profit in 2016-17')
        st.write(latest_yr.groupby('Item Type')['Total Profit'].sum().sort_values(ascending=False).head(3))
        
        st.subheader('Top Item Types based on Units Sold in 2016-17')
        st.write(latest_yr.groupby('Item Type')['Units Sold'].sum().sort_values(ascending=False).head(3))
        
    with fig2:
        st.subheader('Top 3 profitable Region and Country based on 2016-17 sales')
        st.write(latest_yr.groupby('Region')['Total Profit'].sum().sort_values(ascending=False).head(3))
        st.write(latest_yr.groupby('Country')['Total Profit'].sum().sort_values(ascending=False).head(3))
        
    with fig3:
        st.subheader('Least Profitable Item Types in 2016-17')
        st.write(prev_yr.groupby('Item Type')['Total Profit'].sum().sort_values(ascending=False).head(3))
        
        
if option == 'Month':
    
    monthly_profit = df_yr.groupby('ord_month')['Total Profit'].sum().reset_index()
        
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(monthly_profit['ord_month'], monthly_profit['Total Profit'], color='chocolate', marker='o')
    plt.title('Total Profit by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Profit Sum')
        
    monthly_rev = df_yr.groupby('ord_month')['Units Sold'].sum().reset_index()
    
    plt.subplot(1,2,2)
    plt.plot(monthly_rev['ord_month'], monthly_rev['Units Sold'], color='gold', marker='o')
    plt.title('Total Units Sold by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Units Sold')
    st.pyplot(plt)
        
    fig1, fig2 = st.columns(2)
        
    with fig1:
        top_prdts_month = df_yr.loc[df_yr.groupby('ord_month')['Units Sold'].idxmax()]
        st.subheader('Top Products by Units Sold')
        top_prdts_month[['ord_month', 'Item Type', 'Units Sold']]
        
    with fig2:
       top_profit_month = df_yr.loc[df_yr.groupby('ord_month')['Total Profit'].idxmax()]
       st.subheader('Top Products by Total Profit')
       top_profit_month[['ord_month', 'Item Type', 'Total Profit']]

if option == "Month-Year":
    mnth_yr = df_yr.groupby(['ord_year', 'ord_month'])['Total Profit'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='ord_month', y='Total Profit', hue='ord_year', data=mnth_yr, palette='Set2')
    plt.title('Total Profit by Month and Year (Grouped Bar Chart)')
    plt.xlabel('Month')
    plt.ylabel('Total Profit')
    plt.xticks()  # Ensure the x-axis shows all months
    plt.legend(title='Year')
    plt.grid(True, axis='x')
    st.pyplot(plt)
    
    
