import streamlit as st
import pandas as pd
import io
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('ggplot')


st.sidebar.image("./logo.png", width=100)
st.sidebar.header("Hi👋 my name is Mirac")
st.sidebar.write("This application was created for you to gain a quick insight about your data. I hope you enjoy using 😄")

st.header("Welcome my streamlit app 👋")
st.text("This app provide exploratory data analysis on your own dataset")

st.markdown("### Please upload your file or choose local file")
file_format = st.radio('Select file format:', ('csv', 'excel'), key='file_format')
uploaded_file = st.file_uploader("", type=["csv", "excel"])
local_file = st.checkbox("If you wish use local dataset")

if uploaded_file:
    file = uploaded_file
    st.info("Your dataset successfully loaded 🎉")
if local_file:
    file = "./ds_salaries.csv"
    st.info("Local dataset loaded. This dataset is about Data Scientist salaries. 😄")

if not (uploaded_file or local_file):
    file = None

st.sidebar.header("Data Visualization Options")
if file:
    if file_format == "csv":
        df = pd.read_csv(file)
    if file_format == "excel":
        df = pd.read_excel(file)
    
    all_cols = df.columns.to_list()
    cat_cols = df.select_dtypes(include="object").columns.to_list()
    num_cols = df.select_dtypes(exclude="object").columns.to_list()
    
    sel_cat_cols = cat_cols.copy()
    sel_cat_cols.insert(0, '<select>')
    sel_num_cols = num_cols.copy()
    sel_num_cols.insert(0, '<select>')

    st.markdown("## Overview of the Dataset")
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        opt_1 = st.checkbox("Dataset Shape")
        opt_2 = st.checkbox("Dataset Info")
    with col_2:
        opt_3 = st.checkbox("Describe Dataset")
        opt_4 = st.checkbox("Draw Pair Plot")
    with col_3:
        opt_5 = st.checkbox("Correlation Heat Map")
        opt_6 = st.checkbox("Make Crosstap ")
    
    if opt_1:
        st.text(f"Number of Features: {df.shape[0]}\nNumber of Instances: {df.shape[1]}")
    if opt_2:
        # Data Info
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
    if opt_3:
        st.write(df.describe().T)
    if opt_4:
        cols = st.multiselect("Select Columns", options=num_cols, default=num_cols[:3])
        color = st.selectbox("Select column for Color / Hue:", options=cat_cols)
        fig = sns.pairplot(data=df, vars=cols, hue=color)
        st.pyplot(fig)

    if opt_5:
        corr_cols = st.multiselect("Select columns for creating Correlation Matrix", options=num_cols)
        if corr_cols:
            fig = plt.figure(figsize=(10, 7))
            cmap = sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)
            sns.heatmap(df[corr_cols].corr(), annot=True, cmap=cmap)
            st.pyplot(fig.figure)
    if opt_6:
        sel_1 = st.selectbox("Select Index", options=cat_cols)
        sel_2 = st.selectbox("Select Column", options=cat_cols)
        visualize = st.checkbox("Check if you want to visualize crosstab in HeatMap")
        if sel_1 and sel_2:
            if sel_1 != "<select>" and sel_2 != "<select>":
                ct = pd.crosstab(index=df.loc[:,sel_1], columns=df.loc[:, sel_2])
                if visualize:
                    fig = plt.figure(figsize=(15, 10))
                    sns.heatmap(ct, annot=True, fmt="d", cmap="tab10")
                    st.pyplot(fig)
                else:
                    st.table(ct)
    st.sidebar.markdown("### Count Plot")
    count_plot_check = st.sidebar.checkbox("Draw CountPlot")
    if count_plot_check:
        plt.figure(figsize=(10, 15))
        sel_col = st.sidebar.selectbox("Select Column", options=cat_cols)
        fig = sns.countplot(data=df,
                            y=sel_col,
                            order=df[sel_col].value_counts().iloc[:15].index)
        plt.grid(axis="x")
        plt.title("Count Plot")
        st.pyplot(fig.figure)

    st.sidebar.markdown("### Line Chart")
    line_chart_check = st.sidebar.checkbox("Draw LineChart")
    if line_chart_check:
        plt.figure(figsize=(12, 7))
        x_axis = st.sidebar.selectbox("Select x-axis", options=num_cols)
        y_axis = st.sidebar.selectbox("Select y-axis", options=num_cols)
        hue = st.sidebar.selectbox("Select Hue", options=sel_cat_cols)
        if hue != '<select>':
            fig = sns.lineplot(data=df, x=x_axis, y=y_axis, hue=hue)
        else:
            fig = sns.lineplot(data=df, x=x_axis, y=y_axis)
        plt.title("Line Chart")
        st.pyplot(fig.figure)

    
    st.sidebar.markdown("### Scatter Plot")
    scatter_plot_check = st.sidebar.checkbox("Draw Scatter Plot")
    if scatter_plot_check:
        plt.figure(figsize=(10, 7))
        x_axis_scat = st.sidebar.selectbox("Select x-axis", options=num_cols)
        y_axis_scat = st.sidebar.selectbox("Select y-axis", options=num_cols)
        hue_scat = st.sidebar.selectbox("Select Hue", options=sel_cat_cols)
        if hue_scat != '<select>':
            fig_scat = sns.scatterplot(data=df, x=x_axis_scat, y=y_axis_scat, hue=hue_scat)
        else:
            fig_scat = sns.scatterplot(data=df, x=x_axis_scat, y=y_axis_scat)
        plt.title("Scatter Plot")
        st.pyplot(fig_scat.figure)

    st.sidebar.markdown("### Pie Chart")
    st.sidebar.markdown("| It is the same as Count Plot, the only difference is that the first 5 values are taken and their ratios are displayed.")
    pie_chart_check = st.sidebar.checkbox("Draw Pie Chart")
    if pie_chart_check:
        fig = plt.figure(figsize=(12, 6))
        col = st.sidebar.selectbox("Select Column", options=cat_cols)        
        data = df[col].value_counts()[:5]
        plt.pie(data, labels=data.index, autopct='%2.2f%%')
        st.pyplot(fig.figure)
