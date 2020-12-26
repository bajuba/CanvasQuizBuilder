from random import randint
# 0-quize title
# 0-question title, 1-question text, 2-anwers, 3-feedback
class Quizzes:
  
  def __init__(self,questions ):
    self.questions = questions
    self.idents = self.get_idents()

  def read_file(self,filename):
    myfile = open(filename,"r")
    str(myfile.readlines()).split("###")

  def get_idents(self):
    idents = ""
    for question in self.questions:
      for answer in question.answers:
        for response in answer[1]:
          idents += response.ident+","    
    return idents[:-1]
  

class FillQuestion:
    quiz_identifier = 'g8ce2009aaab3283573f3ef0ef1'
    #0-35
    def __init__(self,quiz_title,question_title,text,answers,feedback ):
      self.guid = FillQuestion.quiz_identifier+self.gen_guid()
      self.quiz_title = quiz_title[0]
      self.question_title = question_title[0]
      self.text = text

      self.answers = self.format_answers(answers)
      self.idents = self.get_idents()
      self.feedback = self.format_feedback(feedback)

      self.number = len(self.answers)

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
      
    def format_answers(self, answers):
        new_answers = []
        answer_set = []

        for answer in answers:
          answer_set = answer.split("~")
          responses = []
          for response in range(1,len(answer_set)):
            new_response = Response(answer_set[response])
            responses.append(new_response)
          new_answers.append([answer_set[0],responses])
        return new_answers

    def format_feedback(self, feedback):
        new_feedback = []
        feedback_set = []

        for feeditem in feedback:
          if("~" in feeditem):
            feedback_set = feeditem.split("~")
            new_feedback.append(feedback_set[0])
            new_feedback.append(feedback_set[1])
          else:
            new_feedback.append(feeditem)
        return new_feedback
    def get_idents(self):
      idents = ""
      for answer in self.answers:
        for response in answer[1]:
            idents += response.ident+","
      return idents[:-1]
    
class Response:
    id = 1111
    def __init__(self,text):
      
      self.text = text
      Response.id += 1
      self.ident = str(Response.id)
      