import io
from flask import Flask, render_template, render_template_string, url_for, session, send_file, request, redirect
import pandas as pd
from weasyprint import HTML
# from flask import render_template_string
import copy

app_commit = Flask(__name__)
app_commit.secret_key = b"_j'yXdW7.63}}b72"

# app = Flask(__name__)
# app.secret_key = b"_j'yXdW7.63}}b72"

# Read data from Excel file
# excel_file_path = "generated_records_with_restrictions_hebrew_2.xlsx"
excel_file_path = "generated_records_with_restrictions_hebrew_updated_by.xlsx"
df = pd.read_excel(excel_file_path)[:40]
print("here:::: ",df)
entrance_data = "generated_entrance_details_from_list_4.xlsx"
entrance_df = pd.read_excel(entrance_data)[:40]

limited_df = None
bla = None
temp_df = None

# Create the permissions DataFrame
permissions_df = pd.read_excel("permissions_df80.xlsx")
passwords_df = pd.read_excel("users.xlsx")

passwords_df = pd.read_excel("users.xlsx")
permissions_df = pd.read_excel("permissions.xlsx")
users_list = list(passwords_df.Username.unique())


@app_commit.route('/')
def index():
    return render_template('login.html')

@app_commit.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print("THIS: ", list(passwords_df[passwords_df['Username']==username]['Password'])[0])#,type(list(users_df[users_df['Username']==username]['Password'])))
    # if username in users_list and users[username]['password'] == password:
    if username in users_list and list(passwords_df[passwords_df['Username']==username]['Password'])[0] == password:
        
        # Valid login, set session variables
        session['username'] = username
        print("THIS2",list(passwords_df[passwords_df['Username']==username]['Role'])[0])
        session['role'] = list(passwords_df[passwords_df['Username']==username]['Role'])[0]
        session['Client'] = list(passwords_df[passwords_df['Username']==username]['Client'])[0]
        # session['role'] = users[username]['role']
        return redirect(url_for('dashboard'))
    else:
        return "Invalid login credentials. Please try again."

@app_commit.route('/See_permissions_table')
def see_permissions():
    return render_template('extra_data.html', extra_data_table=permissions_df.to_html(classes='data', index=False), extra_data_table2=passwords_df.to_html(classes='data', index=False))

def check_entrance_permission(id_number):
    # Search for the ID number in the DataFrame
    result = entrance_df[entrance_df['ת.ז'] == id_number]

    if not result.empty:
        # If a match is found, return details
        details = result.to_dict(orient='records')[0]
        return True, details
    else:
        # If no match is found, return False
        return False, None

# @app_commit.route('/check_permission', methods=['GET', 'POST'])
# def check_permission():
#     result = None

#     if request.method == 'POST':
#         id_number = request.form.get("id_number")
#         has_permission, details = check_entrance_permission(id_number)
#         result = {'has_permission': has_permission, 'details': details}

#     return render_template('check_permission.html', result=result)

@app_commit.route('/check_permission', methods=['GET', 'POST'])
def check_permission():
    id_number = request.form.get("id_number")
    has_permission, details = check_entrance_permission(id_number)

    if has_permission:
        result_html = """
            <h2>Entrance Permission Found</h2>
            <p>Details:</p>
            <ul>
                <li><strong>מספר סידורי:</strong> {0}</li>
                <li><strong>שם לקוח:</strong> {1}</li>
                <!-- Add other details as needed -->
            </ul>
        """.format(details.get('מספר סידורי', ''), details.get('שם לקוח', ''))
    else:
        result_html = "<p>No entrance permission found for the given ID.</p>"

    return result_html

