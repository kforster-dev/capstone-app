from flask import Flask, render_template, request
import os, pymysql, pandas

app = Flask(__name__)

LOG_SERVER = '192.168.1.3'

'''
db_host = os.environ['MYSQL_HOST']
db_pass = os.environ['MYSQL_PASSWORD']
db_user = os.environ['MYSQL_USER']
db_name = os.environ['MYSQL_DB']
'''

maria_db = 'void'
maria_user = 'root'
maria_pass = 'secret'
maria_host = '192.168.1.2'

log_db = 'logdb'
log_user = 'voidlog'
log_pass = 'voidpass'

LogConnection = pymysql.connect(host=LOG_SERVER, user=log_user, passwd=log_pass, db=log_db)
#MariaConnection = pymysql.connect(host=maria_host, user=maria_user, passwd=maria_pass, db=maria_db)

def doQuery(connection, querystring):
    cursor = connection.cursor()
    cursor.execute(querystring)
    data = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return data, columns

def getQuery(connection, querystring):
    cursor = connection.cursor()
    cursor.execute(querystring)
    return cursor.fetchall()

def CreateTable(sql_data, Columns):
    df = pandas.DataFrame(sql_data, columns=Columns)
    table = df.to_html(index=False, classes='dbtable')
    return table

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/admin')
def adminpage():
    return render_template('admin.html', boolean=True)

@app.route('/logs')
def logpage():
    try:
        querystring = "SELECT * FROM logs ORDER BY RecordId DESC LIMIT 10;"
        SqlData, Columns = doQuery(LogConnection, querystring)
        html_table = CreateTable(SqlData, Columns)

        return render_template('logdisp.html', table=html_table)
    except Exception as e:
        print(e)
        return "<h1>Sorry, something went wrong: " + e + "</h1>"

@app.route('/admin/createuser', methods=['GET', 'POST'] )
def createuser():
    data = request.form
    if data:
        newUserName = data.get('fname')+'.'+data.get('lname')
        try:
            #querystring = "SELECT * FROM users"
            #SqlData, Columns = doQuery(MariaConnection, querystring)
            #html_table = CreateTable(SqlData, Columns)

            return render_template(
            'welcome.html',
            fname = data.get('fname'), 
            lname = data.get('lname'),
            newgroups = data.get('addgroups'),
            username = newUserName,
            )
        
        except Exception as e:
            print(e)
            return "<h1>Sorry, something went wrong: </h1>" , e

    return render_template('createuser.html', boolean=True)

if __name__ == "__main__":
    app.run(debug=True)