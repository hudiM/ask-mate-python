import connection
import time

#       QUESTIONS
# id: A unique identifier for the question
# submisson_time: The UNIX timestamp when the question was posted
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
answers_file_name = 'answers.csv'

def test():
    return


def resolveQuestionForm(form):
    form.setdefault('submisson_time',time.time())
    return form


def addNewQuestion(form):
    form = resolveQuestionForm(form)
    connection.writeQuestion('question.csv', form)
    return
