import connection
import time

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
# # submission_time: The UNIX timestamp when the answer was posted
# # vote_number: The sum of votes this answer has received
# # question_id: The id of the question this answer belongs to.
# # message: The answer text
# # image: the path to the image for this answer
questions_file_name = 'question.csv'
answers_file_name = 'answer.csv'

def createDebugDatabase():
    connection.writeQuestion(questions_file_name, {'id': 0, 'submission_time': 10, 'view_number': 15, 'vote_number': 50, 'title': 'Da question', 'message': 'This is the question', 'image': 'https://cdn.frankerfacez.com/emoticon/139407/4' })
    connection.writeAnswer(answers_file_name, {'id': 0, 'submission_time': 10, 'vote_number': 15, 'question_id': 0, 'message': 'This is an answer', 'image': 'image.png'})
    return


def resolveQuestionForm(form):
    form.setdefault('submission_time',time.time())
    return form


def addNewQuestion(form):
    form = resolveQuestionForm(form)
    connection.writeQuestion('question.csv', form)
    return


def resolveAnswerForm(form, qID):
    form.setdefault('id', 1)
    form.setdefault('question_id', qID)
    form.setdefault('vote_number', 0)
    form.setdefault('submission_time', time.asctime( time.localtime(time.time())))
    return form


def addNewAnswer(form, questionID):
    form = resolveAnswerForm(form, questionID)
    print(form)
    connection.addAnswer(answers_file_name, form)
    return
