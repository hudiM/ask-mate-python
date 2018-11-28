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
    connection.createQuestionDatabase()
    connection.createAnswerDatabase()
    connection.addQuestion(questions_file_name, {'id': 0, 'submission_time': '1543395761.9055753', 'view_number': 15, 'vote_number': 50, 'title': 'Da question', 'message': 'This is the question', 'image': 'https://cdn.betterttv.net/emote/5b77ac3af7bddc567b1d5fb2/2x' })
    connection.addQuestion(questions_file_name, {'id': 1, 'submission_time': '1563395761.9055753', 'view_number': 5, 'vote_number': 25, 'title': 'Wut', 'message': 'FeelsGoodMan', 'image': 'https://cdn.betterttv.net/emote/56c2cff2d9ec6bf744247bf1/2x' })
    connection.addQuestion(questions_file_name, {'id': 2, 'submission_time': '1523395761.9055753', 'view_number': 5, 'vote_number': 25, 'title': 'EZ', 'message': 'EZy', 'image': 'https://cdn.betterttv.net/emote/5b1740221c5a6065a7bad4b5/2x' })
    connection.addAnswer(answers_file_name, {'id': 0, 'submission_time': '1543395761.9055753', 'vote_number': 15, 'question_id': 0, 'message': 'This is an answer', 'image': 'https://cdn.betterttv.net/emote/55c845ecde06d3181ad07b19/2x'})
    connection.addAnswer(answers_file_name, {'id': 1, 'submission_time': '1543395761.9055753', 'vote_number': 5, 'question_id': 0, 'message': 'This is more answer', 'image': 'https://cdn.betterttv.net/emote/5678a310bf317838643c8188/2x'})
    connection.addAnswer(answers_file_name, {'id': 2, 'submission_time': '1543395761.9055753', 'vote_number': 5, 'question_id': 1, 'message': 'Yeaaa boiii', 'image': 'https://cdn.betterttv.net/emote/5a76a1f170858a32e83d3fc4/2x'})
    return


def resolveQuestionForm(form):
    form.setdefault('submission_time',time.time())
    return form


def addNewQuestion(form):
    form = resolveQuestionForm(form)
    connection.writeQuestion('question.csv', form)
    return


def convertTime(data):
    data['submission_time'] = time.asctime(time.localtime(float(data['submission_time'])))
    return data


# returns answers for given question
def getAnswersForQuestion(filename ,questionID):
    answers = connection.readAllAnswer(filename)
    answers = [convertTime(answer) for answer in answers if answer['question_id'] == questionID]
    return answers


def resolveAnswerForm(form, qID):
    form.setdefault('id', newUUID('answer'))
    form.setdefault('question_id', qID)
    form.setdefault('vote_number', 0)
    form.setdefault('submission_time', time.time())
    return form


def addNewAnswer(form, questionID):
    form = resolveAnswerForm(form, questionID)
    connection.addAnswer(answers_file_name, form)
    return


# generates a new ID to be inserted in database, mode checks if it exist in given database
# mode = question/answer
def newUUID(mode):
    uniqueID = uuid.uuid1()
    while(not isUUIDExist(mode, uniqueID)):
        uniqueID = uuid.uuid1()
    return uniqueID

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


# adds one to the question's view count
def countViews(question):
    question['view_number'] = int(question['view_number'])+1
    updateQuestion(question)
    return question


# switches 1 line in question database with the new given question
def updateQuestion(question):
    data = connection.readAllQuestion(questions_file_name)
    for elem in data:
        if elem['id'] == question['id']:
            data[data.index(elem)] = question
            break
    connection.updateQuestion(questions_file_name, data)
    return
