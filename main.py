
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Database configuration
connection = sqlite3.connect('expenses.db')
cursor = connection.cursor()

# Home route
@app.route('/')
def home():
    # Get all expenses from the database
    expenses = cursor.execute("SELECT * FROM expenses").fetchall()

    # Render the home page with the list of expenses
    return render_template('index.html', expenses=expenses)

# Add expense route
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Get form data
        date = request.form['date']
        type = request.form['type']
        amount = request.form['amount']
        description = request.form['description']

        # Validate form data
        if not date or not type or not amount or not description:
            return render_template('add_expense.html', error="All fields are required")

        # Save expense to database
        cursor.execute("INSERT INTO expenses (date, type, amount, description) VALUES (?, ?, ?, ?)", (date, type, amount, description))
        connection.commit()

        # Redirect to home page
        return redirect(url_for('home'))

    # Render add expense page
    return render_template('add_expense.html')

# Reports route
@app.route('/reports')
def reports():
    return render_template('reports.html')

# Generate report route
@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Get filter criteria from form data
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    type = request.form['type']

    # Generate report based on filter criteria
    if type == 'all':
        expenses = cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date)).fetchall()
    else:
        expenses = cursor.execute("SELECT * FROM expenses WHERE type = ? AND date BETWEEN ? AND ?", (type, start_date, end_date)).fetchall()

    # Render reports page with generated report
    return render_template('reports.html', expenses=expenses, start_date=start_date, end_date=end_date, type=type)

# Main function
if __name__ == '__main__':
    app.run(debug=True)
