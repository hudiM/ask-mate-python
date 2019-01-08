from flask import Flask, render_template, redirect, request, url_for, session, make_response, escape
import data_manager

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# ------------------------
#           main
# ------------------------

# def login_data(func):
#     def func_wrapper(logindata):
#         if 'username' in session:
#             logindata = {'okey': True, 'username': escape(session['username'])}
#         else:
#             logindata = {'okey': False}
#     return func_wrapper(logindata)

# ------------------------
#           main
# ------------------------


@app.route('/')
# @login_data
def route_index():
    if 'username' in session:
        logindata = {'okey': True, 'username': escape(session['username'])}
    else:
        logindata = {'okey': False}
    sorting = {'direction': request.args.get('direction'),'sort': request.args.get('sort')}
    questions = data_manager.get_five_questions(sorting)
    tags = data_manager.get_tags_list()
    return render_template('list.html', questions=questions, tags=tags, index=True, sorting=sorting, logindata = logindata)

@app.route('/list')
def route_list():
    sorting = {'direction': request.args.get('direction'),'sort': request.args.get('sort')}
    questions = data_manager.get_all_questions(sorting)
    tags = data_manager.get_tags_list()
    return render_template('list.html', questions = questions, tags=tags, sorting=sorting)

@app.route('/search-result')
def route_search():
    sorting = {'direction': request.args.get('direction'),'sort': request.args.get('sort')}
    questions = data_manager.get_search_questions(request.args.get('search'),sorting)
    tags = data_manager.get_tags_list()
    return render_template('list.html',questions = questions, tags=tags, sorting=sorting)

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

# ----------------------------------------------------------
#                   user
# ----------------------------------------------------------

@app.route('/register', methods=('GET','POST'))
def route_user_register():
    if request.method == 'POST':
        data_manager.user_register(request.form['username'],request.form['password'])
        return redirect('/')
    return render_template('registration.html')

@app.route('/login', methods=('GET','POST'))
def route_user_login():
    if 'username' in session:
        logindata = {'okey': True, 'username': escape(session['username'])}
    else:
        logindata = {'okey': False}
    if request.method == 'POST':
        # response = make_response(redirect('/'))
        if data_manager.user_login(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            return redirect('/')
    return render_template('registration.html', logindata=logindata)

@app.route('/logout')
def route_user_logout():
    session.pop('username', None)
    return redirect('/')

# ----------------------------------------------------------
#                   tags
# ----------------------------------------------------------

@app.route('/question/<question_id>/edit-tag', methods=['GET','POST'])
def route_edit_tags(question_id):
    if request.method == 'POST':
        data_manager.manage_tags(request.form.getlist('tag'), question_id)
        return redirect(url_for('route_question', question_id=question_id))
    tags = data_manager.get_tags_checked(question_id)
    return render_template('add_tag.html', tags=tags)

@app.route('/new-tag', methods=['GET','POST'])
def route_add_tag():
    if request.method == 'POST':
        data_manager.add_tag(request.form)
        return redirect(url_for('route_add_tag'))
    return render_template('new_tag.html')

@app.route('/tag/<tag_id>/edit', methods=['GET','POST'])
def route_edit_tag(tag_id):
    if request.method == 'POST':
        data_manager.edit_tag(request.form, tag_id)
        return redirect('/')
    return render_template('new_tag.html')

@app.route('/tag/<tag_id>/delete')
def route_delete_tag(tag_id):
    data_manager.delete_tag(tag_id)
    return redirect('/')

# ----------------------------------------------------------
#                   question
# ----------------------------------------------------------

@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        question_id = data_manager.new_question(request.form)
        return redirect('/question/' + str(question_id))
    return render_template('new_question.html', question = None)

@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'POST':
        data_manager.edit_question(request.form, question_id)
        return redirect('/question/'+question_id)
    question = data_manager.get_question_by_id(question_id)
    return render_template('new_question.html', question = question)

@app.route('/question/<question_id>/delete')
def route_question_delete(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')

# ----------------------------------------------------------
#                   answer
# ----------------------------------------------------------

@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        data_manager.new_answer(request.form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', question_id = question_id, answer=None)

@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_answer_edit(answer_id):
    if request.method == 'POST':
        question_id = data_manager.edit_answer(request.form, answer_id)
        return redirect('/question/'+str(question_id))
    answer = data_manager.get_answer(answer_id)
    return render_template('new_answer.html',answer=answer)

@app.route('/answer/<answer_id>/delete')
def route_answer_delete(answer_id):
    question_id = data_manager.delete_answer(answer_id)
    return redirect('/question/'+ str(question_id))

# ----------------------------------------------------------
#                   comments
# ----------------------------------------------------------

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

@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_comment_edit(comment_id):
    if request.method == 'POST':
        question_id = data_manager.edit_comment(request.form, comment_id)
        return redirect('/question/'+str(question_id))
    comment = data_manager.get_comment_by_id(comment_id)
    return render_template('new_comment.html', comment=comment)

@app.route('/comment/<comment_id>/delete')
def route_comment_delete(comment_id):
    question_id = data_manager.delete_comment(comment_id)
    return redirect('/question/'+ str(question_id))

# ----------------------------------------------------------
#                   vote
# ----------------------------------------------------------

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

# ----------------------------------------------------------
#                   server
# ----------------------------------------------------------

if __name__ == '__main__':
    app.run(
        debug=True, # Allow verbose error reports
        port=5111 # Set custom port
    )
