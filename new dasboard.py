import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the dashboard
st.title("📊 Interactive Data Dashboard")

# File uploader widget
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    
    # Display dataset preview and structure
    with st.expander("🔍 Dataset Overview"):
        st.subheader("Dataset Preview")
        st.dataframe(data.head(), use_container_width=True)

        st.subheader("Dataset Information")
        buffer = data.info(buf=None)
        st.text(buffer)

    # Display summary statistics
    with st.expander("📈 Summary Statistics"):
        st.write(data.describe(include="all"))
    
    # Sidebar options for interactivity
    st.sidebar.header("🔧 Filter Options")
    
    # Filter by numeric columns
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        st.sidebar.subheader("Filter by Numeric Columns")
        for col in numeric_columns:
            min_val, max_val = st.sidebar.slider(
                f"{col} Range",
                float(data[col].min()),
                float(data[col].max()),
                (float(data[col].min()), float(data[col].max()))
            )
            data = data[(data[col] >= min_val) & (data[col] <= max_val)]

    # Select columns for visualization
    st.subheader("📊 Select Columns for Visualization")
    column_to_visualize = st.selectbox("Single Column Visualization", data.columns, index=0)
    columns_to_visualize = st.multiselect("Select Multiple Columns for Analysis", data.columns)

    # Visualization Section
    if column_to_visualize:
        st.subheader(f"🔍 Visualization for {column_to_visualize}")
        if data[column_to_visualize].dtype in ['int64', 'float64']:
            st.line_chart(data[column_to_visualize])
        elif data[column_to_visualize].dtype == 'object':
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.countplot(x=data[column_to_visualize], ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    if columns_to_visualize:
        st.subheader("📊 Histogram for Selected Columns")
        for col in columns_to_visualize:
            if data[col].dtype in ['int64', 'float64']:
                fig, ax = plt.subplots()
                sns.histplot(data[col], kde=True, ax=ax)
                ax.set_title(f"Distribution of {col}")
                st.pyplot(fig)

    # Download filtered data
    st.subheader("⬇️ Download Filtered Dataset")
    st.download_button(
        label="Download Filtered CSV",
        data=data.to_csv(index=False).encode('utf-8'),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file to start!")

