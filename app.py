# app.py

import streamlit as st
from retriever import retrieve

st.set_page_config(
    page_title="🩺 WHO Medical Context Retriever",
    page_icon="🧬",
)

st.title("🩺 WHO Medical Context Retriever")
st.markdown(
    """
    This is a minimal prototype Streamlit UI for testing the **semantic context retriever** built during the IIIT Gwalior Hacksagon Hackathon.

    The retriever matches your medical question to trusted WHO disease data using **PubMedBERT**, **FAISS**, and **SQLite**.
    """
)

# Input box
query = st.text_input(
    "Enter your medical question or symptoms:",
    placeholder="e.g. I have mild fever, cough and cold",
)

# Search button
if st.button("Search") or query:
    if not query.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("🔍 Searching trusted WHO database..."):
            results = retrieve(query, top_k=5, min_confidence=0.5)
            if results:
                st.success(f"✅ Found {len(results)} relevant matches.")
                for i, r in enumerate(results, start=1):
                    st.markdown(f"### 🔬 Result {i}: **{r['condition'].title()}**")
                    st.markdown(f"**Source:** `{r['source']}`")
                    st.markdown(f"**Confidence:** `{r['confidence']}`")
                    st.write(r['content'])
                    st.write("---")
            else:
                st.warning("❌ No relevant matches found. Please try different wording or symptoms.")
