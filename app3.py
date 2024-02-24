from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)

# Dummy DataFrame for demonstration
data = {
    'Name': ['John', 'Alice', 'Bob', 'Eve'],
    'Age': [28, 25, 32, 22],
    'Role': ['Admin', 'User', 'User', 'Guest']
}
df = pd.DataFrame(data)

# Dummy user credentials and roles
users = {
    'john': {'password': 'pass123', 'role': 'Admin'},
    'alice': {'password': 'pass456', 'role': 'User'},
    'bob': {'password': 'pass789', 'role': 'User'},
    'eve': {'password': 'pass999', 'role': 'Guest'},
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        # Valid login, set session variables
        session['username'] = username
        session['role'] = users[username]['role']
        return redirect(url_for('dashboard'))
    else:
        return "Invalid login credentials. Please try again."

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        user_role = session['role']

        # Filter data based on user role
        filtered_data = df[df['Role'] == user_role]

        return render_template('dashboard.html', username=username, data=filtered_data.to_html())
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Clear session variables on logout
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'  # Change this to a secure secret key
    app.run(debug=True)
