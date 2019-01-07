import connection
from random import randint
from datetime import datetime

#       QUESTIONS
# id: A unique identifier for the question
# submission_time: The UNIX timestamp when the question was posted
# view_number: How many times this question was displayed in the single question view
# vote_number: The sum of votes this question has received
# title: The title of the question
# message: The question text
# image: The path to the image for this question

#       ANSWERS
# id: A unique identifier for the answer
# submission_time: The UNIX timestamp when the answer was posted
# vote_number: The sum of votes this answer has received
# question_id: The id of the question this answer belongs to.
# message: The answer text
# image: the path to the image for this answer

# ----------------------------------------------------------
#                   get
# ----------------------------------------------------------

def get_sort(sorting):
    sort = 'submission_time'
    direction = 'DESC'
    if sorting['direction'] == 'ASC':
        direction = 'ASC'
    if sorting['sort'] is not None:
        sort = sorting['sort']
    return sort, direction

@connection.connection_handler
def get_search_questions(cursor, search, sorting):
    sort, direction = get_sort(sorting)
    search = '%'+str(search)+'%'
    cursor.execute("SELECT question.id FROM question LEFT JOIN answer ON question.id = answer.question_id WHERE (title LIKE %s OR answer.message LIKE %s OR question.message LIKE %s);",(search,search,search))
    question_ids = cursor.fetchall()
    print(question_ids)
    if question_ids != []:
        ids = []
        for id in question_ids:
            ids.append("id='"+str(id['id'])+"'")
        ids = list(set(ids))
        sql_string = "SELECT * FROM question WHERE "
        sql_string += " OR ".join(ids)
        sql_string += 'ORDER BY {0} {1};'.format(sort, direction)
        print(sql_string)
        cursor.execute(sql_string)
        questions = cursor.fetchall()
        return questions
    return None

@connection.connection_handler
def get_all_questions(cursor, sorting):
    sort, direction = get_sort(sorting)
    cursor.execute('SELECT * FROM question ORDER BY {0} {1};'.format(sort, direction))
    return cursor.fetchall()

@connection.connection_handler
def get_five_questions(cursor, sorting):
    sort, direction = get_sort(sorting)
    cursor.execute('SELECT * FROM question ORDER BY {0} {1} LIMIT 5;'.format(sort, direction))
    return cursor.fetchall()

@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("SELECT * FROM question WHERE ID='{0}';".format(question_id))
    return cursor.fetchall()[0]

@connection.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("SELECT message, image, question_id FROM answer WHERE id={0};".format(answer_id))
    return cursor.fetchone()

@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("SELECT * FROM answer WHERE question_id='{0}' ORDER BY vote_number DESC, submission_time DESC;".format(question_id))
    return cursor.fetchall()

@connection.connection_handler
def get_comments(cursor, mode, data_id):
    if mode == 'question':
        cursor.execute("SELECT * FROM comment WHERE question_id={0};".format(data_id))
    if mode == 'answer':
        cursor.execute("SELECT * FROM comment WHERE answer_id={0};".format(data_id))
    return cursor.fetchall()

@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("SELECT * FROM comment WHERE id={0};".format(comment_id))
    return cursor.fetchone()

@connection.connection_handler
def get_latest_question_id(cursor):
    cursor.execute('SELECT id FROM question ORDER BY submission_time DESC LIMIT 1;')
    return cursor.fetchone()['id']

@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("SELECT question_id FROM answer WHERE id='{0}';".format(answer_id))
    return cursor.fetchone()['question_id']

@connection.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("SELECT question_id, answer_id FROM comment WHERE id={0}".format(comment_id))
    ids = cursor.fetchone()
    if ids['question_id'] is None:
        return get_question_id_by_answer_id(ids['answer_id'])
    return ids['question_id']

@connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute('SELECT name, color, color_mode FROM tag JOIN question_tag ON tag.id=question_tag.tag_id WHERE question_id={0}'.format(question_id))
    return cursor.fetchall()

@connection.connection_handler
def get_tags(cursor):
    cursor.execute('SELECT * FROM tag')
    return cursor.fetchall()

@connection.connection_handler
def get_tags_list(cursor):
    cursor.execute('SELECT name, color, color_mode, question_id FROM tag LEFT JOIN question_tag ON tag.id = question_tag.tag_id')
    return cursor.fetchall()

@connection.connection_handler
def get_tags_checked(cursor, question_id): # something
    cursor.execute('SELECT name, color, color_mode, id, (question_id IS NOT NULL) as checked  FROM tag LEFT JOIN question_tag ON tag.id=question_tag.tag_id AND question_id = %s ORDER BY id, question_id;', question_id)
    return cursor.fetchall()

# ----------------------------------------------------------
#                   add
# ----------------------------------------------------------

@connection.connection_handler
def new_answer(cursor, form, question_id):
    cursor.execute("INSERT INTO answer (submission_time, vote_number, question_id, message, image) VALUES ('{0}',0,'{1}', %s, %s);".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),question_id),(form['message'],form['image']))
    return

