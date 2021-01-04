from random import randint
import os
import shutil
from xml_functions import start_section, question_section, end_section, manifest_file, assessment_file
class Quizzes:
  
  def __init__(self,filepath ):
    self.quizzes = []
    self.import_file(filepath)

  def import_file(self,filepath):
    my_file = open(filepath,"r")

    lines = my_file.readlines()
    stripped_lines = []
    for line in lines:
      if "\n" in line:
        stripped_lines.append(line[:-1])
      else:
        stripped_lines.append(line)

    quizzes = []
    quiz = {}
    question = {}
    quiz["questions"] = []
    quiz["options"] = []
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
        quiz["options"] = []
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
          quiz["options"].append(line)
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
      new_quiz = Quiz(quiz)
      self.quizzes.append(new_quiz)

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
    mydir = os.path.dirname(os.path.realpath(__file__))
    myfile = open("files/imsmanifest.xml", "w")
    myfile.write(manifest_file(self.quizzes))
    myfile.close()
    print(f"{mydir}\\files\\imsmanifest.xml created")

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
      print(f"{mydir}\\files\\{quiz.guid}\\{quiz.guid}.xml created")

      #Write the assessment meta file
      myfile = open(f"files/{quiz.guid}/assessment_meta.xml","w")
      myfile.write(assessment_file(quiz))
      myfile.close()
      print(f"{mydir}\\files\\{quiz.guid}\\assessment_meta.xml created")
    
    shutil.make_archive("newquiz", 'zip', 'files')
    print(f"{mydir}\\newquiz.zip created")

  def cleanup(self):
    my_dir = os.path.dirname(os.path.realpath(__file__))
    my_dir = my_dir+"\\files"

    for item in os.walk(my_dir):
      if  item[0].find("g8ce2009") >= 0:
        try:
          shutil.rmtree(item[0])
          print(item[0], "removed")
        except OSError as e:
          print("Error: %s : %s" % (dir_path, e.strerror))

class Quiz:
  identifier = 'g8ce2009aaab3283573f3ef0ef1'
  ident_counter = 0

  def __init__(self, quiz):
    self.guid = Quiz.identifier + self.gen_guid()
    self.title = quiz["options"][0]
    self.options = self.get_options(quiz["options"][1:] if len(quiz["options"]) > 1 else [])
    self.questions = self.get_questions(quiz)

  def get_questions(self, quiz):
    questions = []
    for question in quiz["questions"]:
      questions.append(Question(question))
    
    return questions

  def get_options(self, options):
    options_return = {
      "description":[],
      "shuffle":"true",
      "scoring":"keep_highest",
      "type":"assignment",
      "lockdown":"false",
      "show_correct":"false",
      "anonymous":"false",
      "attempts":"-1",
      "one_question":"false",
      "cant_go_back":"false",
      "available":"true",
      "one_time_results":"false",
      "show_correct_last":"false",
      "only_visible_to_overrides":"false",
      "module_locked":"false"
    }
    for option in options:
      split_option = option.split("~")
      if split_option[0] == "description":
        for i in range(1, len(split_option)):
          options_return["description"].append(split_option[i])
        continue
      if split_option[0] in options_return.keys():
        options_return[split_option[0]] = split_option[1]
    
    return options_return
    
  def gen_guid(self):
    Quiz.ident_counter += 1
    start = len(str(Quiz.ident_counter))
    guid = ""
    for i in range(start, 6):
      guid += "0"
    return guid + str(Quiz.ident_counter)

class Question:
  def __init__(self, question):
    self.title = question["title"]
    self.text = self.get_text(question["text"])
    qtype = question["type"].split("~")
    self.points = qtype[1] if len(qtype) > 1 else 0
    self.type = self.get_type(qtype[0])
    self.answers = self.get_answers(question["answers"])
    self.answer_ids = self.get_answer_ids()
    self.feedback = self.get_feedback(question["feedback"])
    self.assign_answer_properties()

  def get_answers(self, answers):
    answer_return = []
    for answer in answers:
      safe_answer = self.safe_string(answer, False, True)[0]
      answer_return.append(Answer(safe_answer.split("~")))
    
    return answer_return
  
  def get_text(self, text):
    text_return = []
    safe_escape = ['', False]
    for line in text:
      safe_escape = self.safe_string(line, safe_escape[1])
      text_return.append(safe_escape[0])
    
    return text_return

  def get_feedback(self, feedback):
    feedback_return = []
    for line in feedback:
      feedback_return.append(self.safe_string(line))

    return feedback_return

  def safe_string(self, string, escape=False, amp_escape=False):
    string_return = ''
    replace_char = ''
    space_count = 0
    for ch in string:
      if ch == "|":
        escape = not escape
      if escape:
        replace_char = "&amp;lt;"
      else:
        replace_char = '&lt;'

      if ch == " ":
        space_count += 1
      else:
        space_count = 0

      if ch == '<':
        string_return += replace_char
      elif ch == '&' and amp_escape:
        string_return += "&amp;"
      elif ch != '|':
        if space_count == 4:
          string_return = string_return[:-3]
          string_return += ("&amp;nbsp;" * 4)
          space_count = 0
        else:
          string_return += ch

    return [string_return, escape]

  def get_type(self, question_type):
    if question_type == 'multiblank':
      return 'fill_in_multiple_blanks_question'
    elif question_type == 'multiselect':
      return 'multiple_dropdowns_question'
    elif question_type == 'multichoice':
      return 'multiple_choice_question'
    
    return ''
  
  def get_answer_ids(self):
    ids = '' 
    for answer in self.answers:
      for choice in answer.choices:
        ids += f'{choice.ident},'
    
    return ids[:-1]

  def assign_answer_properties(self):
    for answer in self.answers:
      answer.type = self.type
      answer.point_weight = 100 / len(self.answers)

class Answer:

  def __init__(self, answer):
    self.text = answer[0]
    self.type = ''
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