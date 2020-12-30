from question import Quizzes
import sys


input_file = 'input.txt'
if len(sys.argv) > 1:
  input_file = sys.argv[1]
 
theQuiz = Quizzes(input_file)

#get rid of last job's files/folders
# theQuiz.create_export_file()
#now to output





