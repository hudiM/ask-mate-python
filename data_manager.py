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

@connection.connection_handler
def get_all_questions(cursor):
    sql_string = 'SELECT * FROM "question";'
    cursor.execute(sql_string)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_question_by_id(cursor, question_id):
    sql_string = 'SELECT * FROM "question" WHERE ID='+question_id+';'
    cursor.execute(sql_string)
    question = cursor.fetchall()
    return question

@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    sql_string = 'SELECT * FROM "answer" WHERE question_id='+question_id+';'
    cursor.execute(sql_string)
    question = cursor.fetchall()
    return question

# ----------------------------------------------------------
#                   add
# ----------------------------------------------------------

@connection.connection_handler
def new_answer(cursor, form, question_id):
    sql_string = generate_answer_form(form, question_id)
    print(sql_string)
    while(1):
        try:
            cursor.execute(sql_string)
            break
        except:
            sql_string = generate_answer_form(form, question_id)
    return

def generate_answer_form(form, question_id):
    sql_string = "INSERT INTO answer (id, submission_time, vote_number, question_id, message, image) VALUES ('"+\
                 str(randint(0, 999999))+"','"+\
                 str(datetime.now())+"',"+\
                 "'0','"+\
                 question_id+"','"+\
                 form['message']+"','"+\
                 form['image']+"');"
    return sql_string

# ----------------------------------------------------------
#                   edit
# ----------------------------------------------------------

@connection.connection_handler
def edit_question(cursor, form, question_id):
    sql_string = 'UPDATE question SET ' + \
                 "submission_time='" + str(datetime.now()) +\
                 "', title='" + form['title'] +\
                 "', message='" + form['message'] +\
                 "', image='" + form['image'] +\
                 "' WHERE id=" + question_id + ';'
    print(sql_string)
    cursor.execute(sql_string)
    return
