import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG (UI SETUP)
# -----------------------------
st.set_page_config(
    page_title="Bio Data Dashboard",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🧬 Mutation Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

st.info("Upload any CSV file to analyze and visualize your data dynamically.")

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# -----------------------------
# MAIN APP
# -----------------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(df)

    # -----------------------------
    # DETECT COLUMN TYPES
    # -----------------------------
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    text_cols = df.select_dtypes(include=["object"]).columns

    st.subheader("Column Info")
    st.write("Numeric columns:", list(numeric_cols))
    st.write("Text columns:", list(text_cols))

    # -----------------------------
    # CASE 1: NUMERIC DATA EXISTS
    # -----------------------------
    if len(numeric_cols) > 0:

        st.subheader("📊 Numeric Analysis Mode")

        x_col = st.selectbox("X-axis (categorical/text)", df.columns)
        y_col = st.selectbox("Y-axis (numeric)", numeric_cols)

        # Clean numeric data
        df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
        df_clean = df.dropna(subset=[y_col])

        if df_clean.empty:
            st.warning("No valid numeric data found. Try another column.")
        else:

            # -----------------------------
            # BAR CHART
            # -----------------------------
            st.subheader("Bar Chart")

            width = max(8, len(df_clean[x_col]) * 0.6)
            fig, ax = plt.subplots(figsize=(width, 6))

            ax.bar(df_clean[x_col].astype(str), df_clean[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.tick_params(axis='x', rotation=45)

            plt.tight_layout()
            st.pyplot(fig)

            # -----------------------------
            # PIE CHART
            # -----------------------------
            st.subheader("Pie Chart")

            fig2, ax2 = plt.subplots(figsize=(8, 8))

            ax2.pie(
                df_clean[y_col],
                labels=df_clean[x_col].astype(str),
                autopct="%1.1f%%",
                textprops={'fontsize': 9}
            )

            st.pyplot(fig2)

            # -----------------------------
            # STATISTICS
            # -----------------------------
            st.subheader("Statistics")

            st.write("Total:", df_clean[y_col].sum())
            st.write("Average:", df_clean[y_col].mean())

            if df_clean[y_col].notna().sum() > 0:
                top_row = df_clean.loc[df_clean[y_col].idxmax()]
                st.write("Highest Value Row:", top_row[x_col])

    # -----------------------------
    # CASE 2: NO NUMERIC DATA
    # -----------------------------
    else:

        st.subheader("📊 Categorical Analysis Mode")

        col = st.selectbox("Select column for frequency analysis", text_cols)

        freq = df[col].value_counts()

        st.subheader("Frequency Table")
        st.write(freq)

        st.subheader("Frequency Chart")

        width = max(8, len(freq) * 0.6)
        fig, ax = plt.subplots(figsize=(width, 6))

        ax.bar(freq.index.astype(str), freq.values)
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        st.pyplot(fig)

    # -----------------------------
    # SEARCH FUNCTION
    # -----------------------------
    st.subheader("🔍 Search Data")

    search = st.text_input("Search value")

    if search:
        filtered = df[df.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(),
            axis=1
        )]
        st.write(filtered)

else:
    st.sidebar.info("Upload a CSV file to begin analysis.")