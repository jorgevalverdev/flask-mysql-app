from flask import Flask
from flask import Flask, render_template, json, request, Response
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)

mysql = MySQL()
# MySQL configurations 
app.config['MYSQL_DATABASE_USER'] = 'python_apps'
app.config['MYSQL_DATABASE_PASSWORD'] = 'G7#dL9@tQ2!mX4&z'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
@app.route('/main')
@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    conn = mysql.connect()
    cursor = conn.cursor()
    
    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
    data = cursor.fetchall()
    if len(data) == 0:
        conn.commit()
        return json.dumps({'message':f'User {_name} created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

if __name__ == "__main__":
    app.run()