@app_commit.route('/entrance_permissions')
def entrance_permissions():
    global entrance_df, limited_df, bla
    temp_df_entrance = copy.deepcopy(entrance_df)
    # temp_df_entrance2 = copy.deepcopy(df)
    # print("permissions:",permissions_df.columns,session.client)
    filtered_data_filtered = permissions_df[(permissions_df['Client']==session['Client']) & (permissions_df['Role']==session['role'])][['Client','Site','Access']]#.set_index('Site')
    print("THIS3: אשדוד_ב is in ", (filtered_data_filtered['Site']), "אשדוד_ב" in (list(filtered_data_filtered['Site'])))
    # print
    print("BEFORE:")
    # print(entrance_df)
    print("AFTER:")
    temp_df_entrance = entrance_df[(entrance_df['אתר'].isin(filtered_data_filtered['Site'])) & (entrance_df['שם לקוח'].isin(filtered_data_filtered['Client']))][:30]
    # limited_df = copy.deepcopy(temp_df_entrance)
    print("THIS IS ALSO THE LIMITED6:",temp_df_entrance)
    print("THIS IS ALSO THE LIMITED7:",limited_df)
    print("THIS IS ALSO THE LIMITED78:",bla)
    bla=copy.deepcopy(temp_df_entrance)
    print("THIS IS ALSO THE LIMITED79:",bla)

    print(entrance_df)

    session["df"] = entrance_df.to_csv(index=False, header=True, sep=";")


    # Filter DataFrame based on selected issue type
    selected_issue = request.args.get("issue")
    if selected_issue:
        temp_df_entrance = entrance_df[entrance_df["שם מורשה"] == selected_issue]

    # Filter DataFrame based on selected timeframe
    selected_timeframe = request.args.get("timeframe")
    if selected_timeframe:
        today = pd.Timestamp.today().normalize()
        if selected_timeframe == "1_month":
            start_date = today - pd.DateOffset(months=1)
        elif selected_timeframe == "3_months":
            start_date = today - pd.DateOffset(months=3)
        elif selected_timeframe == "6_months":
            start_date = today - pd.DateOffset(months=6)
        elif selected_timeframe == "1_year":
            start_date = today - pd.DateOffset(years=1)
        else:
            start_date = today

        temp_df_entrance = temp_df_entrance[tetemp_df_entrancemp_df["תאריך +שעה"] >= start_date]

    session["df"] = temp_df_entrance.to_csv(index=False, header=True, sep=";")
    print("THIS IS A TEST:", type(session["df"]), session["df"])
    # session["temp_df_entrance"] = temp_df_entrance.to_html

    # Pass the DataFrame to the template along with the unique issue types and timeframes
    unique_issues = entrance_df["שם מורשה"].unique().tolist()
    unique_timeframes = ["1_month", "3_months", "6_months", "1_year"]
    atarim = temp_df_entrance["אתר"].unique().tolist()
    unique_clients = temp_df_entrance["שם לקוח"].unique().tolist()

    # session["dfff2"] = temp_df_entrance
    print("ALSSO THIS: ",session["df"])
    print("THIS IS ALSO THE LIMITED10:",temp_df_entrance)
    print("THIS IS ALSO THE LIMITED11:",limited_df)
    print("THIS IS ALSO THE LIMITED177:",bla)

    return render_template(
        'permissions.html',
        # 'hello.html',
        tables=[temp_df_entrance.to_html(classes='data', index=False)],
        titles=df.columns.values,
        unique_issues=unique_issues,
        unique_timeframes=unique_timeframes,
        selected_issue=selected_issue,
        selected_timeframe=selected_timeframe,
        atarim=atarim,
        unique_clients=unique_clients,
        data3=filtered_data_filtered.to_html()
    )


@app_commit.route('/hello')
def hello():
    return render_template('hello.html')


