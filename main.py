#Step 1, edit the input.txt to include your quizzes and questions
#step 2, click Run at the top
#step 3, click the 3 dots above files and download zip
#step 4, retrieve the newquiz.zip
#step 5 import into your course as a QTI object
#all done
from question import Quizzes
import sys


input_file = 'input.txt'
if len(sys.argv) > 1:
  input_file = sys.argv[1]
 
theQuiz = Quizzes(input_file)





