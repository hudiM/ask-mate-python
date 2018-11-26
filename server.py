from flask import Flask, render_template, redirect, request, session
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
def route_index():
    data_manager.test()
    questions = connection.readAllQuestion(data_manager.questions_file_name)
    print(questions)
    return render_template('list.html', questions = questions)


if __name__ == '__main__':
    app.run(
        debug=True, # Allow verbose error reports
        port=5111 # Set custom port
    )
