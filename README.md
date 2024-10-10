# ICT305 Machine Masters 🤖

## Unzipping the Environment

Just simply extract the project files from the supplied zip file into required destination.

## Cloning the environment

### 1. git command

Two option are available if the user is wanting to cloning from GitHub via the terminal.

1. the git command that is managed by the Software Freedom Conservancy.
2. the gh command provided by GitHub services.

```bash
git clone github.com/damien-bafile/ict305_project.git
```

or

```bash
gh repo clone damien-bafile/ict305_project
```

### 2. GUI github application

## Setup the environment

To setup the environment will all the necessary prerequisite packages we will use the following command while replacing `<ENV_NAME>` with  a suitable name for you requirements e.g. ICT305_project.

```bash
conda create --name <ENV_NAME> --file requirements.txt
```

## Activate the environment

Activating the environment that you just previously created simply just run `conda activate <ENV_NAME>` replacing with the prevoiusly supplied name.

## Running the Project and accessing the web application

To run the project

```bash
streamlit run streamlit_app.py
```

Once the application has been loaded it will display two serperate addresses

```bash
  Local URL: http://localhost:8501
  Network URL: http://192.168.0.118:8501
```

## Accessing the site

This website has been hosted on "<https://render.com>" web host service where users are able to access it using the "<https://ict305-project-2.onrender.com>". We are currently using the free tier of the web service which has a number of pro and cons attached to it such as:

### Pros

* Generous Free Tier that offers generous resources compared to some competitors, with the ability to host static websites, web services, and databases.
* Auto-Deploy from Git where we were able to connect our GitHub repositories and automatically deploy whenever we pushed an update, which is very convenient for version control and continuous deployment.
* Custom Domains: The free tier allows the use of custom domains, which many other free hosting services restrict or charge for.
* Easy to Use: The interface and deployment process are simple and user-friendly, making it easy to get projects up and running quickly.

### Cons

* Render.com unforatilly automaticily shuts down the site for inactivity. This means the free tier web application will go to sleep after 15 minutes of inactivity, which means users may experience a delay when the app is accessed again, as it takes a around up to a minute to "wake up.". This would have to be the biggest con with using the service.
* The limited bandwidth and storage that free tier comes with limited bandwidth and storage. Due the web applications limited scope this was acceptable for our needs.
* CPU and Memory are constrainted in the free tier and has limited CPU and memory resources, which can affect performance for larger applications or those with high traffic.
* Using the free tier there is no support for databases. As we are using an file based storage solution this doesn't apply.
* As Free-tier users do not have access to premium customer support, which can make it harder to resolve issues promptly.
