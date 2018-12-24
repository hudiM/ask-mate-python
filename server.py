from flask import Flask, render_template, redirect, request, session, url_for
import data_manager
import connection

app = Flask(__name__)


# ------------------------
#           main
# ------------------------

@app.route('/')
def route_index():
    questions = data_manager.get_latest_questions()
    questions = sorted(questions,key=lambda k: k['submission_time'], reverse=True)
    return render_template('list.html', questions = questions)


@app.route('/list')
def route_list():
    questions = data_manager.get_all_questions()
    questions = sorted(questions,key=lambda k: k['submission_time'], reverse=True)
    return render_template('list.html', questions = questions)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.page_view_counter('up', question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comments = data_manager.get_comments_by_question_id(question_id)
    comments = data_manager.get_all_answer_comments()
    return render_template('question.html', question=question, answers = answers, question_comments=question_comments, comments=comments)


# ------------------------
#           ADD
# ------------------------


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        question_id = data_manager.new_question(request.form)
        return redirect('/question/' + str(question_id['id']))
    return render_template('new_question.html', question=None)


@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        data_manager.new_answer(request.form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', question_id = question_id, answer=None)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def route_new_question_comment(question_id):
    if request.method == 'POST':
        data_manager.new_question_comment(request.form, question_id)
        return redirect('/question/' + str(question_id))
    return render_template('comment.html', question_id=question_id, comment=None)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def route_new_answer_comment(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    if request.method == 'POST':
        data_manager.new_answer_comment(request.form, answer_id)
        return redirect('/question/' + str(question_id))
    return render_template('comment.html', question_id=question_id, comment=None)


# ------------------------
#           DELETE
# ------------------------


@app.route('/question/<question_id>/delete')
def route_question_delete(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def route_answer_delete(answer_id):
    question_id = data_manager.delete_answer(answer_id)
    return redirect('/question/'+ str(question_id))


@app.route('/comments/<comment_id>/delete')
def route_comment_delete(comment_id):
    question_id = data_manager.get_question_id_by_comment_id(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect('/question/' + str(question_id))


# ------------------------
#           EDIT
# ------------------------


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'POST':
        data_manager.edit_question(request.form, question_id)
        return redirect('/question/'+question_id)
    question = data_manager.get_question_by_id(question_id)
    print(question)
    return render_template('new_question.html', question = question)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_answer_edit(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    if request.method == 'POST':
        data_manager.edit_answer(request.form, answer_id)
        return redirect('/question/' + str(question_id))
    answer = data_manager.get_answer_by_answer_id(answer_id)
    return render_template('new_answer.html', answer=answer)


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def route_comment_edit(comment_id):
    if request.method == 'POST':
        question_id = data_manager.edit_comment(request.form, comment_id)
        return redirect('/question/' + str(question_id))
    comment = data_manager.get_comment_by_comment_id(comment_id)
    print(comment)
    return render_template('comment.html', comment=comment)


# ------------------------
#           VOTE
# ------------------------


@app.route('/answer/<answer_id>/vote-up')
def route_vote_up(answer_id):
    question_id = data_manager.vote('answer','up',answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote-down')
def route_vote_down(answer_id):
    question_id = data_manager.vote('answer','down',answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/vote-up')
def route_vote_up_question(question_id):
    data_manager.vote('question','up',question_id)
    return redirect('/question/'+question_id)


@app.route('/question/<question_id>/vote-down')
def route_vote_down_question(question_id):
    data_manager.vote('question','down',question_id)
    return redirect('/question/'+question_id)

# ------------------------
#           server
# ------------------------

if __name__ == '__main__':
    app.run(
        debug=True, # Allow verbose error reports
        port=5111 # Set custom port
    )
