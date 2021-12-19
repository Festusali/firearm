# Firearm Tracer Backend

## Flask Backend For Tracing Firearm Crime

This tool enables security operatives or any other autorized personnell to trace firearm crime by searching through the data and comparing hashes of different firearms.


### Features
- Create firearm entry.
- Search firearm details.
- Get list of matching firearms.


### How to Use it
Follow below guide to get the server setup and running.

#### Installation
1. Clone the repo.
   Clone this repo and cd into the directory.
1. Create a virtual environment and activate it.
   Create python virtual environment using pip.
   In your terminal run `python -m venv venv`. This will crreate an isolated virtual environment for the purpose of running this flask app.
   If you're on windows, run `venv/scripts/activate`.
1. Intall the requirements.
   Once the virtual environment is created and activated, install all necessary packages required for the flask app to run by typing: `pip install -r requirements.txt`. Make sure you have active internet connection for this to run.

#### Start the Server
Now that everything is setup, we need to start the server. In the terminal, type: `$env:FLASK_APP = "firearm"`.
Then, startup the server by running: `flask run`.
If you followed all instructions properly, the server should now be up and running. To verify, visit: `http://127.0.0.1:5000/` on your web browser.


Hope you find it beneficial.
