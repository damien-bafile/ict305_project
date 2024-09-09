import streamlit as st
import re
import csv
import os


# Improved email validation regex
def is_valid_email(email):
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return email_pattern.match(email) is not None


# Function to append message to CSV
def append_message_to_csv(name, email, message):
    file_exists = os.path.isfile("messages.csv")

    # Open the file in append mode
    with open("./output/messages.csv", "a", newline="") as csvfile:
        fieldnames = ["Name", "Email", "Message"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is new
        if not file_exists:
            writer.writeheader()

        # Write the message
        writer.writerow({"Name": name, "Email": email, "Message": message})


def contact_form():
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email Address")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("Submit")

        # Ensure no field is empty
        if submit_button:
            errors = []

            if not name:
                errors.append("Please enter your 🧍 name.")

            if not email:
                errors.append("Please enter your 📧 email address.")
            elif not is_valid_email(email):
                errors.append("Invalid email address")

            if not message:
                errors.append("Please enter a 🗯️ message.")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                append_message_to_csv(name, email, message)
                st.success("📤 Message successfully sent!!!")
