# Milestone Project 3 - Discord Clone
## Django Discord Clone
### Introduction
This is a simple version of Discord, a chat application that allows users to create rooms and chat with other users about specific topics. The application is built using Django and Python. The application is deployed on with AWS and can be accessed here ###.  

### Getting Started
To get started, you will need to create an account. Once you have created an account, you will be able to create a room and invite other users to join. You will also be able to join other rooms that have been created by other users.

### Clone
---
To clone this repository, you will need to have Git installed on your machine. Once you have Git installed, you can run the following command in your terminal:

* git clone https://github.com/wtcrowe4/discord
---
Then cd into the discord folder and run the following command to create a virtual environment:
* pip install virtualenv
* virtualenv *env-name*
* source *env-name*/bin/activate
---
Then install the requirements:
* pip install -r requirements.txt
---
Then run the following command to start the server:
* python manage.py runserver
---
You can now access the application on your local machine at localhost:8000.

### Technologies Used
* Python
* Django
* Django Templates
* HTML
* SCSS
* SQLite
* AWS

### Bugs
* Unable to deploy to AWS, it is currently not finding my wsgi.py file correctly. Error: `ModuleNotFoundError: No module named 'discord.wsgi'   
* Currently working on mobile responsiveness.



