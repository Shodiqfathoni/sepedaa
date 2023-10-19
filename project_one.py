import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "casual_y": "sum",
        "registered_y":"sum",
        "cnt_y": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "casual_y": "casual",
        "registered_y": "registered",
        "cnt_y": "total"
    }, inplace=True)
        
    return daily_rent_df



#season
def create_season_df(df):
    season_df = df.groupby(by="season_x").cnt_y.sum().reset_index()
    season_df.rename(columns={
        "cnt_y": "total"
    }, inplace=True)
        
    return season_df

#hour
def create_hour_df(df):
    hour_df = df.groupby(by="hr").cnt_y.sum().reset_index()
    hour_df.rename(columns={
        "cnt_y": "total"
    }, inplace=True)
        
    return hour_df

#weekday
def create_weekday_df(df):
    weekday_df = df.groupby(by="weekday_x").cnt_y.sum().reset_index()
    weekday_df.rename(columns={
        "cnt_y": "total"
    }, inplace=True)
        
    return weekday_df

#workingday
def create_workingday_df(df):
    workingday_df = df.groupby(by="workingday_x").cnt_y.sum().reset_index()
    workingday_df.rename(columns={
        "cnt_y": "total"
    }, inplace=True)
        
    return workingday_df


all_df = pd.read_csv("all_pro1.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)


for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()

with st.sidebar:
     # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/Shodiqfathoni/sepedaa/main/%E2%80%94Pngtree%E2%80%94logo%20bike%20cycling%20mtb%20isolated_5209109.png")

     # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                 (all_df["dteday"] <= str(end_date))]


daily_rent_df = create_daily_rent_df(main_df)
season_df = create_season_df(main_df)
hour_df = create_hour_df(main_df)
weekday_df = create_weekday_df(main_df)
workingday_df = create_workingday_df(main_df)


st.header('bicycles rent dashboard :sparkles:')



st.subheader('Daily rent')

col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_rent_df['casual'].sum()
    st.metric("Total casual", value=total_casual)

with col2:
    total_registered = daily_rent_df['registered'].sum()
    st.metric("Total registered", value= total_registered)

with col3:
    total_casual_and_registered = daily_rent_df['total'].sum()
    st.metric("total casual and registered", value=total_casual_and_registered)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["total"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("total bicycles rent based on season")
#season
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="total", 
    y="season_x",
    data=season_df.sort_values(by="total", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("jumlah peminjaman sepeda tiap musim", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)





st.subheader("total bicycles rent based on hour")
 
#hour
fig, ax = plt.subplots(figsize=(20, 10))
colors =  ["#90CAF9" if x == hour_df["total"].max() else "#D3D3D3" for x in hour_df["total"]]
sns.barplot(
    y="total", 
    x="hr",
    data=hour_df.sort_values(by="total", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("hour 00:00-23:00", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
 
st.subheader("total bicycles rent based on day") 
#weekday
fig, ax = plt.subplots(figsize=(20, 10))
    
colors = ["#90CAF9", "#D3D3D3" , "#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3","#90CAF9"]
 
sns.barplot(
    y="total", 
    x="weekday_x",
    data=weekday_df.sort_values(by="total", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("weekday", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("total bicycles rent based on workingday")
#workingday
fig, ax = plt.subplots(figsize=(20, 10))
    
colors = ["#90CAF9","#D3D3D3"]
 
sns.barplot(
    y="total", 
    x="workingday_x",
    data=workingday_df.sort_values(by="total", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("workingday", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)