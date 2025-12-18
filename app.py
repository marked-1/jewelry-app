import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup Page (Brand-Agnostic Jewelry Engine)
st.set_page_config(page_title="Jewelry SEO Automation", layout="wide")
st.title("💎 Jewelry Listing Generator")
st.write("Upload product images to generate brand-agnostic SEO titles and descriptions.")

# 2. API Configuration (Sidebar)
# Get your key at: https://aistudio.google.com/
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)

# 3. The Logic (Prompt Logic stored in memory)
# This uses your preferred formulas: [Brand] + [Style] + [Cut] + [Stone] + [Metal] + [Category]
SYSTEM_PROMPT = """
You are a Jewelry SEO Expert. Analyze the uploaded image(s). 
For each image, identify the item and generate a listing row in a Markdown table following these exact rules:

1. SEO TITLE FORMULA: [Brand Placeholder] + [Style/Period] + [Cut] + [Stone Variety] + [Metal Purity] + [Category].
2. HUMANE DESCRIPTION: Write a 'Humane' vibe paragraph (2 sentences) about a wearing moment, followed by a 'Fast-Sell' styling or gift tip.
3. TECHNICAL SPECS: List Metal, Stone Shape, and Gemstone Variety.

Include 2025 trending keywords: Quiet Luxury, Ethically Sourced, Sustainable, Stackable, Antique Revival.
Use provided charts (Stone Shape, Ring Types, Gemstone List) to ensure accuracy.
Return results only as a clean Markdown table.
"""

# 4. Multi-Image Upload (Batch Vision Logic)
uploaded_files = st.file_uploader("Choose jewelry images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Generate Listings"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar.")
        else:
            # Using the fast Flash model for zero-cost/high-efficiency batching
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            for uploaded_file in uploaded_files:
                img = Image.open(uploaded_file)
                st.image(img, width=300, caption=f"Analyzing: {uploaded_file.name}")
                
                with st.spinner(f'Processing {uploaded_file.name}...'):
                    # The vision prompt analyzes the image directly
                    response = model.generate_content([SYSTEM_PROMPT, img])
                    st.markdown(response.text)
                    st.divider()
