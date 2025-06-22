# **Simple Python Flask Application with MariaDB Backend**

This repository contains a basic Flask web application that demonstrates how to integrate Flask with a MariaDB database for basic CRUD (Create, Read, Update, Delete) operations. It includes instructions for setting up your environment, database, and deploying the application.

## **Table of Contents**

* [Description](#bookmark=id.4o8p9oyf8k8a)  
* [Features](#bookmark=id.5g905yvki31a)  
* [Prerequisites](#bookmark=id.xi87jvwwu6m1)  
* [Database Setup](#bookmark=id.rx7n7w6vn34j)  
* [Installation](#bookmark=id.gysimz5drll0)  
* [Configuration](#bookmark=id.785n5hvkrpq6)  
* [Running the Application](#bookmark=id.h8eo3260a6s4)  
* [Accessing the Application](#bookmark=id.7c4rcw3gsw8e)  
* [Usage](#bookmark=id.ct0j08r52u7d)  
* [Deployment (Basic)](#bookmark=id.dr8ahqosvawd)  
* [Contributing](#bookmark=id.4dmdrg5we1cu)  
* [License](#bookmark=id.xjeosnhbhdqw)

## **Description**

This is a minimal Flask application that allows you to manage a simple list of "items." It interacts with a MariaDB database to store, retrieve, update, and delete these items. The application provides web interfaces for these operations.

## **Features**

* **List Items:** View all stored items on the home page (/).  
* **Add Item:** Add new items via a dedicated form (/add).  
* **Edit Item:** Modify existing items using an edit form (/edit/\<item\_id\>).  
* **Delete Item:** Remove items from the database (/delete/\<item\_id\>).  
* **MariaDB Integration:** Demonstrates basic database connection and SQL operations using PyMySQL.  
* **Basic UI:** Simple HTML templates with Tailwind CSS for a clean look.

## **Prerequisites**

Before you begin, ensure you have the following installed and configured on your system:

* **Python 3.x:** Download from [python.org](https://www.python.org/).  
* **pip:** Python's package installer (usually comes with Python).  
* **MariaDB Server:** Install MariaDB (or MySQL, which is largely compatible) on your local machine or have access to a remote MariaDB instance.  
  * **MariaDB Installation Guides:**  
    * [MariaDB on macOS (Homebrew)](https://mariadb.com/docs/deploy/install/mm_install/macos/homebrew/)  
    * [MariaDB on Linux (Ubuntu)](https://mariadb.com/docs/deploy/install/mm_install/linux/ubuntu/)  
    * [MariaDB on Windows](https://mariadb.com/docs/deploy/install/mm_install/windows/)  
* **Database User:** Ensure you have a MariaDB user with permissions to create databases and tables (e.g., root user or a dedicated application user).

## **Database Setup**

1. **Start your MariaDB server.**  
2. **Access the MariaDB command-line client or a GUI tool (e.g., DBeaver, MySQL Workbench):**  
   mysql \-u root \-p  
   \# Enter your MariaDB root password when prompted

3. **Create the database and table using the provided schema.sql:**  
   \# From within the MariaDB client:  
   SOURCE /path/to/your/flask\_app\_repo/schema.sql;

   * Alternatively, you can manually run the commands from schema.sql:  
     CREATE DATABASE IF NOT EXISTS flask\_app\_db;  
     USE flask\_app\_db;  
     CREATE TABLE IF NOT EXISTS items (  
         id INT AUTO\_INCREMENT PRIMARY KEY,  
         name VARCHAR(255) NOT NULL,  
         created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP  
     );

## **Installation**

Follow these steps to set up the Flask application:

1. **Clone the repository:**  
   git clone https://github.com/your-username/your-repo-name.git  
   cd your-repo-name

   * *(Note: If you're creating these files locally, just create the app.py, requirements.txt, schema.sql files, and the templates directory with its HTML files in a new directory.)*  
2. **Create a Virtual Environment (Recommended):**  
   python3 \-m venv venv

3. **Activate the Virtual Environment:**  
   * **On macOS/Linux:**  
     source venv/bin/activate

   * **On Windows (Command Prompt):**  
     venv\\Scripts\\activate.bat

   * **On Windows (PowerShell):**  
     .\\venv\\Scripts\\Activate.ps1

4. Install Dependencies:  
   Install Flask and PyMySQL using pip:  
   pip install \-r requirements.txt

## **Configuration**

Open app.py and locate the \--- Database Configuration \--- section.

\# app.py  
\# ...  
DB\_HOST \= 'localhost'  
DB\_USER \= 'root'  
DB\_PASSWORD \= 'password' \# IMPORTANT: Change this\!  
DB\_NAME \= 'flask\_app\_db'  
\# ...  
app.secret\_key \= 'your\_super\_secret\_key\_here' \# IMPORTANT: Change this\!

* **DB\_HOST**: The hostname or IP address of your MariaDB server.  
* **DB\_USER**: Your MariaDB username.  
* **DB\_PASSWORD**: Your MariaDB password. **Strongly recommend changing this default value.**  
* **DB\_NAME**: The name of the database you created (default is flask\_app\_db).  
* **app.secret\_key**: This is crucial for session management and flashing messages. **Change your\_super\_secret\_key\_here to a long, random, and unique string for production environments.**

## **Running the Application**

Ensure your virtual environment is active and your MariaDB server is running.

python app.py

You should see output similar to this, indicating the development server is running:

 \* Serving Flask app 'app'  
 \* Debug mode: on  
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.  
 \* Running on http://0.0.0.0:5000  
Press CTRL+C to quit  
 \* Restarting with stat  
 \* Debugger is active\!  
 \* Debugger PIN: XXX-XXX-XXX

## **Accessing the Application**

Open your web browser and navigate to the following URL:

* **Home Page:** http://127.0.0.1:5000/ or http://localhost:5000/

## **Usage**

* **View Items:** Upon visiting http://127.0.0.1:5000/, you will see a list of items currently in your database.  
* **Add New Item:** Click the "Add New Item" button or navigate to http://127.0.0.1:5000/add. Fill in the item name and click "Add Item".  
* **Edit Item:** On the home page, click the "Edit" button next to an item. You will be taken to an edit form pre-filled with the item's current name. Make changes and click "Update Item".  
* **Delete Item:** On the home page, click the "Delete" button next to an item. You will be prompted for confirmation before the item is removed.

## **Deployment (Basic)**

For production environments, the Flask development server is not suitable due to its limitations and lack of security features. You would typically use a production-ready WSGI (Web Server Gateway Interface) server like [Gunicorn](https://gunicorn.org/) or [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

A very basic production setup with Gunicorn would look something like this (after activating your virtual environment and installing gunicorn with pip install gunicorn):

gunicorn \-w 4 app:app \-b 0.0.0.0:5000

* \-w 4: Runs 4 worker processes (adjust based on your server's CPU cores).  
* app:app: Specifies that Gunicorn should run the app instance from the app.py file.  
* \-b 0.0.0.0:5000: Binds the server to all network interfaces on port 5000\.

Database in Production:  
In a production deployment, your MariaDB instance would likely be on a separate, dedicated server or a managed database service (e.g., Google Cloud SQL, AWS RDS, Azure Database for MariaDB). You would update the DB\_HOST in app.py (preferably via environment variables) to point to your production database server.  
For more robust deployment, consider using Nginx as a reverse proxy in front of Gunicorn, and deploying on platforms like Heroku, AWS Elastic Beanstalk, Google Cloud Run, Docker containers, or Kubernetes.

## **Contributing**

Feel free to fork this repository, open issues, or submit pull requests if you have suggestions or improvements\!

## **License**

This project is licensed under the MIT License \- see the LICENSE file (if applicable) for details.