@connection.connection_handler
def new_question(cursor, form):
    cursor.execute("INSERT INTO question (submission_time, view_number, vote_number, title, message, image) VALUES ('{0}','0','0', %s, %s,%s);".format(datetime.now()),(form['title'],form['message'],form['image']))
    return get_latest_question_id()

@connection.connection_handler
def new_comment(cursor, mode, form, data_id):
    if mode == 'question':
        cursor.execute("INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count) VALUES (%s,%s,%s,%s,%s);",
                       (data_id,None,form['message'],str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),None))
    if mode == 'answer':
        cursor.execute("INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count) VALUES (%s,%s,%s,%s,%s);",
                       (None,data_id,form['message'],str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),None))
    return

@connection.connection_handler
def manage_tags(cursor, form, question_id):
    cursor.execute("DELETE FROM question_tag WHERE question_id='{0}';".format(question_id))
    for tag_id in form:
        cursor.execute("INSERT INTO question_tag (question_id, tag_id) VALUES ('{0}','{1}') ON CONFLICT DO NOTHING;".format(question_id, tag_id))
    return

@connection.connection_handler
def add_tag(cursor, form):
    cursor.execute("INSERT INTO tag (name, color, color_mode) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;", (form['name'],form['color'], None))
    return

# ----------------------------------------------------------
#                   edit
# ----------------------------------------------------------

@connection.connection_handler
def edit_question(cursor, form, question_id):
    cursor.execute("UPDATE question SET submission_time='{0}',title=%s,message=%s,image=%s WHERE id={1};".format(
        str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), question_id),(form['title'], form['message'], form['image']))
    return

@connection.connection_handler
def edit_answer(cursor, form, answer_id):
    cursor.execute("UPDATE answer SET submission_time='{0}',message=%s,image=%s WHERE id={1};".format(
        str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),answer_id),(form['message'],form['image']))
    return get_question_id_by_answer_id(answer_id)

@connection.connection_handler
def edit_comment(cursor, form, comment_id):
    cursor.execute("UPDATE comment SET message=%s, submission_time=%s WHERE id={0};".format(comment_id),(form['message'],str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
    return get_question_id_by_comment_id(comment_id)

@connection.connection_handler
def edit_tag(cursor, form, tag_id):
    cursor.execute("UPDATE tag SET name=%s, color=%s, color_mode=%s WHERE id={0}".format(tag_id), (form['name'], form['color'], None))
    return

# ----------------------------------------------------------
#                   delete
# ----------------------------------------------------------

@connection.connection_handler
def delete_question(cursor, question_id):
    for answer in get_answers_by_question_id(question_id):
        cursor.execute('DELETE FROM comment WHERE answer_id={0}'.format(answer['id']))
    cursor.execute("DELETE FROM question_tag WHERE question_id={0};DELETE FROM comment WHERE question_id={0}; DELETE FROM answer WHERE question_id='{0}'; DELETE FROM question WHERE id='{0}';".format(str(question_id)))
    return

@connection.connection_handler
def delete_answer(cursor, answer_id):
    question_id = get_question_id_by_answer_id(answer_id)
    cursor.execute("DELETE FROM comment WHERE answer_id={0};DELETE FROM answer WHERE id='{0}';".format(str(answer_id)))
    return question_id

@connection.connection_handler
def delete_comment(cursor, comment_id):
    question_id = get_question_id_by_comment_id(comment_id)
    cursor.execute("DELETE FROM comment WHERE id='{0}';".format(str(comment_id)))
    return question_id

@connection.connection_handler
def delete_tag(cursor,tag_id):
    cursor.execute("DELETE FROM question_tag WHERE tag_id={0}; DELETE FROM tag WHERE id={0};".format(tag_id))
    return
# ----------------------------------------------------------
#                   vote
# ----------------------------------------------------------

# mode = answer | question
@connection.connection_handler
def vote(cursor, mode, direction, data_id):
    if direction == 'up':
        cursor.execute("UPDATE {0} SET vote_number=vote_number+1 WHERE id={1};".format(mode, data_id))
    if direction == 'down':
        cursor.execute("UPDATE {0} SET vote_number=vote_number-1 WHERE id={1};".format(mode, data_id))
    if mode == 'answer':
        question_id = get_question_id_by_answer_id(data_id)
        page_view_counter('down', question_id)
        return question_id
    page_view_counter('down', data_id)
    return

# ----------------------------------------------------------
#                   views
# ----------------------------------------------------------

@connection.connection_handler
def page_view_counter(cursor, mode, question_id):
    if mode == 'up':
        cursor.execute("UPDATE question SET view_number=view_number+1 WHERE id={0};".format(question_id))
    if mode == 'down':
        cursor.execute("UPDATE question SET view_number=view_number-1 WHERE id={0};".format(question_id))
    return
