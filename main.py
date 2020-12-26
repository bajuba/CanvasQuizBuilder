from question import FillQuestion, Quizzes
from pprint import pprint
import zipfile
import shutil




theQuiz = Quizzes("multiselect_multiq_format.txt")

#get rid of last job's files/folders
theQuiz.cleanup()
theQuiz.create_export_file()
#now to output





