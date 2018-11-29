import csv

def readQuestion(filename, questionID):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == questionID:
                    return row
    except FileNotFoundError as err:
        print('[Error]', err)
    return 'error'


def readAllQuestion(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError as err:
        data = 'error'
        print('[Error]', err)
    return data


def createQuestionDatabase():
    try:
        with open('question.csv', 'w') as file:
            file.write('id,submission_time,view_number,vote_number,title,message,image\n')
    except FileNotFoundError as err:
        print('[Error]', err)
    return


# debug
def writeQuestion(filename, data):
    try:
        with open(filename, 'w') as file:
            file.write('id,submission_time,view_number,vote_number,title,message,image\n')
            writeFile = csv.DictWriter(file, ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message',
                                              'image'] , lineterminator='\n')
            writeFile.writerow(data)
    except FileNotFoundError as err:
        print('[Error]', err)
    return


# add question:  data = dictionary
def addQuestion(filename, data):
    try:
        with open(filename, 'a') as file:
            writeFile = csv.DictWriter(file, ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message',
                                              'image'], lineterminator='\n')
            writeFile.writerow(data)
    except FileNotFoundError as err:
        print('[Error]', err)
    return

# data = list of dictionaries [{}, {}]
def updateAllQuestions(filename, questions):
    createQuestionDatabase()
    for question in questions:
        addQuestion(filename, question)
    return

###############################################################
#                       ANSWER
###############################################################

def readAnswer(filename, answerID):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == answerID:
                    return row
    except FileNotFoundError as err:
        print('[Error]', err)
    return 'error'


def readAllAnswer(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError as err:
        data = 'error'
        print('[Error]', err)
    return data


def createAnswerDatabase():
    try:
        with open('answer.csv', 'w') as file:
            file.write('id,submission_time,vote_number,question_id,message,image\n')
    except FileNotFoundError as err:
        print('[Error]', err)
    return


def writeAnswer(filename, data):
    try:
        with open(filename, 'w') as file:
            file.write('id,submission_time,vote_number,question_id,message,image\n')
            writeFile = csv.DictWriter(file, ['id', 'submission_time', 'vote_number', 'question_id', 'message',
                                              'image'] , lineterminator='\n')
            writeFile.writerow(data)
    except FileNotFoundError as err:
        print('[Error]', err)
    return


def addAnswer(filename, data):
    try:
        with open(filename, 'a') as file:
            writeFile = csv.DictWriter(file, ['id', 'submission_time', 'vote_number', 'question_id', 'message',
                                              'image'] , lineterminator='\n')
            writeFile.writerow(data)
    except FileNotFoundError as err:
        print('[Error]', err)
    return


def updateAnswer(filename, data):
    createAnswerDatabase()
    for elem in data:
        addAnswer(filename, elem)
    return
