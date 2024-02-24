from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)

a={"אביגיל_יוסף", "נחמה_מזרחי","אלון_מלול","נעמי_עואד","בת שבע_שחר"}

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
users_df = pd.read_excel("passwords_register30.xlsx")
users_list = list(users_df.Username.unique())

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print("THIS: ", list(users_df[users_df['Username']==username]['Password'])[0])#,type(list(users_df[users_df['Username']==username]['Password'])))
    # if username in users_list and users[username]['password'] == password:
    if username in users_list and list(users_df[users_df['Username']==username]['Password'])[0] == password:
        
        # Valid login, set session variables
        session['username'] = username
        print("THIS2",list(users_df[users_df['Username']==username]['Role'])[0])
        session['role'] = list(users_df[users_df['Username']==username]['Role'])[0]
        session['Client'] = list(users_df[users_df['Username']==username]['Client'])[0]
        # session['role'] = users[username]['role']
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
        # filtered_data = df[df['Role'] == user_role]
        passwords = pd.read_excel("passwords_register30.xlsx")#['']
        filtered_data = pd.read_excel("permissions_df80.xlsx")
        filtered_data_filtered = filtered_data[(filtered_data['Client']==session['Client']) & (filtered_data['Role']==session['role'])][['Site','Access']]#.set_index('Site')

        return render_template('dashboard.html', username=username, data1=filtered_data.to_html(),data2=passwords.to_html(), data3=filtered_data_filtered.to_html())
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
