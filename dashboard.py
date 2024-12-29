import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the dashboard
st.title("Interactive Data Dashboard")
# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
if uploaded_file is not None:
    st.subheader("Dataset Preview")
    st.write(data.head())
if uploaded_file is not None:
    st.subheader("Summary Statistics")
    st.write(data.describe())
if uploaded_file is not None:
    st.subheader("Select Columns to Visualize")
    
    # Single column selection
    column_to_visualize = st.selectbox("Select a column for visualization", data.columns)

    # Multiple column selection
    columns_to_visualize = st.multiselect("Select multiple columns for analysis", data.columns)
if uploaded_file is not None:
    if column_to_visualize:
        st.subheader("Visualization")
        
        # Line chart for numerical data
        if data[column_to_visualize].dtype in ['int64', 'float64']:
            st.line_chart(data[column_to_visualize])
        
        # Bar chart for categorical data
        elif data[column_to_visualize].dtype == 'object':
            chart_data = data[column_to_visualize].value_counts()
            st.bar_chart(chart_data)

    if columns_to_visualize:
        st.subheader("Histogram")
        for col in columns_to_visualize:
            if data[col].dtype in ['int64', 'float64']:
                fig, ax = plt.subplots()
                sns.histplot(data[col], kde=True, ax=ax)
                st.pyplot(fig)
if uploaded_file is not None:
    st.subheader("Download Dataset")
    
    # Button to download the dataset
    st.download_button(
        label="Download CSV",
        data=data.to_csv(index=False).encode('utf-8'),
        file_name="modified_data.csv",
        mime="text/csv"
    )
if uploaded_file is not None:
    st.sidebar.header("Filter Options")
    
    # Example: Filter rows by a numeric column
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        filter_column = st.sidebar.selectbox("Filter by column", numeric_columns)
        min_val, max_val = st.sidebar.slider("Range", float(data[filter_column].min()), float(data[filter_column].max()), (float(data[filter_column].min()), float(data[filter_column].max())))
        filtered_data = data[(data[filter_column] >= min_val) & (data[filter_column] <= max_val)]
        st.write(filtered_data)
