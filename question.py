from random import randint
import os
import shutil
from xml_functions import start_section, question_section, end_section, manifest_file, assessment_file
class Quizzes:
  
  def __init__(self,filepath ):
    self.quizzes = []
    # self.questions = self.import_file(filepath)
    self.import_file(filepath)
    # self.idents = self.get_idents()


  def import_file(self,filepath):
    my_file = open(filepath,"r")

    lines = my_file.readlines()
    stripped_lines = []
    for line in lines:
      stripped_lines.append(line.strip())

    quizzes = []
    quiz = {}
    question = {}
    quiz["questions"] = []
    question['text'] = []
    question['answers'] = []
    question["feedback"] = []
    count = 0
    for line in stripped_lines:
      
      if line == "######":
        if count == 5:
          quiz["questions"].append(question)
          question = {}
          question['text'] = []
          question['answers'] = []
          question["feedback"] = []
        
        count=0
        quizzes.append(quiz)
        quiz = {}
        quiz["questions"] = []
      elif line == "###":
        if count == 5:
          quiz["questions"].append(question)
          question = {}
          question['text'] = []
          question['answers'] = []
          question["feedback"] = []
          count=1
          continue

        count += 1
      else:
        if count == 0:
          quiz["title"] = line
        else:
          if count == 1:
            question["title"] = line
          if count == 2:
            question["type"] = line
          if count == 3:
            question["text"].append(line)
          if count == 4:
            question["answers"].append(line)
          if count == 5:
            question["feedback"].append(line)

    for quiz in quizzes:
      self.quizzes.append(Quiz(quiz))

    self.create_files()

  def create_files(self):
    # Delete old files
    self.cleanup()
    # Create the folder to house the files
    if not os.path.exists('files'):
      os.mkdir("files")

    # Create non_cc_assessment folder  
    # if not os.path.exists('files/non_cc_assessment'):
    #   os.mkdir("files/non_cc_assessment")

    #Create and fill the manifest file
    myfile = open("files/imsmanifest.xml", "w")
    myfile.write(manifest_file(self.quizzes))
    myfile.close()

    for quiz in self.quizzes:
      # Create the folder to hold the quiz files
      os.mkdir(f"files/{quiz.guid}")
      myfile = open(f"files/{quiz.guid}/{quiz.guid}.xml","w")

      #Write the quiz file
      myfile.write(start_section(quiz))
      for question in quiz.questions:
        myfile.write(question_section(question))
      myfile.write(end_section())
      myfile.close()

      #Write the assessment meta file
      myfile = open(f"files/{quiz.guid}/assessment_meta.xml","w")
      myfile.write(assessment_file(quiz))
      myfile.close()
    
    shutil.make_archive("newquiz", 'zip', 'files')

  def cleanup(self):
    my_dir = os.path.dirname(os.path.realpath(__file__))
    my_dir = my_dir+"/files"

    for item in os.walk(my_dir):
      if  item[0].find("g8ce2009") >= 0:
        try:
          shutil.rmtree(item[0])
          print(item[0], "removed")
        except OSError as e:
          print("Error: %s : %s" % (dir_path, e.strerror))

class Quiz:
  identifier = 'g8ce2009aaab3283573f3ef0ef1'

  def __init__(self, quiz):
    self.guid = Quiz.identifier + self.gen_guid()
    self.title = quiz["title"]
    self.questions = self.get_questions(quiz)

  def get_questions(self, quiz):
    questions = []
    for question in quiz["questions"]:
      questions.append(Question(question))
    
    return questions

  def gen_guid(self):
    guid = ""
    for i in range(0,6):
      num = randint(0,15)
      if(num <= 9):
        num += 48
      else:
        num += 87
      guid += chr(num)
    return guid

class Question:
  def __init__(self, question):
    self.title = question["title"]
    self.text = question["text"]
    self.points = 0
    self.type = self.get_type(question["type"])
    self.answers = self.get_answers(question["answers"])
    self.answer_ids = self.get_answer_ids()
    self.feedback = question["feedback"]
    self.assign_point_weights()

  def get_answers(self, answers):
    answer_return = []
    for answer in answers:
      answer_return.append(Answer(answer.split("~")))
    
    return answer_return

  def get_type(self, question_type):
    if question_type == 'multiblank':
      self.points = 20
      return 'fill_in_multiple_blanks_question'
    elif question_type == 'multiselect':
      self.points = 1
      return 'multiple_dropdowns_question'
    elif question_type == 'multichoice':
      self.points = 5
      return 'multiple_choice_question'
    
    return ''
  
  def get_answer_ids(self):
    ids = '' 
    for answer in self.answers:
      for choice in answer.choices:
        ids += f'{choice.ident},'
    
    return ids[:-1]

  def assign_point_weights(self):
    for answer in self.answers:
      answer.point_weight = 100 / len(self.answers)

class Answer:

  def __init__(self, answer):
    self.text = answer[0]
    self.choices = self.get_choices(answer[1:])
    self.correct_ident = self.choices[0].ident
    self.point_weight = 0

  def get_choices(self, choices):
    choice_return = []
    for choice in choices:
      choice_return.append(Choice(choice))
    
    return choice_return
    
class Choice:
  identifier = 100
  def __init__(self, choice):
    self.ident = Choice.identifier
    self.text = choice
    Choice.identifier += 1