from flask import Flask, render_template, redirect, request, session
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    questions = connection.readAllQuestion(data_manager.questions_file_name)
    print(questions)
    return render_template('list.html', questions = questions)


@app.route('/add-question', methods=['GET','POST'])
def route_new_question():
    if request.method == 'POST':
        data_manager.resolveQuestionForm(request.form)
        return redirect('/')
    return render_template('new_question.html')


@app.route('/question/<question_id>')
def route_question(question_id):
    question = connection.readQuestion(data_manager.questions_file_name, question_id)
    return render_template('question.html', question=question)

@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        form = {'message': request.form['message'], 'image': request.form['image']}
        data_manager.addNewAnswer(form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', question_id = question_id)

@app.route('/settings')
def route_settings():
    return render_template('settings.html')

@app.route('/settings/createNewDatabase')
def newDatabase():
    connection.createQuestionDatabase()
    return redirect('/settings')

@app.route('/settings/createDebugDatabase')
def debugDatabase():
    data_manager.createDebugDatabase()
    return redirect('/settings')


if __name__ == '__main__':
    app.run(
        debug=True, # Allow verbose error reports
        port=5111 # Set custom port
    )