@app_commit.route('/dashboard')
def dashboard():
    global df, limited_df, bla
    temp_df = copy.deepcopy(df)
    # temp_df2 = copy.deepcopy(df)
    # print("permissions:",permissions_df.columns,session.client)
    filtered_data_filtered = permissions_df[(permissions_df['Client']==session['Client']) & (permissions_df['Role']==session['role'])][['Client','Site','Access']]#.set_index('Site')
    print("THIS3: אשדוד_ב is in ", (filtered_data_filtered['Site']), "אשדוד_ב" in (list(filtered_data_filtered['Site'])))
    # print
    print("BEFORE:")
    # print(df)
    print("AFTER:")
    temp_df = df[(df['אתר'].isin(filtered_data_filtered['Site'])) & (df['שם לקוח'].isin(filtered_data_filtered['Client']))][:30]
    # limited_df = copy.deepcopy(temp_df)
    print("THIS IS ALSO THE LIMITED6:",temp_df)
    print("THIS IS ALSO THE LIMITED7:",limited_df)
    print("THIS IS ALSO THE LIMITED78:",bla)
    bla=copy.deepcopy(temp_df)
    print("THIS IS ALSO THE LIMITED79:",bla)

    print(df)

    session["df"] = df.to_csv(index=False, header=True, sep=";")


    # Filter DataFrame based on selected issue type
    selected_issue = request.args.get("issue")
    if selected_issue:
        temp_df = df[df["סוג תקלה"] == selected_issue]

    # Filter DataFrame based on selected timeframe
    selected_timeframe = request.args.get("timeframe")
    if selected_timeframe:
        today = pd.Timestamp.today().normalize()
        if selected_timeframe == "1_month":
            start_date = today - pd.DateOffset(months=1)
        elif selected_timeframe == "3_months":
            start_date = today - pd.DateOffset(months=3)
        elif selected_timeframe == "6_months":
            start_date = today - pd.DateOffset(months=6)
        elif selected_timeframe == "1_year":
            start_date = today - pd.DateOffset(years=1)
        else:
            start_date = today

        temp_df = temp_df[temp_df["תאריך +שעה"] >= start_date]

    session["df"] = temp_df.to_csv(index=False, header=True, sep=";")
    print("THIS IS A TEST:", type(session["df"]), session["df"])
    # session["temp_df"] = temp_df.to_html

    # Pass the DataFrame to the template along with the unique issue types and timeframes
    unique_issues = df["סוג תקלה"].unique().tolist()
    unique_timeframes = ["1_month", "3_months", "6_months", "1_year"]
    atarim = temp_df["אתר"].unique().tolist()
    unique_clients = temp_df["שם לקוח"].unique().tolist()

    # session["dfff2"] = temp_df
    print("ALSSO THIS: ",session["df"])
    print("THIS IS ALSO THE LIMITED10:",temp_df)
    print("THIS IS ALSO THE LIMITED11:",limited_df)
    print("THIS IS ALSO THE LIMITED177:",bla)

    return render_template(
        'index.html',
        tables=[temp_df.to_html(classes='data', index=False)],
        titles=df.columns.values,
        unique_issues=unique_issues,
        unique_timeframes=unique_timeframes,
        selected_issue=selected_issue,
        selected_timeframe=selected_timeframe,
        atarim=atarim,
        unique_clients=unique_clients,
        data3=filtered_data_filtered.to_html()
    )

    # Pass the DataFrame to the template
    return render_template('index.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
from io import BytesIO

@app_commit.route("/download", methods=["POST"])
def download():
    # Get the CSV data as a string from the session
    csv = session["df"] if "df" in session else ""
    
    # Create a string buffer
    buf_str = io.StringIO(csv)

    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    
    # Return the CSV data as an attachment
    return send_file(buf_byt,
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="data.csv")


from tabulate import tabulate
from reportlab.pdfgen import canvas
import io



from io import StringIO

@app_commit.route("/download_pdf", methods=["POST"])
def download_pdf():
    global limited_df, bla,temp_df
    # ddf = pd.read_csv(session["df"])
    # print("NOWW THIS IS ALSO THE LIMITED792:",ddf)
    csv_file_like_object = StringIO(session["df"])#, sep=';')

    # Read the CSV data into a DataFrame
    this_df = pd.read_csv(csv_file_like_object)
    print("NOWW THIS IS ALSO THE LIMITED792:",df)

    print("THIS IS ALSO THE LIMITED798:",type(bla), bla)

    print("SEEE ALSSO THIS3: ",session["df"])
    print("THIS IS ALSO THE LIMITED12:",temp_df)
    print("THIS IS ALSO THE LIMITED13:",limited_df)

    print("THIS IS THE LIMITED8:", bla)
    # Get the HTML content from the template
    html_content = render_template_string(
        '<h1>רשימת תקלות</h1>{{ table|safe }}', 
        table=bla.to_html(classes='data', index=False)
    )

    # @page {
    #         background: white;
    #         display: block;
    #         margin: 0in 0.44in 0.2in 0.44in;
    #         margin-bottom: 0.5cm;
    #         box-shadow: 0 0 0.5cm rgba(0,0,0,0.5);
    #         }

    # Get the HTML content from the template with styles
    html_content = render_template_string(
        """
        <style>
            /* Include your table styles here */
            table {
                border-collapse: collapse;
                # width: 70%;
                width: 70%; /* Set table width to 100% of the container */
                max-width: 70%; /* Set maximum width to prevent overflow */
            }
            @page {
                size: landscape;
            }
            
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }

            th {
                background-color: #f2f2f2;
            }
        </style>
        <h1>רשימת תקלות</h1>
        {{ table|safe }}
        """, 
        table=bla.to_html(classes='data', index=False)
    )

    # Create a PDF file from the HTML content
    pdf_file = HTML(string=html_content).write_pdf(size=('A3', 'landscape'))

    # Create a bytes buffer from the PDF file
    buf_byt = io.BytesIO(pdf_file)
    

    return send_file(
        buf_byt,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="data.pdf"
    )

@app_commit.route("/add_entry", methods=["POST"])
def add_entry():
    global df  # Make df global so that it can be accessed and modified

    # Retrieve form data
    serial_number = request.form.get("serial_number")
    customer_name = request.form.get("customer_name")
    date_time = request.form.get("date_time")
    location = request.form.get("location")
    issue_type = request.form.get("issue_type")
    description = request.form.get("description")
    report_to = request.form.get("report_to")
    call_number = request.form.get("call_number")
    treatment_completion = request.form.get("treatment_completion")
    notes = request.form.get("notes")
    event_closed_by = request.form.get("event_closed_by")
    last_updated_by = session['username']

    # Add the new entry to the DataFrame
    new_entry = pd.DataFrame({
        "מספר סידורי": [serial_number],
        "שם לקוח": [customer_name],
        "תאריך +שעה": [date_time],
        "אתר": [location],
        "סוג תקלה": [issue_type],
        "תיאור": [description],
        "דווח ל...": [report_to],
        "מס' קריאה": [call_number],
        "סיום טיפול (סגירה)": [treatment_completion],
        "הערות": [notes],
        "מי סגר את האירוע": [event_closed_by],
        "עודכן לאחרונה על ידי": [last_updated_by],
    })

    df = pd.concat([df, new_entry], ignore_index=True)

    # Update the session with the updated DataFrame
    session["df"] = df.to_csv(index=False, header=True, sep=";")

    # # Redirect back to the main page
    # return redirect("/")

    issue_types = ["Type A", "Type B", "Type C"]
    locations = ["Location 1", "Location 2", "Location 3"]
    customer_names = ["Customer 1", "Customer 2", "Customer 3"]

    # Pass dropdown values as arguments to the HTML page
    return render_template('index.html', 
    issue_types=issue_types, 
    locations=locations, 
    customer_names=customer_names)

 
# @app_commit.route("/add_entry", methods=["POST"])
# def add_entry():
#     global df  # Make df global so that it can be accessed and modified

#     # Retrieve form data
#     name = request.form.get("name")
#     age = request.form.get("age")
#     city = request.form.get("city")

#     # Add the new entry to the DataFrame
#     new_entry = pd.DataFrame({"Name": [name], "Age": [int(age)], "City": [city]})
#     df = pd.concat([df, new_entry], ignore_index=True)

#     # Update the session with the updated DataFrame
#     session["df"] = df.to_csv(index=False, header=True, sep=";")

#     # Redirect back to the main page
#     return redirect("/")

if __name__ == '__main__':
    app_commit.run(debug=True, port=5004)
