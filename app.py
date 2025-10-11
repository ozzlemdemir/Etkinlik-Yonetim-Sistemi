from flask import Flask,render_template

# Create an instance of the Flask class
app = Flask(__name__)

@app.route('/')
def hello_world():
    return ("hello.html")

@app.route('/login')
def login():
    return ("login.html")

# Run the application
if __name__ == '__main__':
    app.run(debug=True)