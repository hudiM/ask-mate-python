from flask import Flask, render_template, redirect, request, session
import data_manager
import connection

app = Flask(__name__)


# ------------------------
#           main
# ------------------------

@app.route('/')
@app.route('/list')
def route_index():
    questions = connection.readAllQuestion(data_manager.questions_file_name)
    questions = sorted(questions,key=lambda k: k['submission_time'], reverse=True)
    return render_template('list.html', questions = questions)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        form = {'title' : request.form['title'], 'message' : request.form['message'], 'image' : request.form['image']}
        unique_id = data_manager.addNewQuestion(form)
        return redirect('/question/' + str(unique_id))
    return render_template('new_question.html', question = None)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = connection.readQuestion(data_manager.questions_file_name, question_id)
    question = data_manager.countViews(question)
    question = data_manager.convertTime(question)
    answers = data_manager.getAnswersForQuestion(data_manager.answers_file_name, question_id)
    return render_template('question.html', question=question, answers = answers)


@app.route('/question/<question_id>/delete')
def route_question_delete(question_id):
    data_manager.deleteQuestion(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def route_answer_delete(answer_id):
    question_id = data_manager.deleteAnswer(answer_id)
    return redirect('/question/'+question_id)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'POST':
        form = {'title' : request.form['title'], 'message' : request.form['message'], 'image' : request.form['image']}
        data_manager.editQuestion(form, question_id)
        return redirect('/question/'+question_id)
    question = connection.readQuestion(data_manager.questions_file_name, question_id)
    return render_template('new_question.html', question = question)


@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        form = {'message': request.form['message'], 'image': request.form['image']}
        data_manager.addNewAnswer(form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', question_id = question_id)


@app.route('/answer/<answer_id>/vote-up')
def route_vote_up(answer_id):
    question_id = data_manager.voteAnswerUp(answer_id)
    return redirect('/question/'+question_id)

@app.route('/answer/<answer_id>/vote-down')
def route_vote_down(answer_id):
    question_id = data_manager.voteAnswerDown(answer_id)
    return redirect('/question/'+question_id)

@app.route('/question/<question_id>/vote-up')
def route_vote_up_question(question_id):
    data_manager.voteQuestion('up', question_id)
    return redirect('/question/'+question_id)

@app.route('/question/<question_id>/vote-down')
def route_vote_down_question(question_id):
    data_manager.voteQuestion('down', question_id)
    return redirect('/question/'+question_id)

# ------------------------
#           debug
# ------------------------

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

# ------------------------
#           server
# ------------------------

if __name__ == '__main__':
    app.run(
        debug=True, # Allow verbose error reports
        port=5111 # Set custom port
    )
