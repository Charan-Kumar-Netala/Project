from flask import Flask,request,redirect,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb+srv://Charan:Ronaldo97@cluster0.mt15p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

db_operations = mongo.db.users # creating Collection ('db' is Database)

@app.route('/')
def webPage():
    return render_template('webPage.html')

@app.route('/login') ## Login form
def index():
    return render_template('index.html')
    
@app.route('/success', methods = ['POST'])
def success():
    username = request.form['username']
    password = request.form['password']
    query = {'username': username, 'password': password}

    f = db_operations.find()
    output = [{'username' : user['username'], 'password' : user['password']} for user in f]

    # if username in database, return gotit! So, find in collections
    if query in output:
        return redirect('/gotit')
    # if username is not in database, return register
    else:
        return '''  <head>
                        <style> body  {background-color: yellow} 
                                .form {background-color:blue; padding: 20px 32px; width:fit-content}
                                h2    {color: white}
                        </style>
                        </head>
                        <body>
                        <div class="form">
                        <h2>Username not in Database</h2> 
                        <p><a href="/register" style="color:yellow">Register</p></div></body>'''

@app.route('/register',methods = ['POST','GET']) ## Registration form
def register():
    if request.method =='POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if name == '':
            return '''  <head>
                        <style> body  {background-color: yellow} 
                                .form {background-color:blue; padding: 20px 32px; width:fit-content}
                                h2    {color: white}
                        </style>
                        </head>
                        <body>
                        <div class="form">
                        <h2>Invalid name combination</h2> 
                        <p><a href="/register" style="color:yellow">Register</p></div></body>'''
        db_operations.insert_one({'name': name,'username': username, 'password': password})
        return redirect('/gotit')
    else:
        return render_template('register.html')

@app.route('/reset',methods=['POST','GET'])
def reset():
    if request.method== 'POST':
        name = request.form['name']
        new_password = request.form['password']
        query = {'name': name}
        new_values={'$set':{'password': new_password}}
        
        f = db_operations.find()
        output = [{'name' : user['name']} for user in f]
        if query in output:
            db_operations.update_one(query,new_values)
            return redirect('/login')
        else:
            return 'Name not found' + '<p><a href="/reset">Reset</p>'
    else:
        return render_template('reset_password.html')

@app.route('/gotit')
def gotit():
    return render_template('ref.html')
     
# @app.route('/create')
# def create():
#     new_user = {'Name' : 'xyz', 'Age' : 20}
#     db_operations.insert_one(new_user)
#     #print(user['Name'],'Created successfully')
#     result = {'result' : 'Created successfully'}
#     return result

# @app.route('/create')
# def create_many():
#     new_user_1 = {'Name' : 'xyz1', 'Age' : 10}
#     new_user_2 = {'Name' : 'xyz2', 'Age' : 20}
#     new_user_3 = {'Name' : 'xyz3', 'Age' : 30}
#     new_users = [new_user_1, new_user_2, new_user_3]
#     db_operations.insert_many(new_users)
#     result = {'result' : 'Created successfully'}
#     return result

# @app.route('/read')
# def read():
#     users = db_operations.find()
#     output = [{'Name' : user['Name'], 'Age' : user['Age']} for user in users]
#     #print(output)
#     return jsonify(output)

# @app.route('/')
# def index():
#     return '''
#         <h1>Save file</h1>
#         <form method="POST" action="/save-file" enctype="multipart/form-data">
#             <label for="name">Name</label>
#             <input type="text" name="name" id="name">
#             <input type="file" name="new_file"><br><br>
#             <input type="submit">
#         </form>
#     '''

# @app.route('/save-file', methods=['POST'])
# def save_file():
#     if 'new_file' in request.files:
#         new_file = request.files['new_file']
#         mongo.save_file(new_file.filename, new_file)
#         data = {'Name' : request.values.get('name'), 'File Name' : new_file.filename}
#         db_operations.insert(data)
#     return redirect('/')

# @app.route('/retrieve-file/<name>')
# def retrieve_file(name):
#     filt = {'Name' : name}
#     f = db_operations.find_one(filt)
#     file_name = f['File Name']
#     return mongo.send_file(file_name)

if __name__ == '__main__':
    app.run(debug=True)