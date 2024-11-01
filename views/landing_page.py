import streamlit as st
import pandas as pd

from forms.contact import contact_form


@st.dialog("Contact Me")
def show_contact_form():
    contact_form()


# TODO: Add some real text to the front page

l_margin, centre, r_margin = st.columns([0.1, 0.8, 0.1])

with centre:
    # --- HERO SECTION ---
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    with col1:
        st.image("./assets/images/Police-logo-240-2021.png", width=230)
    with col2:
        st.title("ICT305 - **Machine Masters** 🤖", anchor=False)
        if st.button("📩"):
            show_contact_form()

    # --- MORE INFO ---
    st.write("\n")
    st.write(
        """
        <H1>Case Summary</H1>
This website aims to enhance crime management by developing an interactive data visualization platform that provides accessible insights into crime trends and patterns across metropolitan and regional areas.  

    # --- EVEN MORE INFO ---
    st.write("\n")
    st.subheader("More Info", anchor=False)
    st.write("""
<H1>Problem Definition</H1>
Crime data is often presented in a static, dense format, making it difficult for key stakeholders – such as policymakers, law enforcement, and the public. Hence, the absence of a dynamic, user-friendly visualization tool that allows users to compare crime trends between metropolitan and regional areas, highlighting patterns and areas of concern in an actionable way. 

<H1>Goal</H1>
The primary goal of this project is to develop an easy-to-use, interactive website that visualizes crime data across both metropolitan and regional areas of Western Australia. 

<H1>Narrative</H1> 
This project focuses on creating an engaging narrative about how crime data visualization can empower stakeholders to take meaningful action to improve community safety. 

<H1>Target Audience</H1> 
The platform is designed to cater to a wide range of stakeholders, including Police officers and law enforcement agencies, Government agencies, Researchers and academics, Residents of Western Australia. 

<H1>Dataset Summary</H1> 
The project uses crime data from the Western Australia Police Force, covering the period from January 2007 to June 2024. 
""", unsafe_allow_html=True)
