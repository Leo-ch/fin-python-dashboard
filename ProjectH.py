# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import plotly.express as px
import streamlit as st


# To run the app:
# (1) Change the cd to C:\Users\chaul\AppData\Local\Programs\Python\Python311\Scripts\Project H
# (2) run the command jupytext --to py ProjectH.ipynb
# (3) run the comment streamlit run ProjectH.py

df = pd.concat( [pd.read_excel('Project_H_data.xlsx',sheet_name='Europe'),
                pd.read_excel('Project_H_data.xlsx',sheet_name='Asia'),
                pd.read_excel('Project_H_data.xlsx',sheet_name='Middle East and North Africa'),
                pd.read_excel('Project_H_data.xlsx',sheet_name='North America'),
                pd.read_excel('Project_H_data.xlsx',sheet_name='Latin America')
                ])
df=df.melt(id_vars=['Category','Item','Geography'])
df[['Month','Division']]=df['variable'].str.split('_',expand=True)
df.drop(columns='variable',inplace=True)
df=df[df['Division']!='Total']
df['Division']=df['Division'].replace({'CC':'Corporate Center'})
df['Month'] = pd.to_datetime(df['Month'])
df['Year']=df['Month'].dt.year.astype(str)
df['Quarter_index']=df['Month'].dt.month/3
df['Quarter']="Q"+df['Quarter_index'].astype(int).astype(str)

st.set_page_config(page_title='Financial Dashboard',
                   page_icon='HSBC_logo.png',
                   layout="wide")

st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.header('Filter Pannel')
st.sidebar.text(" \n")
st.sidebar.text(" \n")
div = st.sidebar.multiselect(
    'Select the division:',
    options=df['Division'].unique(),
    default=df['Division'].unique()
)
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
geo = st.sidebar.multiselect(
    'Select the geo:',
    options=df['Geography'].unique(),
    default=df['Geography'].unique()
)

df_selection = df.query("Division == @div & Geography == @geo")


st.title("Financial Dashboard")
st.text("in US$'m unless specified")
st.markdown('---')

NII = df_selection.loc[(df_selection['Item']=='Net interest income/(expense)') & (df_selection['Year']=='2019'),'value'].sum()
NII_d = (df_selection.loc[(df_selection['Item']=='Net interest income/(expense)') & (df_selection['Year']=='2019'),'value'].sum() \
/df_selection.loc[(df_selection['Item']=='Net interest income/(expense)') & (df_selection['Year']=='2018'),'value'].sum()-1)*100

G1 = pd.DataFrame(df_selection.loc[df_selection['Item']=='Net interest income/(expense)'].groupby(by=['Year'])['value'].sum())

NPT = df_selection.loc[(df_selection['Item']=='Profit/(loss) before tax') & (df_selection['Year']=='2019'),'value'].sum()
NPT_d = (df_selection.loc[(df_selection['Item']=='Profit/(loss) before tax') & (df_selection['Year']=='2019'),'value'].sum() \
/df_selection.loc[(df_selection['Item']=='Profit/(loss) before tax') & (df_selection['Year']=='2018'),'value'].sum()-1)*100


G2 = pd.DataFrame(df_selection.loc[df_selection['Item']=='Profit/(loss) before tax'].groupby(by=['Year'])['value'].sum())


CER = 100*abs(df_selection.loc[(df_selection['Item']=='Total operating expenses') & (df_selection['Year']=='2019'),'value'].sum() / df_selection.loc[(df_selection['Item']=='Net operating income before change in expected credit losses and other credit impairment charges') & (df_selection['Year']=='2019'),'value'].sum())
CER_d = CER - 100*abs(df_selection.loc[(df_selection['Item']=='Total operating expenses') & (df_selection['Year']=='2018'),'value'].sum() / df_selection.loc[(df_selection['Item']=='Net operating income before change in expected credit losses and other credit impairment charges') & (df_selection['Year']=='2018'),'value'].sum())

G3 = pd.DataFrame(df_selection.loc[df_selection['Item']=='Total operating expenses'].groupby(by=['Year'])['value'].sum())
G4 = pd.DataFrame(df_selection.loc[df_selection['Item']=='Net operating income before change in expected credit losses and other credit impairment charges'].groupby(by=['Year'])['value'].sum())
G5 = pd.concat([G3,G4],axis=1)
G5.columns=['TOE','NI']
G5['CER']=abs(G5['TOE']/G5['NI'])

