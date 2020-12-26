from question import FillQuestion, Quizzes
from pprint import pprint



theQuiz = Quizzes("input.txt")

#get rid of last job's files/folders
theQuiz.cleanup()
theQuiz.create_export_file()
#now to output





