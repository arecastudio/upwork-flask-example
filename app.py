from flask import Flask,redirect,url_for,request,render_template,jsonify
from flask_mysqldb import MySQL

app=Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_USER'] = 'rail'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'upwork_flask'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# TODO Update secret key
app.secret_key = 'UPDATETHISPART'

#mysql.init_app(app)
mysql=MySQL(app)

#conn = mysql.connect()
#cursor = conn.cursor()

@app.route('/')
def myindex():
    user="mark"
    if request.method=='GET':
        sql="SELECT * FROM person ORDER BY createdate ASC;"
        try:
            cursor=mysql.connection.cursor()
            cursor.execute(sql)
            mydata=cursor.fetchall()
            cursor.close()
            #return redirect(url_for('myindex'))
            return render_template('default.html',data=mydata)
        except Exception as e:
            return jsonify({'failed':str(e)})

@app.route('/loadTable')
def loadTable():
    user="mark"
    if request.method=='GET':
        sql="SELECT * FROM person ORDER BY createdate ASC;"
        try:
            cursor=mysql.connection.cursor()
            cursor.execute(sql)
            mydata=cursor.fetchall()
            cursor.close()
            #return redirect(url_for('myindex'))
            return render_template('table-view.html',data=mydata)
        except Exception as e:
            return jsonify({'failed':str(e)})

@app.route('/add',methods=['POST','GET'])
def add_person():
    if request.method=='POST':
        firstname=request.form['firstname']
        familyname=request.form['familyname']
        age=request.form['age']
        status=request.form['status']

        sql="INSERT INTO person(firstname,familyname,age,status)VALUES(%s,%s,%s,%s);"
        try:
            cursor=mysql.connection.cursor()
            cursor.execute(sql,(firstname,familyname,int(age),status))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'success':'Data submited sucessful.'})
        except Exception as e:
            return jsonify({'failed':str(e)})
        
@app.route('/dataview/<idx>',methods=['GET'])
def dataview(idx):
    if request.method=='GET':
        sql="SELECT * FROM person where id=%s;"
        try:
            cursor=mysql.connection.cursor()
            cursor.execute(sql,(idx))
            mydata=cursor.fetchall()
            cursor.close()
            return render_template('table-view.html',data=mydata)
        except Exception as e:
            return jsonify({'failed':str(e)})


if __name__ == '__main__':
    app.run(debug=True)
