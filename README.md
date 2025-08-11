# Ticket-Management-System

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:Aayam1o1/Ticket-Management-System.git
$ cd ticket-management-system
```

Create a virtual environment using conda, activate it and install dependencies using poetry:

```sh
$ conda create --name <env> python=3.11
$ conda activate <env>
```

Then install the dependencies:

```sh
(env)$ poetry install
```

Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `conda`.

Once `poetry` has finished downloading the dependencies:

```sh

(env)$ cd project
Please create a database for named ticket through psql or pgadmin.
(env)$ python manage.py migrate
(env)$ python datascript.py

(env)$ python manage.py runserver
```

Create a .env file and add all the necessary environment variable.
And navigate to `http://127.0.0.1:8000/admin/`.

## Features

- Roles and Permissions
- Menu Creation and Assign
- Ticket Creation and Assign

Note: The admin panel can be accessed by two users: 
username: superuser
password: superpass1234

username: admin
password: pass1234

The permissions are set as:
admin: Can do everything mentioned in the permission model.
supervisor: Create, edit and view (ticket and menu) and Assign the menu and tickets.
agent: Can Create and view ticket
normal: Can view ticket.
