import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px

def toggle_details():
    st.session_state.show_details = not st.session_state.show_details

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.set_page_config(page_title="Survey Grove",
                   page_icon = '🌳',
                   layout="wide")

st.title("🌳 Survey Grove")
st.markdown("## Free Survey Analysis Tool")

st.markdown("""
Upload a CSV of survey responses (one row per participant, one column per question).  
""")

# --- Details and Instructions ---
if "show_details" not in st.session_state:
    st.session_state.show_details = False

clicked = st.button("Show / Hide Details", on_click=toggle_details)

if st.session_state.show_details:
    st.markdown("""
Directions:
1. Upload Survey Data, with Questions listed in each column (wide, not long)
2. Select 3 **attributes** (eg: Gender) that you want to analyze (you can always do more later)
3. Tag responses to your questions as **numeric** or **categorical**. This will determine the kind of analysis.
4. For categorical data, define **positive** responses.
5. Run the tool!

The tool will:
- Create visualizations of your questions
- Run **statistical testing** to see if there is a significant difference in your attribute groups (eg: "Do men rate a question significantly differently than women?")
- **Significance tests** are ANOVA or Chi²
""")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your survey CSV", type=["csv"], key="file_uploader")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.uploaded_file = uploaded_file

    st.success(f"✅ Loaded {df.shape[0]} responses and {df.shape[1]} columns.")
    with st.expander("Preview Data", expanded=False):
        st.dataframe(df.head())

    # --- Attribute selection ---
    st.header("Step 1: Identify Attributes")
    attrs = st.multiselect(
        "Select up to three attribute columns (for grouping)",
        options=df.columns.tolist(),
        max_selections=3,
        key="attr_select"
    )

    # --- Identify question columns ---
    st.header("Step 2: Identify Question Columns")
    question_cols = [c for c in df.columns if c not in attrs]
    st.write(f"Detected {len(question_cols)} potential question columns.")

    # --- Auto-detect types ---
    auto_types = {
        c: "numeric" if np.issubdtype(df[c].dropna().dtype, np.number) else "categorical"
        for c in question_cols
    }

    st.subheader("Question Type Overrides")
    q_types = {}
    for col in question_cols:
        q_types[col] = st.selectbox(
            f"Type of question '{col}'",
            ["categorical", "numeric","Do Not Analyze"],
            index=0 if auto_types[col] == "categorical" else 1,
            key=f"type_{col}"
        )

    # --- Define positive responses ---
    st.header("Step 3: Define Positive Responses (Categorical)")
    positive_map = {}
    for col in [c for c in question_cols if q_types[c] == "categorical"]:
        unique_vals = sorted(df[col].dropna().unique())
        pos_vals = st.multiselect(
            f"Select positive responses for '{col}'",
            options=unique_vals,
            key=f"pos_{col}"
        )
        positive_map[col] = pos_vals

    # --- Run Analysis ---
    st.header("Step 4: Run Analysis")
    col_run, col_reset = st.columns([1, 1])
    with col_run:
        run = st.button("🚀 Run Survey Analysis", use_container_width=True)
    with col_reset:
        st.button("🔄 Reset All", use_container_width=True, on_click=reset_app)

    if run:
        st.divider()
        for q in question_cols:
            qtype = q_types[q]
            if qtype == 'Do Not Analyze':
                continue
            q_title = q.replace("_"," ").title()
            st.markdown(f"## 🧩 Question: {q_title}")

            for attr in attrs:
                title = f"{q} cut by: {attr}".replace("_", " ").title()
                st.markdown(f"### 📊 {title}")

                if qtype == "numeric":
                    # --- Numeric Analysis ---
                    fig = px.box(df, x=attr, y=q, points="all", title=title)
                    st.plotly_chart(fig, use_container_width=True)

                    groups = [group[q].dropna() for _, group in df.groupby(attr)]
                    if len(groups) > 1 and all(len(g) > 1 for g in groups):
                        f_val, p_val = stats.f_oneway(*groups)
                        st.write(f"**ANOVA:** F = {f_val:.3f}, p = {p_val:.3g}")
                        if p_val < 0.05:
                            st.write(f"_A **p-value < 0.05** suggests there may be significant differences between groups_")
                        else:
                            st.write(f"_A **p-value > 0.05** suggests there may **not** be significant differences between groups_")
                    else:
                        st.info("Not enough groups or data for ANOVA.")

                elif qtype == "categorical":
                    # --- Convert to Positive / Not Positive ---
                    df["_positive_"] = df[q].isin(positive_map[q]).astype(int)

                    summary = df.groupby(attr)["_positive_"].mean().reset_index()
                    summary["_positive_"] *= 100
                    fig = px.bar(
                        summary,
                        x=attr,
                        y="_positive_",
                        title=f"Percent Positive for '{q_title}' by {attr.title()}",
                        labels={"_positive_": "% Positive"}
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Chi-square test
                    contingency = pd.crosstab(df[attr], df["_positive_"])
                    if contingency.shape[0] > 1:
                        chi2, p_val, dof, exp = stats.chi2_contingency(contingency)
                        st.write(f"**Chi² test:** χ² = {chi2:.3f}, p = {p_val:.3g}")
                        if p_val < 0.05:
                            st.write(f"_A **p-value < 0.05** suggests there may be significant differences between groups_")
                        else:
                            st.write(f"_A **p-value > 0.05** suggests there may **not** be significant differences between groups_")

                    else:
                        st.info("Not enough groups for Chi² test.")

                    df.drop(columns="_positive_", inplace=True)

            st.divider()

# --- Session reset ---
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if st.button("🔄 Reset App"):
    reset_app()

# --- credits & buy me a coffee ---
st.markdown("""
    <p style="
        font-size: 16px;
        color: #2B3A2F;
        margin-bottom: 8px;
    ">
        This app was created by Kevin Verhoff.  
        If you find this tool useful and would like to buy me a coffee, I’d appreciate it:
    </p>
""", unsafe_allow_html=True)

st.markdown("""
    <a href="https://www.buymeacoffee.com/wZyLoMV" target="_blank"
       style="
           display: inline-block;
           padding: 6px 14px;
           background-color: #ffdd00;
           color: #2B3A2F;
           text-align: center;
           border-radius: 6px;
           text-decoration: none;
           font-weight: 600;
           font-size: 14px;
           box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
           transition: all 0.2s ease-in-out;
       "
       onmouseover="this.style.backgroundColor='#ffcf00'"
       onmouseout="this.style.backgroundColor='#ffdd00'">
       ☕ Buy me a coffee
    </a>
""", unsafe_allow_html=True)