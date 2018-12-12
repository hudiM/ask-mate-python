from flask import Flask, render_template, redirect, request, url_for
import data_manager
import connection

app = Flask(__name__)


# ------------------------
#           main
# ------------------------

@app.route('/')
def route_index():
    questions = data_manager.get_five_questions()
    questions = sorted(questions,key=lambda k: k['submission_time'], reverse=True)
    tags = data_manager.get_tags()
    return render_template('list.html', questions=questions, tags=tags, index=True)

@app.route('/list')
def route_list():
    questions = data_manager.get_all_questions()
    tags = data_manager.get_tags()
    return render_template('list.html', questions = questions, tags=tags)

@app.route('/question/<question_id>/edit-tag', methods=['GET','POST'])
def route_add_tag(question_id):
    if request.method == 'POST':
        data_manager.add_tag(request.form.getlist('tag'), question_id)
        return redirect(url_for('route_question', question_id=question_id))
    return render_template('add_tag.html')

@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        question_id = data_manager.new_question(request.form)
        return redirect('/question/' + str(question_id))
    return render_template('new_question.html', question = None)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.page_view_counter('up', question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comments = data_manager.get_comments('question',question_id)
    tags = data_manager.get_tags_by_question_id(question_id)
    answer_comments = []
    for answer in answers:
        answer_comments.append(data_manager.get_comments('answer', answer['id']))
    return render_template('question.html', question=question, answers = answers, question_comments=question_comments, answer_comments=answer_comments, tags=tags)


@app.route('/question/<question_id>/delete')
def route_question_delete(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def route_answer_delete(answer_id):
    question_id = data_manager.delete_answer(answer_id)
    return redirect('/question/'+ str(question_id))

@app.route('/comment/<comment_id>/delete')
def route_comment_delete(comment_id):
    question_id = data_manager.delete_comment(comment_id)
    return redirect('/question/'+ str(question_id))

@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_answer_edit(answer_id):
    if request.method == 'POST':
        question_id = data_manager.edit_answer(request.form, answer_id)
        return redirect('/question/'+str(question_id))
    answer = data_manager.get_answer(answer_id)
    return render_template('new_answer.html',answer=answer)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'POST':
        data_manager.edit_question(request.form, question_id)
        return redirect('/question/'+question_id)
    question = data_manager.get_question_by_id(question_id)
    return render_template('new_question.html', question = question)

@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_comment_edit(comment_id):
    if request.method == 'POST':
        question_id = data_manager.edit_comment(request.form, comment_id)
        return redirect('/question/'+str(question_id))
    comment = data_manager.get_comment_by_id(comment_id)
    return render_template('new_comment.html', comment=comment)

@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        data_manager.new_answer(request.form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', question_id = question_id, answer=None)

@app.route('/question/<question_id>/new-comment', methods=['GET','POST'])
def route_new_comment_question(question_id):
    if request.method == 'POST':
        data_manager.new_comment('question', request.form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_comment.html', comment=None)

@app.route('/answer/<answer_id>/new-comment', methods=['GET','POST'])
def route_new_comment_answer(answer_id):
    if request.method == 'POST':
        data_manager.new_comment('answer', request.form, answer_id)
        return redirect('/question/'+str(data_manager.get_question_id_by_answer_id(answer_id)))
    return render_template('new_comment.html', comment=None)


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
