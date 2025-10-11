from flask import Flask,render_template,redirect, url_for, request, make_response

# Create an instance of the Flask class
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("hello.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/index', methods=['POST'])
def index():
     ContexData={
    'email' :request.form["email"],
    'password' :request.form["password"],
    }
     return render_template("index.html",**ContexData)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)