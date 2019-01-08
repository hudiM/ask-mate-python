from flask import Flask, render_template, redirect, request, url_for, session, make_response, escape
import data_manager

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def check_login():
    if 'username' in session:
        login_data = {'okey': True, 'username': escape(session['username'])}
    else:
        login_data = {'okey': False}
    return login_data

# ------------------------
#           main
# ------------------------


@app.route('/')
def route_index():
    login_data = check_login()
    sorting = {'direction': request.args.get('direction'),'sort': request.args.get('sort')}
    questions = data_manager.get_five_questions(sorting)
    tags = data_manager.get_tags_list()
    return render_template('list.html', questions=questions, tags=tags, index=True, sorting=sorting, login_data = login_data)

@app.route('/list')
def route_list():
    login_data = check_login()
    sorting = {'direction': request.args.get('direction'),'sort': request.args.get('sort')}
    questions = data_manager.get_all_questions(sorting)
    tags = data_manager.get_tags_list()
    return render_template('list.html', questions = questions, tags=tags, sorting=sorting, login_data=login_data)

@app.route('/search-result')
def route_search():
    login_data = check_login()
    sorting = {'direction': request.args.get('direction'),'sort': request.args.get('sort')}
    questions = data_manager.get_search_questions(request.args.get('search'),sorting)
    tags = data_manager.get_tags_list()
    return render_template('list.html',questions = questions, tags=tags, sorting=sorting, login_data=login_data)

@app.route('/question/<question_id>')
def route_question(question_id):
    login_data = check_login()
    question = data_manager.get_question_by_id(question_id)
    data_manager.page_view_counter('up', question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comments = data_manager.get_comments('question',question_id)
    tags = data_manager.get_tags_by_question_id(question_id)
    answer_comments = []
    for answer in answers:
        answer_comments.append(data_manager.get_comments('answer', answer['id']))
    return render_template('question.html', question=question, answers = answers, question_comments=question_comments, answer_comments=answer_comments, tags=tags, login_data=login_data)

# ----------------------------------------------------------
#                   user
# ----------------------------------------------------------

@app.route('/users')
def route_user_list():
    login_data = check_login()
    users = data_manager.get_all_user()
    return render_template('users.html', login_data=login_data, users=users)


@app.route('/register', methods=('GET','POST'))
def route_user_register():
    login_data = check_login()
    if request.method == 'POST':
        data_manager.user_register(request.form['username'],request.form['password'])
        return redirect('/')
    return render_template('registration.html', login_data=login_data)

@app.route('/login', methods=('GET','POST'))
def route_user_login():
    login_data = check_login()
    if request.method == 'POST':
        if data_manager.user_login(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            return redirect('/')
    return render_template('registration.html', login_data=login_data)

@app.route('/logout')
def route_user_logout():
    session.pop('username', None)
    return redirect('/')

# ----------------------------------------------------------
#                   tags
# ----------------------------------------------------------
@app.route('/tags')
def route_get_tags():
    login_data = check_login()
    tags = data_manager.get_tags_with_question_number()
    return render_template('tags.html', tags=tags, login_data=login_data)

@app.route('/question/<question_id>/edit-tag', methods=['GET','POST'])
def route_edit_tags(question_id):
    login_data = check_login()
    if request.method == 'POST':
        data_manager.manage_tags(request.form.getlist('tag'), question_id)
        return redirect(url_for('route_question', question_id=question_id))
    tags = data_manager.get_tags_checked(question_id)
    return render_template('add_tag.html', tags=tags, login_data=login_data)

@app.route('/new-tag', methods=['GET','POST'])
def route_add_tag():
    login_data = check_login()
    if request.method == 'POST':
        data_manager.add_tag(request.form)
        return redirect(url_for('route_add_tag'))
    return render_template('new_tag.html', login_data=login_data)

@app.route('/tag/<tag_id>/edit', methods=['GET','POST'])
def route_edit_tag(tag_id):
    login_data = check_login()
    if request.method == 'POST':
        data_manager.edit_tag(request.form, tag_id)
        return redirect('/')
    return render_template('new_tag.html', login_data=login_data)

@app.route('/tag/<tag_id>/delete')
def route_delete_tag(tag_id):
    data_manager.delete_tag(tag_id)
    return redirect('/')

# ----------------------------------------------------------
#                   question
# ----------------------------------------------------------

@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    login_data = check_login()
    if request.method == 'POST':
        question_id = data_manager.new_question(request.form)
        return redirect('/question/' + str(question_id))
    return render_template('new_question.html', question = None, login_data=login_data)

@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    login_data = check_login()
    if request.method == 'POST':
        data_manager.edit_question(request.form, question_id)
        return redirect('/question/'+question_id)
    question = data_manager.get_question_by_id(question_id)
    return render_template('new_question.html', question = question, login_data=login_data)

@app.route('/question/<question_id>/delete')
def route_question_delete(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')

# ----------------------------------------------------------
#                   answer
# ----------------------------------------------------------

@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def route_new_answer(question_id):
    login_data = check_login()
    if request.method == 'POST':
        data_manager.new_answer(request.form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', question_id = question_id, answer=None, login_data=login_data)

@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_answer_edit(answer_id):
    login_data = check_login()
    if request.method == 'POST':
        question_id = data_manager.edit_answer(request.form, answer_id)
        return redirect('/question/'+str(question_id))
    answer = data_manager.get_answer(answer_id)
    return render_template('new_answer.html',answer=answer, login_data=login_data)

@app.route('/answer/<answer_id>/delete')
def route_answer_delete(answer_id):
    question_id = data_manager.delete_answer(answer_id)
    return redirect('/question/'+ str(question_id))

# ----------------------------------------------------------
#                   comments
# ----------------------------------------------------------

@app.route('/question/<question_id>/new-comment', methods=['GET','POST'])
def route_new_comment_question(question_id):
    login_data = check_login()
    if request.method == 'POST':
        data_manager.new_comment('question', request.form, question_id)
        return redirect('/question/'+str(question_id))
    return render_template('new_comment.html', comment=None, login_data=login_data)

@app.route('/answer/<answer_id>/new-comment', methods=['GET','POST'])
def route_new_comment_answer(answer_id):
    login_data = check_login()
    if request.method == 'POST':
        data_manager.new_comment('answer', request.form, answer_id)
        return redirect('/question/'+str(data_manager.get_question_id_by_answer_id(answer_id)))
    return render_template('new_comment.html', comment=None, login_data=login_data)

@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_comment_edit(comment_id):
    login_data = check_login()
    if request.method == 'POST':
        question_id = data_manager.edit_comment(request.form, comment_id)
        return redirect('/question/'+str(question_id))
    comment = data_manager.get_comment_by_id(comment_id)
    return render_template('new_comment.html', comment=comment, login_data=login_data)

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
