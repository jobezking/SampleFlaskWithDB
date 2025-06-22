# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

# --- Flask Application Initialization ---
app = Flask(__name__)
# Set a secret key for flashing messages (important for production)
app.secret_key = 'your_super_secret_key_here' # IMPORTANT: Change this to a strong, random key in production!

# --- Database Configuration ---
# In a real-world application, these credentials should be loaded from
# environment variables (e.g., using python-dotenv) or a secure configuration system.
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password' # IMPORTANT: Use a strong password and manage it securely!
DB_NAME = 'flask_app_db'

# --- Database Connection Helper ---
def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor # Returns rows as dictionaries
        )
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        flash(f"Database connection error: {e}", 'error')
        return None

# --- Routes ---

@app.route('/')
def index():
    """
    Displays a list of all items from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return render_template('index.html', items=[]) # Render with empty list if no connection

    items = []
    try:
        with conn.cursor() as cursor:
            # SQL query to select all items
            cursor.execute("SELECT id, name FROM items ORDER BY id DESC")
            items = cursor.fetchall() # Fetch all results
    except pymysql.Error as e:
        flash(f"Error retrieving items: {e}", 'error')
        print(f"Error retrieving items: {e}")
    finally:
        conn.close() # Always close the connection

    return render_template('index.html', items=items)

@app.route('/add', methods=('GET', 'POST'))
def add_item():
    """
    Handles adding new items to the database.
    GET: Displays the form to add an item.
    POST: Processes the form submission and inserts the item.
    """
    if request.method == 'POST':
        item_name = request.form['name']

        if not item_name:
            flash('Name is required!', 'error')
            return redirect(url_for('add_item')) # Redirect back to the form

        conn = get_db_connection()
        if conn is None:
            return redirect(url_for('index')) # Redirect to home if no connection

        try:
            with conn.cursor() as cursor:
                # SQL query to insert a new item
                cursor.execute("INSERT INTO items (name) VALUES (%s)", (item_name,))
            conn.commit() # Commit the transaction to save changes
            flash(f'Item "{item_name}" added successfully!', 'success')
            return redirect(url_for('index')) # Redirect to the home page after adding
        except pymysql.Error as e:
            flash(f"Error adding item: {e}", 'error')
            print(f"Error adding item: {e}")
            conn.rollback() # Rollback on error
        finally:
            conn.close()

    return render_template('add_item.html')

@app.route('/edit/<int:item_id>', methods=('GET', 'POST'))
def edit_item(item_id):
    """
    Handles editing existing items in the database.
    GET: Displays the form to edit an item with pre-filled data.
    POST: Processes the form submission and updates the item.
    """
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('index'))

    item = None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone() # Fetch a single row
    except pymysql.Error as e:
        flash(f"Error retrieving item for edit: {e}", 'error')
        print(f"Error retrieving item for edit: {e}")
    finally:
        conn.close()

    if item is None:
        flash('Item not found!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        item_name = request.form['name']

        if not item_name:
            flash('Name is required!', 'error')
            # Stay on the edit page with the current item data
            return render_template('edit_item.html', item=item)

        conn = get_db_connection() # Re-establish connection for POST request
        if conn is None:
            return redirect(url_for('index'))

        try:
            with conn.cursor() as cursor:
                # SQL query to update an existing item
                cursor.execute("UPDATE items SET name = %s WHERE id = %s", (item_name, item_id))
            conn.commit()
            flash(f'Item "{item_name}" updated successfully!', 'success')
            return redirect(url_for('index'))
        except pymysql.Error as e:
            flash(f"Error updating item: {e}", 'error')
            print(f"Error updating item: {e}")
            conn.rollback()
        finally:
            conn.close()

    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=('POST',))
def delete_item(item_id):
    """
    Handles deleting an item from the database.
    This route only accepts POST requests for security reasons.
    """
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('index'))

    try:
        with conn.cursor() as cursor:
            # SQL query to delete an item
            cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        conn.commit()
        flash('Item deleted successfully!', 'success')
    except pymysql.Error as e:
        flash(f"Error deleting item: {e}", 'error')
        print(f"Error deleting item: {e}")
        conn.rollback()
    finally:
        conn.close()

    return redirect(url_for('index'))

# --- Error Handling (Basic) ---
@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 error page."""
    return render_template('404.html'), 404

# --- Main entry point for the Flask application ---
if __name__ == '__main__':
    # When running locally, set host to '0.0.0.0' to be accessible from other machines
    # on the network, or '127.0.0.1' (localhost) for local access only.
    # debug=True automatically reloads the server on code changes and provides a debugger.
    # NEVER use debug=True in a production environment.
    app.run(debug=True, host='0.0.0.0', port=5000)

