from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)


@app.route('/')
def route_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(
        debug=True, # Allow verbose error reports
        port=5111 # Set custom port
    )