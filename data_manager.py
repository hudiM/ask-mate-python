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
    question_id = newUUID('question')
    form.setdefault('id', question_id)
    form.setdefault('submission_time', time.time())
    form.setdefault('view_number', 0)
    form.setdefault('vote_number', 0)
    return form, question_id


def addNewQuestion(form):
    form, question_id = resolveQuestionForm(form)
    connection.addQuestion('question.csv', form)
    return question_id


def convertTime(form):
    form['submission_time'] = time.asctime(time.localtime(float(form['submission_time'])))
    return form


# returns answers for given question
def getAnswersForQuestion(filename, question_id):
    answers = connection.readAllAnswer(filename)
    answers = [convertTime(answer) for answer in answers if answer['question_id'] == question_id]
    return answers


def resolveAnswerForm(form, question_id):
    form.setdefault('id', newUUID('answer'))
    form.setdefault('question_id', question_id)
    form.setdefault('vote_number', 0)
    form.setdefault('submission_time', time.time())
    return form


def addNewAnswer(form, question_id):
    print('answer')
    form = resolveAnswerForm(form, question_id)
    print('form done')
    connection.addAnswer(answers_file_name, form)
    return


# generates a new ID to be inserted in database, mode checks if it exist in given database
# mode = question/answer
def newUUID(mode):
    unique_id = uuid.uuid1()
    while(not isUUIDExist(mode, unique_id)):
        unique_id = uuid.uuid1()
    return unique_id

def isUUIDExist(mode, unique_id):
    if mode == 'answer':
        answers = connection.readAllAnswer(answers_file_name)
        if answers == []:
            return 1
        for answer in answers:
            if unique_id != answer['id']:
                return 1
    if mode == 'question':
        questions = connection.readAllQuestion(questions_file_name)
        if questions == []:
            return 1
        for question in questions:
            if unique_id != question['id']:
                return 1
    return 0


# adds one to the question's view count
def countViews(question):
    question['view_number'] = int(question['view_number'])+1
    updateQuestion(question)
    return question

def voteCountViewsFix(question):
    question['view_number'] = int(question['view_number'])-1
    updateQuestion(question)
    return question


# switches 1 line in question database with the new given question
def updateQuestion(question):
    questions = connection.readAllQuestion(questions_file_name)
    for question in questions:
        if question['id'] == question['id']:
            questions[questions.index(question)] = question
            break
    connection.updateQuestion(questions_file_name, questions)
    return


# ----------------------------------------------------------
#                   deletes
# ----------------------------------------------------------
def deleteQuestion(question_id):
    question = connection.readQuestion(questions_file_name, question_id)
    questions = connection.readAllQuestion(questions_file_name)
    questions.remove(question)
    connection.updateQuestion(questions_file_name, questions)
    deleteAnswersByQuestion(question_id)
    return

def deleteAnswersByQuestion(question_id):
    answers = connection.readAllAnswer(answers_file_name)
    answers = [answer for answer in answers if answer['question_id'] != question_id]
    connection.updateAnswer(answers_file_name, answers)
    return


def deleteAnswer(answer_id):
    answer = connection.readAnswer(answers_file_name, answer_id)
    answers = connection.readAllAnswer(answers_file_name)
    answers.remove(answer)
    connection.updateAnswer(answers_file_name, answers)
    return answer['question_id']


# ----------------------------------------------------------
#                   answer voting
# ----------------------------------------------------------
def voteAnswerSend(answer):
    answers = connection.readAllAnswer(answers_file_name)
    for answer in answers:
        if answer['id'] == answer['id']:
            answers[answers.index(answer)] = answer
    connection.updateAnswer(answers_file_name, answers)
    return

def voteAnswerUp(answer_id):
    answer = connection.readAnswer(answers_file_name, answer_id)
    answer['vote_number'] = int(answer['vote_number'])+1
    voteAnswerSend(answer)
    voteCountViewsFix(connection.readQuestion(questions_file_name, answer['question_id']))
    return answer['question_id']

def voteAnswerDown(answer_id):
    answer = connection.readAnswer(answers_file_name, answer_id)
    answer['vote_number'] = int(answer['vote_number'])-1
    voteAnswerSend(answer)
    voteCountViewsFix(connection.readQuestion(questions_file_name, answer['question_id']))
    return answer['question_id']


# ----------------------------------------------------------
#                   edit question
# ----------------------------------------------------------
def editQuestion(form, question_id):
    question = connection.readQuestion(questions_file_name, question_id)
    questions = connection.readAllAnswer(questions_file_name)
    number = questions.index(question)
    question['title'] = form['title']
    question['message'] = form['message']
    question['image'] = form['image']
    questions[number] = question
    connection.updateQuestion(questions_file_name, questions)
    return
