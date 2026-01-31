import streamlit as st
import pathlib

from backend.ai_engine import generate_response
from backend.prompts import (
    campaign_prompt,
    sales_prompt,
    lead_scoring_prompt
)

# ---------------- CSS LOADER (THIS WAS STEP 2) ----------------
def load_css():
    css_file = pathlib.Path(__file__).parent / "styles.css"
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



def render_ui():
    st.set_page_config("MarketMind", layout="wide")

    # LOAD CUSTOM CSS
    load_css()

    # ---------------- HEADER ----------------
    st.title("📊 MarketMind")
    st.caption("Generative AI–Powered Sales & Marketing Intelligence Platform")

    menu = st.sidebar.selectbox(
        "Select Intelligence Engine",
        [
            "Campaign Intelligence",
            "Sales Narrative",
            "Revenue Probability (Lead Scoring)"
        ]
    )

    # ---------------- CAMPAIGN INTELLIGENCE ----------------
    if menu == "Campaign Intelligence":
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("📢 Campaign Intelligence Engine")
        st.write("AI-powered marketing strategy generation.")

        product = st.text_area("Product Description")
        audience = st.text_area("Target Audience")
        platform = st.text_input("Marketing Platform")

        if st.button("Generate Campaign"):
            prompt = campaign_prompt(product, audience, platform)
            with st.spinner("Generating campaign strategy..."):
                result = generate_response(prompt)
            st.markdown(result)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- SALES NARRATIVE ----------------
    elif menu == "Sales Narrative":
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("🧾 Sales Narrative Engine")
        st.write("High-conversion sales messaging using AI.")

        product = st.text_input("Product Name")
        persona = st.text_area("Customer Persona")

        if st.button("Generate Sales Pitch"):
            prompt = sales_prompt(product, persona)
            with st.spinner("Generating sales narrative..."):
                result = generate_response(prompt)
            st.markdown(result)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- LEAD SCORING ----------------
    elif menu == "Revenue Probability (Lead Scoring)":
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("📈 Revenue Probability Engine")
        st.write("Predict lead conversion probability with AI.")

        name = st.text_input("Lead Name")
        budget = st.text_area("Budget")
        need = st.text_area("Business Need")
        urgency = st.text_area("Urgency")

        if st.button("Analyze Lead"):
            prompt = lead_scoring_prompt(name, budget, need, urgency)
            with st.spinner("Analyzing lead..."):
                result = generate_response(prompt)
            st.markdown(result)

        st.markdown('</div>', unsafe_allow_html=True)
