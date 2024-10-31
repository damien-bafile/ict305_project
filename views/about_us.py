import streamlit as st
import os

# Define the details of the people
project_members = {
    "Tran Anh Huy PHAN": ["Introduction to the case", "Power point presentation", "Demo video script"],
    "Redwan Hossain": ["Visual / Graphic / Interactivity", "Story Telling"],
    "Eren Tanah Stannard": ["Data Analysis", "Data exploration and Discovery", "Document formatting and structure",
                            "Visualisations: bar, scatter, and line plots"],
    "Damien Bafile": ["Data set introduction", "Storyboard", "Website Framework",
                      "Website Integration Management (Git)", "Colour Styling"]
}

# Define the assets directory
assets_dir = "./assets/images"

# Create a Streamlit app to display the details
st.title("Project Team Details")

# Create two columns
col1, col2 = st.columns(2)

for i, (member, tasks) in enumerate(project_members.items()):
    if i % 2 == 0:
        col = col1
    else:
        col = col2

    with col:
        col.subheader(member)
        first_name = member.split()[0].lower()
        image_path = os.path.join(assets_dir, f"{first_name}.png")
        if os.path.isfile(image_path):
            col.image(image_path, caption=member)
        else:
            col.write("Image not found")
        col.write("Tasks Contributed:")
        for task in tasks:
            col.write(f"- {task}")