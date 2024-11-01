Deployment Manual

# Software Requirements

- Anaconda Distribution
- Python 3.9 - 3.12 (3.12 recommended)
- pip
    - Streamlit
    - Bokeh
    - Plotly Express
    - geoJSON
    - BeautifulSoup
    - openpyxl

# Unzipping the Environment

Extract the project files from the supplied zip file and place them into the required destination.

# Cloning the environment

## 1\. git command

Alliteratively the project may be cloned from our GitHub repository using the following commands.

git clone <https://github.com/damien-bafile/ict305_project.git>

or

gh repo clone damien-bafile/ict305_project

# Setup the environment

## Creating the environment

After unzipping or cloning the repository, it will be necessary to create an Anaconda Environment to install all the related packages for the project. For this project we developed using python 3.12 so we recommend using that. Installation maybe done with the following command.

conda create -n &lt;ENV_NAME&gt; python=3.12

Press Y to Proceed with installation.

## Activate the environment

To activate the environment that you just previously created, simply run replacing &lt;ENV_NAME&gt; with the previously supplied environment name.

conda activate &lt;ENV_NAME&gt;

Please enter the command to activate the environment.

cd ict305_project

## Installing the environment

To setup the environment will all the prerequisite packages we will use the following command while replacing &lt;ENV_NAME&gt; with a suitable name for your requirements e.g. ICT305_project

pip install -r requirements.txt

# Running the Project and accessing the web application

To run the project, enter the following command.

streamlit run streamlit_app.py

Once the application has been loaded, it will display two separate addresses.

Local URL: <http://localhost:8501Network> URL: http://\*.\*.\*.\*:8501

By default, the website will automatically load in your operating system's default browser. If this does not happen simply just paste the address URL into your browser address bar to access the site.

## Accessing the site

This website has been hosted on [share.streamlit.io](https://share.streamlit.io) web host service where users are able to access it using the " <https://ict305project-machine-masters.streamlit.app”>. As we are currently using the free tier of the web service the service is slow as the system's resources are limited.