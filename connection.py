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
            file.write('id,submisson_time,view_number,vote_number,title,message,image\n')
    except FileNotFoundError as err:
        print('[Error]', err)
    return


def writeQuestion(filename, data):
    try:
        with open(filename, 'w') as file:
            file.write('id,submisson_time,view_number,vote_number,title,message,image\n')
            writeFile = csv.DictWriter(file, ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message',
                                              'image'] , lineterminator='\n')
            writeFile.writerow(data)
    except FileNotFoundError as err:
        print('[Error]', err)
    return


def addQuestion(filename, data):
    try:
        with open(filename, 'a') as file:
            writeFile = csv.DictWriter(file, ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message',
                                              'image'], lineterminator='\n')
            writeFile.writerow(data)
    except FileNotFoundError as err:
        print('[Error]', err)
    return
