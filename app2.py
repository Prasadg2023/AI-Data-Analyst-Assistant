import streamlit as st

import pandas as pd

from groq import Groq

import matplotlib.pyplot as plt

import os

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(

    page_title="AI Data Analyst Assistant",

    layout="wide"

)

# -----------------------------

# TITLE

# -----------------------------

st.title(" AI Data Analyst Assistant")

st.write("Upload dataset and get AI-powered insights using Groq LLM")

# -----------------------------

# GROQ API

# -----------------------------

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------

# FILE UPLOAD

# -----------------------------

uploaded_file = st.file_uploader(

    " Upload CSV File",

    type=["csv"]

)

# -----------------------------

# PROCESS DATASET

# -----------------------------

if uploaded_file is not None:

    # LOAD DATA

    df = pd.read_csv(uploaded_file)

    # -----------------------------

    # DATASET PREVIEW

    # -----------------------------

    st.subheader(" Dataset Preview")

    st.dataframe(df.head())

    # -----------------------------

    # MISSING VALUE HANDLING

    # -----------------------------

    st.subheader(" Handle Missing Values")

    missing_option = st.selectbox(

        "Select Missing Value Handling Method",

        ["None", "Drop Rows", "Fill Mean", "Fill Median", "Fill Mode"]

    )

    df_clean = df.copy()

    if missing_option == "Drop Rows":

        df_clean = df_clean.dropna()

    elif missing_option == "Fill Mean":

        df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))

    elif missing_option == "Fill Median":

        df_clean = df_clean.fillna(df_clean.median(numeric_only=True))

    elif missing_option == "Fill Mode":

        for col in df_clean.columns:

            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)

    # -----------------------------

    # CLEAN DATASET PREVIEW

    # -----------------------------

    st.subheader(" Cleaned Dataset (Non-Missing)")

    st.dataframe(df_clean.head())

    # -----------------------------

    # BASIC INFORMATION

    # -----------------------------

    st.subheader(" Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("Rows", df_clean.shape[0])

    with col2:

        st.metric("Columns", df_clean.shape[1])

    with col3:

        st.metric("Missing Values", int(df_clean.isnull().sum().sum()))

    # -----------------------------

    # SUMMARY FOR AI

    # -----------------------------

    shape_df = pd.DataFrame({

        "Metric": ["Rows", "Columns"],

        "Values": [df_clean.shape[0], df_clean.shape[1]]

    })

    column_info = pd.DataFrame({

        "Column Name": df_clean.columns,

        "Data Type": df_clean.dtypes.astype(str),

        "Missing Values": df_clean.isnull().sum().values,

        "Unique Values": [df_clean[col].nunique() for col in df_clean.columns]

    })

    numeric_df = df_clean.select_dtypes(include=['int64', 'float64'])

    missing_df = pd.DataFrame({

        "Column": df_clean.columns,

        "Missing Count": df_clean.isnull().sum().values,

        "Missing Percentage": (

            df_clean.isnull().sum().values / len(df_clean)

        ) * 100

    })

    summary = f"""

    Dataset Shape:

    {shape_df.to_string(index=False)}

    Column Information:

    {column_info.to_string(index=False)}

    Numerical Statistics:

    {numeric_df.describe().to_string() if not numeric_df.empty else 'No Numeric Columns'}

    Missing Values:

    {missing_df.to_string(index=False)}

    Sample Data:

    {df_clean.head().to_string()}

    """

    # -----------------------------

    # AI INSIGHTS

    # -----------------------------

    st.subheader(" AI Analysis")

    if st.button("Generate AI Insights"):

        with st.spinner("Analyzing dataset using AI..."):

            prompt = f"""

            You are a senior data analyst.

            Analyze this dataset summary carefully.

            Dataset Summary:

            {summary}

            Provide:

            1. Dataset overview

            2. Key insights

            3. Missing value analysis

            4. Business recommendations

            5. Suggested visualizations

            6. Important trends

            """

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[{"role": "user", "content": prompt}],

                temperature=0.5,

                max_tokens=1500

            )

            result = response.choices[0].message.content

            st.subheader(" AI Insights")

            st.write(result)

    # -----------------------------

    # VISUALIZATION DASHBOARD

    # -----------------------------

    st.subheader(" Data Visualization Dashboard")

    numeric_cols = df_clean.select_dtypes(include=['int64', 'float64']).columns

    cat_cols = df_clean.select_dtypes(include=['object']).columns

    if len(numeric_cols) > 1:

        col1, col2, col3 = st.columns(3)

        with col1:

            hist_col = st.selectbox("Histogram Column", numeric_cols)

        with col2:

            box_col = st.selectbox("Box Plot Column", numeric_cols)

        with col3:

            x_col = st.selectbox("Scatter X-axis", numeric_cols)

            y_col = st.selectbox("Scatter Y-axis", numeric_cols, key="y")

        if len(cat_cols) > 0:

            cat_col = st.selectbox("Bar Chart Category", cat_cols)

            bar_num_col = st.selectbox("Bar Chart Value", numeric_cols, key="bar")

        else:

            cat_col = None

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # Histogram

        axes[0, 0].hist(df_clean[hist_col].dropna())

        axes[0, 0].set_title(f"Histogram - {hist_col}")

        # Box Plot

        axes[0, 1].boxplot(df_clean[box_col].dropna())

        axes[0, 1].set_title(f"Box Plot - {box_col}")

        # Scatter

        axes[1, 0].scatter(df_clean[x_col], df_clean[y_col])

        axes[1, 0].set_title(f"{x_col} vs {y_col}")

        axes[1, 0].set_xlabel(x_col)

        axes[1, 0].set_ylabel(y_col)

        # Bar

        if cat_col is not None:

            bar_data = df_clean.groupby(cat_col)[bar_num_col].mean().sort_values(ascending=False).head(10)

            axes[1, 1].bar(bar_data.index.astype(str), bar_data.values)

            axes[1, 1].set_title(f"{bar_num_col} by {cat_col}")

            axes[1, 1].tick_params(axis='x', rotation=45)

        else:

            axes[1, 1].text(0.5, 0.5, "No Categorical Data", ha='center')

        plt.tight_layout()

        st.pyplot(fig)

    else:

        st.warning("Need at least 2 numeric columns.")

    # -----------------------------

    # CATEGORICAL VISUALIZATION

    # -----------------------------

    st.subheader(" Categorical Data Visualization")

    if len(cat_cols) > 0:

        cat_vis_col = st.selectbox("Select Categorical Column", cat_cols, key="cat_vis")

        value_counts = df_clean[cat_vis_col].value_counts().head(10)

        fig_cat, ax_cat = plt.subplots()

        ax_cat.bar(value_counts.index.astype(str), value_counts.values)

        ax_cat.set_title(f"Top Categories in {cat_vis_col}")

        ax_cat.set_xlabel(cat_vis_col)

        ax_cat.set_ylabel("Count")

        plt.xticks(rotation=45)

        st.pyplot(fig_cat)

    else:

        st.warning("No categorical columns available.")

    # -----------------------------

    # CHAT WITH DATASET

    # -----------------------------

    st.subheader(" Chat With Dataset")

    user_question = st.text_input("Enter your question")

    if st.button("Get Answer"):

        if user_question.strip() != "":

            with st.spinner("Generating answer..."):

                question_prompt = f"""

                You are an expert data analyst.

                Dataset Summary:

                {summary}

                User Question:

                {user_question}

                Give a clear and detailed answer.

                """

                response = client.chat.completions.create(

                    model="llama-3.3-70b-versatile",

                    messages=[{"role": "user", "content": question_prompt}],

                    temperature=0.3,

                    max_tokens=1000

                )

                answer = response.choices[0].message.content

                st.subheader(" Answer")

                st.write(answer)

        else:

            st.warning("Please enter a question.")