G6= pd.DataFrame(df_selection.loc[(df_selection['Item']=='Net interest income/(expense)') & (df_selection['Year']=='2019')].groupby(by=['Division'])['value'].sum().sort_values(ascending=False))
G6['color']=G6['value']
G6['color'].iloc[0]='#D7282F'
G6['color'].iloc[1:]='#BCBEC0'



G7 = pd.DataFrame(df_selection.loc[(df_selection['Item']=='Net interest income/(expense)') & (df_selection['Year']=='2019')].groupby(by=['Geography'])['value'].sum().sort_values(ascending=False))
G7['color']=G7['value']
G7['color'].iloc[0]='#D7282F'
G7['color'].iloc[1:]='#BCBEC0'



G8= pd.DataFrame(df_selection.loc[(df_selection['Item']=='Profit/(loss) before tax') & (df_selection['Year']=='2019')].groupby(by=['Division'])['value'].sum().sort_values(ascending=False))
G8['color']=G8['value']
G8['color'].iloc[0]='#D7282F'
G8['color'].iloc[1:]='#BCBEC0'



G9 = pd.DataFrame(df_selection.loc[(df_selection['Item']=='Profit/(loss) before tax') & (df_selection['Year']=='2019')].groupby(by=['Geography'])['value'].sum().sort_values(ascending=False))
G9['color']=G9['value']
G9['color'].iloc[0]='#D7282F'
G9['color'].iloc[1:]='#BCBEC0'


G10 = pd.DataFrame(df_selection.loc[(df_selection['Item']=='Total operating expenses') &  (df_selection['Year']=='2019')].groupby(by=['Division'])['value'].sum())
G11 = pd.DataFrame(df_selection.loc[(df_selection['Item']=='Net operating income before change in expected credit losses and other credit impairment charges') &  (df_selection['Year']=='2019')].groupby(by=['Division'])['value'].sum())
G12 = pd.concat([G10,G11],axis=1)
G12.columns=['TOE','NI']
G12['CER']=abs(G12['TOE']/G12['NI'])
G12.sort_values(by=['CER'],ascending=True,inplace=True)
G12['color']=G12['CER']
G12['color'].iloc[0]='#D7282F'
G12['color'].iloc[1:]='#BCBEC0'


G13 = pd.DataFrame(df_selection.loc[(df_selection['Item']=='Total operating expenses') &  (df_selection['Year']=='2019')].groupby(by=['Geography'])['value'].sum())
G14 = pd.DataFrame(df_selection.loc[(df_selection['Item']=='Net operating income before change in expected credit losses and other credit impairment charges') &  (df_selection['Year']=='2019')].groupby(by=['Geography'])['value'].sum())
G15 = pd.concat([G13,G14],axis=1)
G15.columns=['TOE','NI']
G15['CER']=abs(G15['TOE']/G15['NI'])
G15.sort_values(by=['CER'],ascending=True,inplace=True)
G15['color']=G15['CER']
G15['color'].iloc[0]='#D7282F'
G15['color'].iloc[1:]='#BCBEC0'

Graph1 = px.bar(
    G1,
    x=G1.index,
    y='value',
    orientation='v',
    template='plotly_white',
    width=250, height=180,
    text_auto=',',
    color=G1.index,
    color_discrete_sequence=['#BCBEC0','#BCBEC0','#BCBEC0','#D7282F']
)


Graph2 = px.bar(
    G2,
    x=G2.index,
    y='value',
    orientation='v',
    template='plotly_white',
    width=250, height=180,
    text_auto=',',
    color=G2.index,
    color_discrete_sequence=['#BCBEC0','#BCBEC0','#BCBEC0','#D7282F']
)
Graph3 = px.bar(
    G5,
    x=G5.index,
    y='CER',
    orientation='v',
    template='plotly_white',
    width=250, height=180,
    text_auto='.0%',
    color=G3.index,
    color_discrete_sequence=['#BCBEC0','#BCBEC0','#BCBEC0','#D7282F']
)
Graph4 = px.bar(
    G6,
    x='value',
    y=G6.index,
    orientation='h',
    template='plotly_white',
    text_auto=',',
    color = 'color',
    color_discrete_map="identity"
)
Graph5 = px.bar(
    G7,
    x='value',
    y=G7.index,
    orientation='h',
    template='plotly_white',
    text_auto=',',
    color = 'color',
    color_discrete_map="identity"
)

Graph6 = px.bar(
    G8,
    x='value',
    y=G8.index,
    orientation='h',
    template='plotly_white',
    text_auto=',',
    color = 'color',
    color_discrete_map="identity"
)

Graph7 = px.bar(
    G9,
    x='value',
    y=G9.index,
    orientation='h',
    template='plotly_white',
    text_auto=',',
    color = 'color',
    color_discrete_map="identity"
)


