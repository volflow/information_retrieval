from flask import Flask, render_template
app = Flask(__name__)
correct = 0

@app.route("/")
def main():
    return render_template('signup.html')

@app.route("/loggedin")
def mainer():
    return render_template('intro.html')

@app.route("/start")
def mainerr():
    return render_template('screenload.html')

@app.route("/help")
def mainerrr():
    return render_template('help.html')

if __name__ == "__main__":
    app.run()
