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
excel_file_path = "generated_records_with_restrictions_hebrew.xlsx"
df = pd.read_excel(excel_file_path)[:40]
limited_df = None
bla = None
temp_df = None
# print(df)
# @app.route('/')
# def index():
#     session["df"] = df.to_csv(index=False, header=True, sep=";")

#     # Pass the DataFrame to the template
#     return render_template('index.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

# # Create a dummy DataFrame
# data = {'Name': ['John', 'Alice', 'Bob'],
#         'Age': [25, 30, 22],
#         'City': ['New York', 'San Francisco', 'Chicago']}
# df = pd.DataFrame(data)

# Create the permissions DataFrame
permissions_df = pd.read_excel("permissions_df80.xlsx")[:20]
# pd.DataFrame(permissions_data)

# Create the permissions DataFrame
# passwords_df = pd.read_excel("passwords_register30.xlsx")[:20]
passwords_df = pd.read_excel("users.xlsx")#[:20]
# .DataFrame(permissions_data)

permissions_data = {'לקוח': ['לקוח1', 'לקוח2', 'לקוח3'],
                    'Role': ['Admin', 'User', 'Admin'],
                    'Permission': ['Read/Write', 'Read', 'Read/Write']}

passwords_df = pd.read_excel("users.xlsx")#[:20]
# permissions_df = pd.read_excel("permissions_df80.xlsx")
permissions_df = pd.read_excel("permissions.xlsx")
users_list = list(passwords_df.Username.unique())

# pd.DataFrame(permissions_data)

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
        data3=filtered_data_filtered.to_html()
    )

    # Pass the DataFrame to the template
    return render_template('index.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
from io import BytesIO

@app_commit.route("/download", methods=["POST"])
def download():
    # Get the CSV data as a string from the session
    # csv = session["df"] if "df" in session else ""
    csv_file_like_object = StringIO(session["df"])#, sep=';')

    # Read the CSV data into a DataFrame
    this_df = pd.read_csv(csv_file_like_object, encoding='utf-8')

    pdf_stream = BytesIO()

    # Create a PDF using reportlab
    pdf = canvas.Canvas(pdf_stream, pagesize='A3')
    pdf.drawString(100, 800, "Converted PDF from Excel")
    pdf.drawString(100, 780, "-" * 30)

    # Convert DataFrame to a table in PDF
    table_data = [df.columns.values.tolist()] + df.values.tolist()
    for i, row in enumerate(table_data):
        for j, value in enumerate(row):
            pdf.drawString(100 + j * 100, 760 - (i + 1) * 12, str(value))

    # Save the PDF to the BytesIO object
    pdf.save()

    # Move the cursor to the beginning of the BytesIO object
    pdf_stream.seek(0)

    # Return the BytesIO object as a PDF file for download
    return send_file(pdf_stream, download_name='converted_file.pdf', as_attachment=True)


@app_commit.route("/download22", methods=["POST"])
def download22():
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

@app_commit.route("/download", methods=["POST"])
def download33():
    # app = Flask(__name__)

    # Your CSV data as a string
    csv_data = """Name,Age,City
    John,25,New York
    Alice,30,San Francisco
    Bob,22,Chicago"""

    # Convert CSV string to a table using tabulate
    table = tabulate([row.split(',') for row in csv_data.split('\n') if row], headers='firstrow', tablefmt='grid')

    # Create a PDF buffer
    pdf_buffer = io.BytesIO()

    # Create a PDF using reportlab
    pdf = canvas.Canvas(pdf_buffer, pagesize=(400, 400))  # Adjust the page size as needed

    # Draw the table on the PDF
    pdf.drawString(10, 300, table)

    pdf.save()

    # Move the buffer cursor to the beginning
    pdf_buffer.seek(0)

    # Return the PDF data as an attachment
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="data.pdf"
    )

@app_commit.route("/download_pdf2", methods=["POST"])
def download_pdf2():

