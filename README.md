# OC-P9

This project is a web application built with Django that allows users to request and share reviews of books or articles.
Each user has access to a personalized feed displaying posts and reviews in reverse chronological order.
The application includes features such as user authentication, content management, and follow connections.

## Requirements

- Python3
- A recent web browser that supports :
    - HTML5
    - CSS3

## Setup

### 1. Clone the project repository

Open your terminal and clone the project repository using the following command:

    git clone https://github.com/QuentinSab/OC-P9.git

### 2. Create a virtual environment

Move in the project directory with :

	cd .\OC-P9\

To create a virtual environment for the API, use:

On Windows:

	python -m venv env

On macOS/Linux:

    python3 -m venv env

### 3. Activate the virtual environment

To activate the virtual environment, use:

On Windows:

    env\Scripts\activate

On macOS/Linux:

    source env/bin/activate

### 4. Install dependencies

With the virtual environment activated, install the required packages listed in requirements.txt using the following command:

    pip install -r requirements.txt

## Usage

### 1. Activate the virtual environment

If the virtual environment is not already activated, use this command in the project directory:

On Windows:

    env\Scripts\activate

On macOS/Linux:

    source env/bin/activate

### 2. Start the server

Move in the application directory with :

	cd .\webapp\

And launch the server with :

    python manage.py runserver

### 3. Open the web interface

On an internet browser, go to the address :

	http://127.0.0.1:8000

### 4. Test

The application includes four users for testing purposes.

An administrator user with access to the administration interface:

    Username : admin
    Password : admin

Three test users:

    Username : Utilisateur1
    Password : Motdepasse1

    Username : Utilisateur2
    Password : Motdepasse2

    Username : Utilisateur3
    Password : Motdepasse3

### 5. Administration interface

To access administration interface go to the following address :

    http://127.0.0.1:8000/admin/

And use the administrator credentials.