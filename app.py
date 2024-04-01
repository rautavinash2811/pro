from flask import Flask, request, render_template, jsonify
import psycopg2

app = Flask(__name__)

# Database connection details
DB_NAME = 'IMCA'
DB_USER = 'postgres'
DB_PASSWORD = 'avi123'
DB_HOST = 'localhost'

# Function to establish database connection
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Route to render the index.html template (home page)
@app.route('/')
def index():
    return render_template('menu.html')

# Route to render the order_details.html template
@app.route('/order_details')
def order_details():
    return render_template('order_details.html')

# Route to render the about.html template
@app.route('/about')
def about():
    return render_template('about.html')

# Route to render the menu.html template
@app.route('/menu')
def menu():
    return render_template("index.html")

# Route to handle order submission
@app.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        # Extract order data from the request
        order_data = request.form.to_dict()
        
        # Connect to the database
        conn = connect_to_db()
        if conn:
            try:
                # Open a cursor to perform database operations
                cur = conn.cursor()
                
                # Insert the order data into the database
                for item_name, quantity in order_data.items():
                    cur.execute("INSERT INTO orders (item_name, quantity) VALUES (%s, %s)",
                                (item_name, int(quantity)))
                
                # Commit the transaction
                conn.commit()
                
                # Close communication with the database
                cur.close()
                conn.close()
                
                return jsonify({'message': 'Order submitted successfully'})
            except psycopg2.Error as e:
                print("Error executing SQL statement:", e)
                conn.rollback()
                cur.close()
                conn.close()
                return jsonify({'error': 'Failed to store order data'})
        else:
            return jsonify({'error': 'Failed to connect to the database'})
    else:
        return jsonify({'error': 'Invalid request method'})

if __name__ == '__main__':
    app.run(debug=True)