# ==
    # # Get the CSV data as a string from the session
    # csv = session["df"] if "df" in session else ""

    # # Create a DataFrame from the CSV data
    # df_from_csv = pd.read_csv(pd.compat.StringIO(csv), sep=';')

    # <body>{df_from_csv.to_html(index=False)}</body>
    print("SEEE ALSSO THIS3: ",session["df"])

    # Create an HTML object with rotated table
    html_str = f"""
    <html>
    <head><style>
    table {{ transform: rotate(-90deg); white-space: nowrap; }}
    </style></head>
    <body>{session["df"].to_html(index=False)}</body>
    </html>
    """
    html = HTML(string=html_str)

    # Create PDF with rotated table
    pdf_bytes = html.write_pdf()

    # Return the PDF data as an attachment
    return send_file(io.BytesIO(pdf_bytes),
                     mimetype="application/pdf",
                     as_attachment=True,
                     download_name="data.pdf")


# ==

# import fitz  # PyMuPDF
import PyPDF2

# ---
@app_commit.route("/download_pdf4", methods=["POST"])
def download_pdf4():
    # Your HTML content
    html_content = "<html><body><p>Your HTML content</p></body></html>"

    # Create a PDF file from the HTML content
    pdf_bytes = HTML(string=html_content).write_pdf()

    # Create a bytes buffer from the PDF file
    pdf_buffer = io.BytesIO(pdf_bytes)

    # Open the PDF using PyPDF2
    pdf_reader = PyPDF2.PdfReader(pdf_buffer)
    pdf_writer = PyPDF2.PdfWriter()

    # Add pages in reverse order to horizontally flip
    for page_num in range(pdf_reader.numPages - 1, -1, -1):
        page = pdf_reader.getPage(page_num)
        page.rotateClockwise(180)
        pdf_writer.addPage(page)

    # Create a new bytes buffer for the flipped PDF
    flipped_pdf_buffer = io.BytesIO()
    pdf_writer.write(flipped_pdf_buffer)
    flipped_pdf_buffer.seek(0)

    # Return the flipped PDF data as an attachment
    return send_file(
        flipped_pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="flipped_data.pdf"
    )
 

# ---
from xhtml2pdf import pisa
from io import StringIO
import pdfkit
 
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
    
    # def convert_html_to_pdf(html_string, pdf_path):
    #     with open(pdf_path, "wb") as pdf_file:
    #         pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
            
    #     return not pisa_status.err

    # # HTML content
    # html_content = '''
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>PDF Example</title>
    # </head>
    # <body>
    #     <h1>Hello, world!</h1>
    # </body>
    # </html>
    # '''

    # # Generate PDF
    # pdf_path = "example.pdf"
    # if convert_html_to_pdf(html_content, pdf_path):
    #     print(f"PDF generated and saved at {pdf_path}")
    # else:
    #     print("PDF generation failed")
        
    # Return the PDF data as an attachment

    # pdffile = pdfkit.from_string('AskPython :)','sample_string.pdf')
    # buf_byt = io.BytesIO(pdffile)

    return send_file(
        buf_byt,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="data.pdf"
    )

@app_commit.route("/download_pdf888", methods=["POST"])
def download_pdf888():
    html_content = """
    <html>
    <head>
        <style>
            @page {
                size: landscape;
            }
        </style>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
    </html>
    """

    # Generate PDF from HTML content
    pdf_file = HTML(string=html_content).write_pdf()

    # # Get the HTML content from the template with styles
    
    # # Create a PDF file from the HTML content
    # pdf_file = HTML(string=html_content).write_pdf(size=('A3', 'landscape'))

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
    })

    df = pd.concat([df, new_entry], ignore_index=True)

    # Update the session with the updated DataFrame
    session["df"] = df.to_csv(index=False, header=True, sep=";")

    # Redirect back to the main page
    return redirect("/")

 
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
    app_commit.run(debug=True, port=5002)
