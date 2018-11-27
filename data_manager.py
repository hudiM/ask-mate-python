import connection
import time
import uuid

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
questions_file_name = 'question.csv'
answers_file_name = 'answer.csv'

def createDebugDatabase():
    connection.writeQuestion(questions_file_name, {'id': 0, 'submission_time': 10, 'view_number': 15, 'vote_number': 50, 'title': 'Da question', 'message': 'This is the question', 'image': 'https://cdn.frankerfacez.com/emoticon/139407/4' })
    connection.writeAnswer(answers_file_name, {'id': 0, 'submission_time': 10, 'vote_number': 15, 'question_id': 0, 'message': 'This is an answer', 'image': 'https://cdn.betterttv.net/emote/55c845ecde06d3181ad07b19/2x'})
    return


def resolveQuestionForm(form):
    form.setdefault('submission_time',time.time())
    return form


def addNewQuestion(form):
    form = resolveQuestionForm(form)
    connection.writeQuestion('question.csv', form)
    return


def appendNewQuestion(form):
    form = resolveQuestionForm(form)
    connection.addQuestion()
    return form

def resolveAnswerForm(form, qID):
    form.setdefault('id', newUUID('answer'))
    form.setdefault('question_id', qID)
    form.setdefault('vote_number', 0)
    form.setdefault('submission_time', time.asctime( time.localtime(time.time())))
    return form


def addNewAnswer(form, questionID):
    form = resolveAnswerForm(form, questionID)
    connection.addAnswer(answers_file_name, form)
    return

# mode = question/answer
def newUUID(mode):
    uniqueID = uuid.uuid1()
    while(not isUUIDExist(mode, uniqueID)):
        uniqueID = uuid.uuid1()
    return uniqueID

# mode = question/answer
def isUUIDExist(mode, uniqueID):
    if mode == 'answer':
        data = connection.readAllAnswer(answers_file_name)
        for elem in data:
            if uniqueID != elem['id']:
                return 1
    if mode == 'question':
        data = connection.readAllQuestion(questions_file_name)
        for elem in data:
            if uniqueID != elem['id']:
                return 1
    return 0

def countViews(question):
    question['view_number'] = int(question['view_number'])+1
    updateQuestion(question)
    return question

def updateQuestion(question):
    data = connection.readAllQuestion(questions_file_name)
    for elem in data:
        if elem['id'] == question['id']:
            data[data.index(elem)] = question
            break
    print(data)
    connection.updateQuestion(questions_file_name, data)
    return
