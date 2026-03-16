import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='startUp analysis')
df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month

def load_investor_details(investor):
    st.title(investor)
    # 5 recent investment
    st.subheader('Most recent Investment')
    st.dataframe(df[df['investors'].str.contains(investor)].head()[['date','Startup','Vertical','city','round','amount']])

    col1,col2=st.columns(2)
    with col1:
        #biggest investment
        temp_df=df[df['investors'].str.contains(investor)].groupby('Startup')['amount'].sum().sort_values(ascending=False)
        st.subheader('Biggest Investment')
        fig,ax=plt.subplots()
        ax.bar(temp_df.index,temp_df.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        #sector investment
        temp_df1=df[df['investors'].str.contains(investor)].groupby('Vertical')['amount'].sum()
        st.subheader('sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(temp_df1,autopct='%0.1f%%',labels=temp_df1.index)
        st.pyplot(fig1)

    col1,col2=st.columns(2)
    with col1:
        #stage investment
        temp_df1 = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('stage investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(temp_df1, autopct='%0.1f%%', labels=temp_df1.index)
        st.pyplot(fig1)
    with col2:
        #city investment
        temp_df1 = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('city investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(temp_df1, autopct='%0.1f%%', labels=temp_df1.index)
        st.pyplot(fig1)

    #year by year investment
    st.subheader('Year by Year investment ')
    temp_df=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig1, ax1 = plt.subplots()
    ax1.plot(temp_df.index,temp_df.values)
    st.pyplot(fig1)

def load_startup_detail(startup):
    st.title(startup)
     #founders
    st.subheader('Founders')
    st.write('NA')

    #industry
    st.subheader('Industry')
    st.write(df[df['Startup'].str.contains(startup)]['Vertical'].unique())

    #subindustry
    st.subheader('Subindustry')
    st.write(df[df['Startup'].str.contains(startup)]['subvertical'].dropna().unique())

    #city
    st.subheader('City')
    st.write(df[df['Startup'].str.contains(startup)]['city'].unique())

    #staging round
    st.subheader('Staging round information')
    temp_df=df[df['Startup'].str.contains(startup)][['date', 'investors', 'round', 'amount']]
    st.dataframe(temp_df)

def load_overall_analysis():
    st.title('Overall Analysis')

    #total invested amount
    total=round(df['amount'].sum(),2)

    #maximum amount infused in a startup
    max_funding= df.groupby('Startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #average funding
    avg_funding = round(df.groupby('Startup')['amount'].sum().mean(),2)

    #total funded startups
    num_startups=df['Startup'].nunique()


    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total)+'cr')
    with col2:
        st.metric('Max', str(max_funding) + 'cr')
    with col3:
        st.metric('Avg', str(avg_funding) + 'cr')
    with col4:
        st.metric('Funded startups', num_startups)

    st.header('MoM graph')

    selected_option=st.selectbox('select type',['Total','count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()

    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['year'].astype('string') + '-' + temp_df['month'].astype('string')
    fig, ax = plt.subplots()
    ax.plot(temp_df['x_axis'],temp_df['amount'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)







#sidebar
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['overall Analysis','Startup','Investor'])

if option=='overall Analysis':
    load_overall_analysis()
elif option=='Startup':
    selected_startup=st.sidebar.selectbox('select startUp',sorted(df['Startup'].unique().tolist()))
    btn1=st.sidebar.button('find Startup details')
    if btn1:
        load_startup_detail(selected_startup)
else:
    selected_investor=st.sidebar.selectbox('select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('find Investor details')
    if btn2:
        load_investor_details(selected_investor)