Graph8 = px.bar(
    G12,
    x='CER',
    y=G12.index,
    orientation='h',
    template='plotly_white',
    text_auto='.0%',
    color = 'color',
    color_discrete_map="identity"
)


Graph9 = px.bar(
    G15,
    x='CER',
    y=G15.index,
    orientation='h',
    template='plotly_white',
    text_auto='.0%',
    color = 'color',
    color_discrete_map="identity"
)

Graph1.update_yaxes(showgrid=False,visible=False)
Graph2.update_yaxes(showgrid=False,visible=False)
Graph3.update_yaxes(showgrid=False,visible=False)
Graph1.update_layout(xaxis_title=None,showlegend=False)
Graph2.update_layout(xaxis_title=None,showlegend=False)
Graph3.update_layout(xaxis_title=None,showlegend=False)

Graph1.update_traces(textfont_size=13, textangle=0, textposition="outside", cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph2.update_traces(textfont_size=13, textangle=0, textposition="outside", cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph3.update_traces(textfont_size=13, textangle=0, textposition="outside", cliponaxis=False,hovertemplate = None,hoverinfo = "skip")

Graph4.update_layout(yaxis={'categoryorder': 'total ascending'},xaxis_title=None,yaxis_title=None,xaxis_tickformat = '#,',showlegend=False)
Graph5.update_layout(yaxis={'categoryorder': 'total ascending'},xaxis_title=None,yaxis_title=None,xaxis_tickformat = '#,',showlegend=False)
Graph6.update_layout(yaxis={'categoryorder': 'total ascending'},xaxis_title=None,yaxis_title=None,xaxis_tickformat = '#,',showlegend=False)
Graph7.update_layout(yaxis={'categoryorder': 'total ascending'},xaxis_title=None,yaxis_title=None,xaxis_tickformat = '#,',showlegend=False)
Graph8.update_layout(yaxis={'categoryorder': 'total descending'},xaxis_title=None,yaxis_title=None,xaxis_tickformat = '0%',showlegend=False)
Graph9.update_layout(yaxis={'categoryorder': 'total descending'},xaxis_title=None,yaxis_title=None,xaxis_tickformat = '0%',showlegend=False)

Graph4.update_traces(textfont_size=13, textangle=0, cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph5.update_traces(textfont_size=13, textangle=0, cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph6.update_traces(textfont_size=13, textangle=0, cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph7.update_traces(textfont_size=13, textangle=0, cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph8.update_traces(textfont_size=13, textangle=0, cliponaxis=False,hovertemplate = None,hoverinfo = "skip")
Graph9.update_traces(textfont_size=13, textangle=0, cliponaxis=False,hovertemplate = None,hoverinfo = "skip")


if (len(div) == 0) or (len(geo)==0):
    st.warning('Please select at least one option for divion and geo.')
else:
    left_col, middle_col, right_col = st.columns(3)

    with left_col:
        st.subheader("Net Interest Income")
        st.header(f"{NII:,.0f}")
        st.text("YoY:⠀"+f"{NII_d:.0f}%")
        st.plotly_chart(Graph1)
    with middle_col:
        st.subheader("Net Profit before Tax")
        st.header(f"{NPT:,.0f}")
        st.text("YoY:⠀"+f"{NPT_d:.0f}%")
        st.plotly_chart(Graph2)
    with right_col:
        st.subheader("Cost Efficiency Ratio")
        st.header(f"{CER:.0f}%")
        st.text("YoY:⠀"+f"{CER_d:.0f}ppt")
        st.plotly_chart(Graph3)
    st.markdown("---")

    left_col2, right_col2 = st.columns(2)
    with left_col2:
        st.subheader("Net Interest Income by Division")
        st.plotly_chart(Graph4)
    with right_col2:
        st.subheader("Net Interest Income by Geo")
        st.plotly_chart(Graph5)
    st.markdown("---")
    left_col2, right_col2 = st.columns(2)
    with left_col2:
        st.subheader("Net Profit before Tax by Division")
        st.plotly_chart(Graph6)
    with right_col2:
        st.subheader("Net Profit before Tax by Geo")
        st.plotly_chart(Graph7)

    st.markdown("---")
    left_col2, right_col2 = st.columns(2)

    with left_col2:
        st.subheader("Cost Efficiency Ratio by Division")
        st.plotly_chart(Graph8)
    with right_col2:
        st.subheader("Cost Efficiency Ratio by Geo")
        st.plotly_chart(Graph9)



hide_st_style ="""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)