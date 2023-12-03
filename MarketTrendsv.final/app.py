# app.py
from flask import Flask, render_template, send_from_directory, url_for, redirect
import psycopg2
import plotly.express as px


app = Flask(__name__, static_folder='static')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="companydata",
    user="postgres",
    password="please enter your pw",
    host="localhost",
    port="please enter your port"
)

cur = conn.cursor()


@app.route('/')
def home():
    # Fetch data from PostgreSQL
    # query = "SELECT 'Date', 'amzn4Qsum' FROM ftp3"
    cur.execute('SELECT year, MAX(amznyeps) FROM ftp3 GROUP BY year')
    rows = cur.fetchall()

    cur.execute('SELECT year, "amznPEratio" FROM ftp3')
    rows_l = cur.fetchall()

    

# Extracting data from rows for chart 1 on home page
    categories = [row[0] if len(row) >= 1 else None for row in rows]
    values = [row[1] if len(row) >= 2 else None for row in rows]
# Extracting data from rows for chart 2 on home page
    categories2 = [row[0] if len(row) >= 1 else None for row in rows_l]
    values2 = [row[1] if len(row) >= 2 else None for row in rows_l]
    

# Creating a Plotly Express bar chart
    fig = px.bar(x=categories, y=values, labels={'x': 'Year', 'y': 'Amazon Annul EPS($)'}, title="Amazon EPS", color=values, color_continuous_scale='delta', orientation='v', template="simple_white")
    
#Connet to Html
    chart_path = "static/chart.html"
    fig.write_html(chart_path)
# Render the chart in the HTML template
    chart_div = fig.to_html(full_html=False)


    fig2 = px.line(x=categories2, y=values2, labels={'x': 'Year', 'y': 'Amazon PE Ratio'}, title="Amazon")
    line_chart_path = "static/line_chart.html"
    fig2.write_html(line_chart_path)
    line_chart_div = fig2.to_html(full_html=False)

    

    


    # cur.close()
    # conn.close()

    return render_template('index.html', chart_div=chart_div, line_chart_div=line_chart_div)


@app.route('/switch_data/<company>')
def switch_data(company):
    # Fetch data based on the selected company
    if company == 'amazon':
        cur.execute('SELECT year, MAX(amznyeps) FROM ftp3 GROUP BY year')
        title = "Amazon Annul EPS"
    elif company == 'boa':
        cur.execute('SELECT year, MAX(bacyeps) FROM ftp3 GROUP BY year')
        title = "Bank of America Annul EPS"
    elif company == 'google':
        cur.execute('SELECT year, MAX(googlyeps) FROM ftp3 GROUP BY year')
        title = "Google Annul EPS"
    elif company == 'mcd':
        cur.execute('SELECT year, MAX(mcdyeps) FROM ftp3 GROUP BY year')
        title = "McDonald's Annul EPS"
    elif company == 'vz':
        cur.execute('SELECT year, MAX(vzyeps) FROM ftp3 GROUP BY year')
        title = "Verizon Communications Annul EPS"        
    else:
        # Handle other companies or invalid input
        return "Invalid company"

    rows = cur.fetchall()


    # Extracting data
    categories = [row[0] if len(row) >= 1 else None for row in rows]
    values = [row[1] if len(row) >= 2 else None for row in rows]

    # Creating a Plotly Express line chart for the selected data
    fig = px.bar(x=categories, y=values, labels={'x': 'Year', 'y': f'{company} EPS ($)'}, title=title, color=values, color_continuous_scale='delta', orientation='v')

    # Save the chart to an HTML file
    chart_path = f"static/chart_{company}.html"
    fig.write_html(chart_path)

    # Render the HTML template with the selected chart
    return redirect(url_for('static', filename=f'chart_{company}.html'))

@app.route('/switch_data_line_chart/<company>')
def switch_data_line_chart(company):
    # Fetch data based on the selected company
    if company == 'amazon':
        cur.execute('SELECT year, "amznPEratio" FROM ftp3')
        title = "Amazon PE Ratio"
    elif company == 'bank_of_america':
        cur.execute('SELECT year, "bacPEratio" FROM ftp3')
        title = "Bank of America PE Ratio"
    elif company == 'google':
        cur.execute('SELECT year, "googlPEratio" FROM ftp3')
        title = "Google PE Ratio"
    elif company == 'mcd':
        cur.execute('SELECT year, "mcdPEratio" FROM ftp3')
        title = "McDonald's PE Ratio"  
    elif company == 'vz':
        cur.execute('SELECT year, "vzPEratio" FROM ftp3')
        title = "Verizon Communications PE Ratio"      
    else:
        # Handle other companies or invalid input
        return "Invalid company"

    rows = cur.fetchall()


    # Extracting data
    categories = [row[0] if len(row) >= 1 else None for row in rows]
    values = [row[1] if len(row) >= 2 else None for row in rows]

    # Creating a Plotly Express line chart for the selected data
    fig = px.line(x=categories, y=values, labels={'x': 'Year', 'y': f'{company} PE Ratio'}, title=title)

    # Save the chart to an HTML file
    chart_path = f"static/line_chart_{company}.html"
    fig.write_html(chart_path)

    # Render the HTML template with the selected chart
    return redirect(url_for('static', filename=f'line_chart_{company}.html'))
    



if __name__ == '__main__':
    app.run(debug=True)
