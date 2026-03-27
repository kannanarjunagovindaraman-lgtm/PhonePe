#= IMPORTING LIBRARIES /=#   

#Pandas Library
import pandas as pd
import requests
#MySQL and SQLAlchemy Libraries
from urllib.parse import quote
from sqlalchemy import create_engine

#Dashboard Libraries
import plotly.express as px
import streamlit as st

#Connection for SQLAlchemy
local_DB_URL="postgresql://postgres:admin@localhost:5432/Phonepe"
engine=create_engine(local_DB_URL)

#================================== /   DASHBOARD SETUP   / ================================#


st.set_page_config(
    page_title="Phonepe Pulse Data Visualization",
    page_icon="📊",
    layout="wide")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(#c1ade0,#f7f7f7);
ckground-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
title: 
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title(":blue[Phonepe Pulse Data Visualization]")


#Creating tabs
tab1, tab2 ,tab3, tab4, tab5= st.tabs(['**Transaction Analysis Across States and Districts**','**User Registration Analysis**','**Insurance Transactions Analysis**','**User Engagement and Growth Strategy**','**Insurance Penetration and Growth Potential Analysis**'])


# ===================================================       /      TRANSACTION TAB    /     ===================================================== #
with tab1:
    st.markdown('This tab has Top 10 Transaction data of every state, district and pincode.')

    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='tr_yr', index=0)
        tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='tr_qtr', index=0)
    with col2:
        tr_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='tr_state', index=36)
        

    #============== / OUTPUT / ==============#

    col3,col4,col5=st.columns(3)

    # -------------------------       /     All India Transaction        /        ------------------ #
    if tr_state == 'All':
        with col3:

        #Tables and toggle switches with bar plots
            st.markdown(":violet[**Top 10 States**]")
            query_tp1=f"""SELECT "State"  as State, 
                            SUM("Transacion_count") AS Transaction_count
                        FROM public.aggtransaction 
                        WHERE "Year" = '{tr_yr}' 
                        AND "Quarter" = '{tr_qtr}' 
                        GROUP BY "State" 
                        ORDER BY Transaction_count DESC 
                        LIMIT 10; """
            df_tp1=pd.read_sql(query_tp1,engine)
            df_tp1.index += 1
            st.dataframe(df_tp1)

            on_1 = st.toggle("Show plot",key='on_1')

        if on_1:
            fig1 = px.bar(df_tp1 , x = 'state', y ='transaction_count', color ='transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 states based on Transaction Count', 
                height = 600)
            st.plotly_chart(fig1)

            query_all=f"""SELECT "State"  as State, 
                            SUM("Transacion_count") AS Transaction_count
                        FROM public.aggtransaction 
                        WHERE "Year" = '{tr_yr}' 
                        AND "Quarter" = '{tr_qtr}' 
                        GROUP BY "State" 
                        ORDER BY Transaction_count DESC;
                        """
            df_all=pd.read_sql(query_all,engine)
            geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            geojson_data = requests.get(geojson_url).json()

            df_all['State'] = df_all['state'].str.strip().str.title()

            fig = px.choropleth(
            df_all,
            geojson=geojson_data,
            featureidkey='properties.ST_NM',
            locations='State',
            color='transaction_count',
            color_continuous_scale='Reds'
             )

            fig.update_geos(fitbounds="locations", visible=False, scope="asia")

            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp2=f"""SELECT "District", "Count" FROM public."aggTopTransaction"
            WHERE "Year"='{tr_yr}' AND "Pincode" ='' AND "Quarter" = '{tr_qtr}' ORDER BY "Count" DESC LIMIT 10;
"""
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_2 = st.toggle("Show plot",key='on_2')

        if on_2:
            fig2 = px.bar(df_tp2 , x = 'District', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col5:
            st.markdown(":violet[**Top 10 Pincodes performed well based on Quater of the year**]")
            query_tp3=f"""SELECT "Pincode", "Count" FROM public."aggTopTransaction"
            WHERE "Year"='{tr_yr}' AND "District" ='' AND "Quarter" = '{tr_qtr}' ORDER BY "Count" DESC LIMIT 10;
"""
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_3 = st.toggle("Show plot",key='on_3')

        if on_3:
            fig3 = px.bar(df_tp3 , x = 'Pincode', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 pincode performed well based on Quater of the year', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)


    # -------------------------       /     State wise Transaction        /        ------------------ #
    else: 

        with col3:

            #Tables and toggle switches with bar plots
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp2=f"""SELECT "District", "Count" FROM  public."aggTopTransaction"
            WHERE "Year"='{tr_yr}' AND "Pincode" ='' AND "Quarter" = '{tr_qtr}' AND "State" = '{tr_state}' 
            ORDER BY "Count" DESC LIMIT 10;"""
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_2 = st.toggle("Show plot",key='on_2')

        if on_2:
            fig2 = px.bar(df_tp2 , x = 'District', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col4:
            st.markdown(":violet[**Top 10 Pincodes performed well for the selected year and State**]")
            query_tp3=f"""SELECT "Pincode", "Count" FROM public."aggTopTransaction"
            WHERE "Year"='{tr_yr}' AND "District" ='' AND "State" = '{tr_state}'
			ORDER BY "Count" DESC LIMIT 10;"""
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_3 = st.toggle("Show plot",key='on_3')

        if on_3:
            fig3 = px.bar(df_tp3 , x = 'Pincode', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 Pincodes performed well for the selected year and State', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)


# ===================================================       /      USER TAB    /     ===================================================== #

with tab2:
    st.markdown('This tab has Top 10 User data of every state, district and pincode.')


    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        u_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='u_yr', index=0)
        u_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='u_qtr', index=0)
    with col2:
        u_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='u_state', index=36)

    
    #============== / OUTPUT / ==============#
    col3, col4, col5=st.columns(3)

    # -------------------------       /     All India Users        /        ------------------ #
    if u_state == 'All':

        #Tables and toggle switches with bar plots
        with col3:
            st.markdown(":violet[**Top 10 States**]")
            query_tp4=f"""SELECT "State", SUM("RegisteredCount") AS Registered_users 
                FROM public."aggMapUsers" WHERE "Year"='{u_yr}' AND "Quarter" = '{u_qtr}' GROUP BY "State"
				ORDER BY Registered_users DESC LIMIT 10;"""
            df_tp4=pd.read_sql(query_tp4,engine)
            df_tp4.index += 1
            st.dataframe(df_tp4)

            on_4 = st.toggle("Show plot",key='on_4')

        if on_4:
            fig4 = px.bar(df_tp4 , x = 'State', y ='registered_users', color ='registered_users', 
                color_continuous_scale = 'thermal', title = 'Top 10 states based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig4)

            query_all=f"""SELECT "State", SUM("RegisteredCount") AS Registered_users 
                FROM public."aggMapUsers" WHERE "Year"='{u_yr}' AND "Quarter" = '{u_qtr}' GROUP BY "State"
				ORDER BY Registered_users DESC ;
                        """
            df_all=pd.read_sql(query_all,engine)
            geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            geojson_data = requests.get(geojson_url).json()

            df_all['State'] = df_all['State'].str.strip().str.title()

            fig = px.choropleth(
            df_all,
            geojson=geojson_data,
            featureidkey='properties.ST_NM',
            locations='State',
            color='registered_users',
            color_continuous_scale='Reds'
             )

            fig.update_geos(fitbounds="locations", visible=False, scope="asia")

            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp5=f"""SELECT "District", "RegisteredCount" FROM  public."aggTopUsers"
                WHERE "Year"='{u_yr}' AND "Quarter" = '{u_qtr}' ORDER BY "RegisteredCount" DESC LIMIT 10;"""
            df_tp5=pd.read_sql(query_tp5,engine)
            df_tp5.index += 1
            st.dataframe(df_tp5)

            on_5 = st.toggle("Show plot",key='on_5')
        if on_5:
            fig5 = px.bar(df_tp5 , x = 'District', y ='RegisteredCount', color ='RegisteredCount', 
                color_continuous_scale = 'thermal', title = 'Top 10 District based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig5)
        
    # -------------------------       /     State wise Users        /        ------------------ #
    else:
        
        #Tables and toggle switches with bar plots
        with col3:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp5=f"""SELECT "District", "RegisteredCount" FROM  public."aggTopUsers"
                WHERE "Year"='{u_yr}' AND "District"!='' AND "Quarter" = '{u_qtr}' ORDER BY "RegisteredCount" DESC LIMIT 10;"""
            
            df_tp5=pd.read_sql(query_tp5,engine)
            df_tp5.index += 1
            st.dataframe(df_tp5)

            on_5 = st.toggle("Show plot",key='on_5')

        if on_5:
            fig5 = px.bar(df_tp5 , x = 'District', y ='RegisteredCount', color ='RegisteredCount', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts', 
                height = 600,)
            st.plotly_chart(fig5)

        with col4:
            st.markdown(":violet[**Top 10 Pincode**]")
            query_tp6=f"""SELECT "Pincode", "RegisteredCount" FROM  public."aggTopUsers"
                WHERE "Year"='{u_yr}' AND "Pincode"!='' AND "Quarter" = '{u_qtr}' ORDER BY "RegisteredCount" DESC LIMIT 10;"""
            df_tp6=pd.read_sql(query_tp6,engine)
            df_tp6.index += 1
            st.dataframe(df_tp6)

            on_6 = st.toggle("Show plot",key='on_6')

        if on_6:
            fig6 = px.bar(df_tp6 , x = 'Pincode', y ='RegisteredCount', color ='RegisteredCount', 
                color_continuous_scale = 'thermal', title = 'Top 10 pincodes based on User registration', 
                height = 600,)
            fig6.update_layout(xaxis_type='category')
            st.plotly_chart(fig6)

with tab3:
    st.markdown('This tab shows Top 10 Insurance data of every state, district and pincode.')

    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        Ir_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='Ir_yr', index=0)
        Ir_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='Ir_qtr', index=0)
    with col2:
        Ir_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='Ir_state', index=36)
        

    #============== / OUTPUT / ==============#

    col3,col4,col5=st.columns(3)

    # -------------------------       /     All India Transaction        /        ------------------ #
    if Ir_state == 'All':
        with col3:

        #Tables and toggle switches with bar plots
            st.markdown(":violet[**Top 10 States**]")
            query_tp1=f"""SELECT "State"  as State, 
                            SUM("Count") AS Transaction_count
                        FROM public."aggTopInsurance"  
                        WHERE "Year" = '{Ir_yr}' 
                        AND "Quarter" = '{Ir_qtr}' 
                        GROUP BY "State" 
                        ORDER BY Transaction_count DESC 
                        LIMIT 10; """
            df_tp1=pd.read_sql(query_tp1,engine)
            df_tp1.index += 1
            st.dataframe(df_tp1)

            on_7 = st.toggle("Show plot",key='on_7')

            query_all=f"""SELECT "State"  as State, 
                            SUM("Count") AS Transaction_count
                        FROM public."aggTopInsurance"  
                        WHERE "Year" = '{Ir_yr}' 
                        AND "Quarter" = '{Ir_qtr}' 
                        GROUP BY "State" 
                        ORDER BY Transaction_count DESC;
                        """
            df_all=pd.read_sql(query_all,engine)
            geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            geojson_data = requests.get(geojson_url).json()

            df_all['State'] = df_all['state'].str.strip().str.title()

            fig = px.choropleth(
            df_all,
            geojson=geojson_data,
            featureidkey='properties.ST_NM',
            locations='State',
            color='transaction_count',
            color_continuous_scale='Reds'
             )

            fig.update_geos(fitbounds="locations", visible=False, scope="asia")

            st.plotly_chart(fig, use_container_width=True)

        if on_7:
            fig1 = px.bar(df_tp1 , x = 'state', y ='transaction_count', color ='transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 states based on Transaction Count', 
                height = 600)
            st.plotly_chart(fig1)

        with col4:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp2=f"""SELECT "District", "Count" FROM public."aggTopInsurance"
            WHERE "Year"='{Ir_yr}' AND "Pincode" ='' AND "Quarter" = '{Ir_qtr}'  ORDER BY "Count" DESC LIMIT 10;
"""
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_8 = st.toggle("Show plot",key='on_8')

        if on_8:
            fig2 = px.bar(df_tp2 , x = 'District', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col5:
            st.markdown(":violet[**Top 10 Pincodes performed well based on Quater of the year**]")
            query_tp3=f"""SELECT "Pincode", "Count" FROM public."aggTopInsurance"
            WHERE "Year"='{Ir_yr}' AND "District" ='' AND "Quarter" = '{Ir_qtr}'  ORDER BY "Count" DESC LIMIT 10;
"""
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_9 = st.toggle("Show plot",key='on_9')

        if on_9:
            fig3 = px.bar(df_tp3 , x = 'Pincode', y ='transaction_count', color ='Quarter', 
                color_continuous_scale = 'thermal', title = 'Top 10 Pincodes performed well based on Quater of the year', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)


    # -------------------------       /     State wise Transaction        /        ------------------ #
    else: 

        with col3:

            #Tables and toggle switches with bar plots
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp2=f"""SELECT "District", "Count" FROM  public."aggTopInsurance"
            WHERE "Year"='{Ir_yr}' AND "Pincode" ='' AND "Quarter" = '{Ir_qtr}' AND "State" = '{Ir_state}' 
            ORDER BY "Count" DESC LIMIT 10;"""
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_10 = st.toggle("Show plot",key='on_10')

        if on_10:
            fig2 = px.bar(df_tp2 , x = 'District', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col4:
            st.markdown(":violet[**Top 10 Pincodes performed well based on Quater of the year**]")
            query_tp3=f"""SELECT "Pincode", "Count" FROM public."aggTopInsurance"
            WHERE "Year"='{Ir_yr}' AND "District" ='' AND "Quarter" = '{Ir_qtr}'  ORDER BY "Count" DESC LIMIT 10;"""
         
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_11 = st.toggle("Show plot",key='on_11')

        if on_11:
            fig3 = px.bar(df_tp3 , x = 'Pincode', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Top 10 Pincodes performed well based on Quater of the year', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)
with tab4:
    st.markdown('This tab shows User Engagement and Growth Strategy.')


    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='us_yr', index=0)
        us_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='us_qtr', index=0)
    with col2:
        us_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='us_state', index=36)

    
    #============== / OUTPUT / ==============#
    col3, col4, col5=st.columns(3)

    # -------------------------       /     All India Users        /        ------------------ #
    if us_state == 'All':

        #Tables and toggle switches with bar plots
        with col3:
            st.markdown(":violet[**Least 10 States**]")
            query_tp4=f"""SELECT "State" AS State, 
                    SUM("RegisteredCount") AS RegisteredCount, SUM("AppOpens") as AppOpens
                FROM public."aggMapUsers" WHERE "Year"='{us_yr}' AND "Quarter" = '{us_qtr}' GROUP BY "State"
				ORDER BY RegisteredCount,AppOpens LIMIT 10;"""
            df_tp4=pd.read_sql(query_tp4,engine)
            df_tp4.index += 1
            st.dataframe(df_tp4)

            on_12 = st.toggle("Show plot",key='on_12')

            

        if on_12:
            fig4 = px.bar(df_tp4 , x = 'state', y ='registeredcount', color ='appopens', 
                color_continuous_scale = 'thermal', title = 'Least 10 states based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig4)

            query_all=f"""SELECT "State" AS State, 
                    SUM("RegisteredCount") AS RegisteredCount, SUM("AppOpens") as AppOpens
                FROM public."aggMapUsers" WHERE "Year"='{us_yr}' AND "Quarter" = '{us_qtr}' GROUP BY "State"
				ORDER BY RegisteredCount,AppOpens ;
                        """
            df_all=pd.read_sql(query_all,engine)
            geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            geojson_data = requests.get(geojson_url).json()

            df_all['State'] = df_all['state'].str.strip().str.title()

            fig = px.choropleth(
            df_all,
            geojson=geojson_data,
            featureidkey='properties.ST_NM',
            locations='State',
            color='registeredcount',
            color_continuous_scale='Reds'
             )

            fig.update_geos(fitbounds="locations", visible=False, scope="asia")

            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown(":violet[**Least 10 Districts**]")
            query_tp5=f"""SELECT "District" AS District, 
                    SUM("RegisteredCount") AS RegisteredCount, SUM("AppOpens") as AppOpens
                FROM public."aggMapUsers" WHERE "Year"='{us_yr}' AND "Quarter" = '{us_qtr}' GROUP BY "District"
ORDER BY RegisteredCount,AppOpens LIMIT 10;"""
            df_tp5=pd.read_sql(query_tp5,engine)
            df_tp5.index += 1
            st.dataframe(df_tp5)

            on_13 = st.toggle("Show plot",key='on_13')
        if on_13:
            fig5 = px.bar(df_tp5 , x = 'district', y ='registeredcount', color ='appopens', 
                color_continuous_scale = 'thermal', title = 'Least 10 District based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig5)
        
    # -------------------------       /     State wise Users        /        ------------------ #
    else:
        
        #Tables and toggle switches with bar plots
        with col3:
            st.markdown(":violet[**Least 10 Districts**]")
            query_tp5=f"""SELECT "District" AS District, 
                    SUM("RegisteredCount") AS RegisteredCount, SUM("AppOpens") as AppOpens
                FROM public."aggMapUsers"
                WHERE "Year"='{us_yr}' AND "Quarter" = '{us_qtr}' GROUP BY District ORDER BY RegisteredCount LIMIT 10;"""
            
            df_tp5=pd.read_sql(query_tp5,engine)
            df_tp5.index += 1
            st.dataframe(df_tp5)

            on_13 = st.toggle("Show plot",key='on_13')

        if on_13:
            fig5 = px.bar(df_tp5 , x = 'district', y ='registeredcount', color ='appopens', 
                color_continuous_scale = 'thermal', title = 'Least 10 districts', 
                height = 600,)
            st.plotly_chart(fig5)

        with col4:
            st.markdown(":violet[**Top 10 District**]")
            query_tp6=f"""SELECT "District" AS District, 
                    SUM("RegisteredCount") AS RegisteredCount, SUM("AppOpens") as AppOpens
                FROM public."aggMapUsers"
                WHERE "Year"='{us_yr}' AND "Quarter" = '{us_qtr}' GROUP BY District ORDER BY RegisteredCount DESC LIMIT 10;"""
            df_tp6=pd.read_sql(query_tp6,engine)
            df_tp6.index += 1
            st.dataframe(df_tp6)

            on_14 = st.toggle("Show plot",key='on_14')

        if on_14:
            fig6 = px.bar(df_tp6 , x = 'district', y ='registeredcount', color ='appopens', 
                color_continuous_scale = 'thermal', title = 'Top 10 District based on User registration', 
                height = 600,)
            fig6.update_layout(xaxis_type='category')
            st.plotly_chart(fig6)
with tab5:
    st.markdown('This tab shows Insurance Penetration and Growth Potential Analysis.')

    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        Ip_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='Ip_yr', index=0)
        Ip_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='Ip_qtr', index=0)
    with col2:
        Ip_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='Ip_state', index=36)
        

    #============== / OUTPUT / ==============#

    col3,col4,col5=st.columns(3)

    # -------------------------       /     All India Transaction        /        ------------------ #
    if Ip_state == 'All':
        with col3:

        #Tables and toggle switches with bar plots
            st.markdown(":violet[**Least 10 States**]")
            query_tp1=f"""SELECT "state"  as State, 
                            SUM("insurance_count") AS Insurance_count,
							SUM("insurance_amount") AS Insurance_Amount
                        FROM public.agginsurance 
                        WHERE "year" = '{Ip_yr}' 
                        AND "quarter" = '{Ip_qtr}' 
                        GROUP BY "state" 
                        ORDER BY Insurance_count  
                        LIMIT 10;"""
            df_tp1=pd.read_sql(query_tp1,engine)
            df_tp1.index += 1
            st.dataframe(df_tp1)

            on_15 = st.toggle("Show plot",key='on_15')

        if on_15:
            fig1 = px.bar(df_tp1 , x = 'state', y ='insurance_count', color ='insurance_amount', 
                color_continuous_scale = 'thermal', title = 'Least 10 states based on Insurance Count - Action required to improve Insurance numbers', 
                height = 600)
            st.plotly_chart(fig1)

            query_all=f"""SELECT "state"  as State, 
                            SUM("insurance_count") AS Insurance_count,
							SUM("insurance_amount") AS Insurance_Amount
                        FROM public.agginsurance 
                        WHERE "year" = '{Ip_yr}' 
                        AND "quarter" = '{Ip_qtr}' 
                        GROUP BY "state" 
                        ORDER BY Insurance_count   ;
                        """
            df_all=pd.read_sql(query_all,engine)
            geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            geojson_data = requests.get(geojson_url).json()

            df_all['State'] = df_all['state'].str.strip().str.title()

            fig = px.choropleth(
            df_all,
            geojson=geojson_data,
            featureidkey='properties.ST_NM',
            locations='State',
            color='insurance_count',
            color_continuous_scale='Reds'
             )

            fig.update_geos(fitbounds="locations", visible=False, scope="asia")

            st.plotly_chart(fig, use_container_width=True)
        with col4:
            st.markdown(":violet[**Least 10 Districts**]")
            query_tp2=f"""SELECT "District" AS District, 
                    SUM("Count") AS Insurance_count, SUM("Amount") as Insurance_Amount
                FROM public."aggMapInsurance"
                WHERE "Year"='{Ip_yr}' AND "Quarter" = '{Ip_qtr}' GROUP BY District ORDER BY Insurance_count LIMIT 10;
"""
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_16 = st.toggle("Show plot",key='on_16')

        if on_16:
            fig2 = px.bar(df_tp2 , x = 'district', y ='insurance_count', color ='insurance_amount', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col5:
            st.markdown(":violet[**Least 5 state performed very low Insurance amount based on Quater of the year**]")
            query_tp3=f"""SELECT "state"  as state,"quarter", 
                    SUM("insurance_amount") AS Insurance_Amount
                FROM public.agginsurance 
                WHERE "year" = '{Ip_yr}' 
                GROUP BY "state","quarter"
                ORDER BY Insurance_Amount 
                LIMIT 5		 
"""
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_17 = st.toggle("Show plot",key='on_17')

        if on_17:
            fig3 = px.bar(df_tp3 , x = 'state', y ='insurance_amount', color ='quarter', 
                color_continuous_scale = 'thermal', title = 'Least 5 state performed very low Insurance amount based on Quater of the year', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)


    # -------------------------       /     State wise Transaction        /        ------------------ #
    else: 

        with col3:

            #Tables and toggle switches with bar plots
            st.markdown(":violet[**Least 10 Districts**]")
            query_tp3=f"""SELECT "District" AS District, 
                    SUM("Count") AS Insurance_count, SUM("Amount") as Insurance_Amount
                FROM public."aggMapInsurance"
                WHERE "Year"='{Ip_yr}' AND "Quarter" = '{Ip_qtr}' AND "State" = '{Ip_state}' GROUP BY District ORDER BY Insurance_count LIMIT 10;
"""
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)
            on_18 = st.toggle("Show plot",key='on_18')

        if on_18:
            fig2 = px.bar(df_tp2 , x = 'District', y ='Count', color ='Count', 
                color_continuous_scale = 'thermal', title = 'Least 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col4:
            st.markdown(":violet[**Least 5 District performed very low Insured amount for the selected year and State**]")
            query_tp3=f"""SELECT "District", "Quarter", SUM("Amount") as Amount FROM  public."aggMapInsurance"
            WHERE "Year"='{Ip_yr}' AND "State" = '{Ip_state}'
			group by "District", "Quarter"
            ORDER BY Amount LIMIT 5;"""
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_19 = st.toggle("Show plot",key='on_19')

        if on_19:
            fig3 = px.bar(df_tp3 , x = 'District', y ='amount', color ='Quarter', 
                color_continuous_scale = 'thermal', title = 'Least 5 District performed very low Insured amount for the selected year and State', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)
