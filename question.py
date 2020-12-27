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
  
  #     start = 

  # def create_file(self,guid,complete_quiz_text,meta):
  #   os.mkdir(f"files/{guid}")
    
  #   myfile = open(f"files/{guid}/{guid}.xml","w")
  #   myfile.write(complete_quiz_text)
  #   myfile.close()

  #   myfile = open(f"files/{guid}/assessment_meta.xml","w")
  #   myfile.write(meta)
  #   myfile.close()

  # def create_export_file(self):
  #   if not os.path.exists('files'):
  #     os.mkdir("files")
  #   for question in self.questions:
  #     #print(theQuiz.questions[0].text)
      
  #     # start = 
      
  #     question_area = ""
  #     for line in question.text:
  #       question_area += self.para(line)
      
  #     answers_area = f'''&lt;/div&gt;
  #       </mattext></material>'''
  #     #print(question.answers)
  #     for answer in question.answers:
  #       answers_area += f'''<response_lid ident="response_{answer[0]}">
  #             <material>
  #               <mattext>{answer[0]}</mattext>
  #             </material>
  #             <render_choice>
  #             '''
  #       for option in answer[1]:
  #         answers_area += f'''<response_label ident="{option.ident}">
  #                   <material>
  #                     <mattext texttype="text/plain">{option.text}</mattext>
  #                   </material>
  #                 </response_label>
  #                 '''
  #       answers_area += '''</render_choice>
  #               </response_lid>
  #               '''
                
  #     #print(answers_area)
  #     outcomes_area='''</presentation>
              
  #             <resprocessing>
  #               <outcomes>
  #                 <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
  #               </outcomes>'''
  #     for answer in question.answers:        
  #       outcomes_area +=f'''<respcondition>
  #                   <conditionvar>
  #                     <varequal respident="response_{answer[0]}">{answer[1][0].ident}</varequal>
  #                   </conditionvar>
  #                   <setvar varname="SCORE" action="Add">{format(100/question.number, '.2f')}</setvar>
  #                 </respcondition>
                  
  #               '''
  #     outcomes_area+="</resprocessing>"
  #     feedback_area=f'''<itemfeedback ident="correct_fb">
  #               <flow_mat>
  #                 <material>
  #                   <mattext texttype="text/html">{self.para(question.feedback[0])}&lt;a class="instructure_file_link inline_disabled" href="{question.feedback[2]}" target="_blank"&gt;{question.feedback[1]}&lt;/a&gt;&lt;/p&gt;</mattext>
  #                 </material>
  #               </flow_mat>
  #             </itemfeedback>
  #           </item>
  #         </section>
  #       </assessment>
  #     </questestinterop>

  #     '''
      
      

  #     meta = self.create_meta(question.guid,question.quiz_title)
  #     complete_quiz_text = start+question_area+answers_area+outcomes_area+feedback_area
  #     self.create_file(question.guid,complete_quiz_text,meta)
  #   

  #   myfile = open("files/imsmanifest.xml", "w")
  #   myfile.write(self.build_manifest(self.questions))
  #   myfile.close()
      
  # def para(self,text):
  #   return "&lt;p&gt;"+text+"&lt;/p&gt;"
  # def create_meta(self,guid,title):
  #   meta = f'''<?xml version="1.0" encoding="UTF-8"?>
  #   <quiz identifier="{guid}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  #   <title>{title}</title>
  #   <description></description>
  #   <shuffle_answers>true</shuffle_answers>
  #   <scoring_policy>keep_highest</scoring_policy>
  #   <hide_results></hide_results>
  #   <quiz_type>assignment</quiz_type>
  #   <points_possible>20.0</points_possible>
  #   <require_lockdown_browser>false</require_lockdown_browser>
  #   <require_lockdown_browser_for_results>false</require_lockdown_browser_for_results>
  #   <require_lockdown_browser_monitor>false</require_lockdown_browser_monitor>
  #   <lockdown_browser_monitor_data/>
  #   <show_correct_answers>false</show_correct_answers>
  #   <anonymous_submissions>false</anonymous_submissions>
  #   <could_be_locked>true</could_be_locked>
  #   <disable_timer_autosubmission>false</disable_timer_autosubmission>
  #   <allowed_attempts>-1</allowed_attempts>
  #   <one_question_at_a_time>false</one_question_at_a_time>
  #   <cant_go_back>false</cant_go_back>
  #   <available>true</available>
  #   <one_time_results>false</one_time_results>
  #   <show_correct_answers_last_attempt>false</show_correct_answers_last_attempt>
  #   <only_visible_to_overrides>false</only_visible_to_overrides>
  #   <module_locked>false</module_locked>
  #   <assignment identifier="g19a942d0e6d2cd3b55e47ac97123a{randint(111,999)}">
  #   <title>{title}</title>
  #   <due_at/>
  #   <lock_at/>
  #   <unlock_at/>
  #   <module_locked>false</module_locked>
  #   <workflow_state>published</workflow_state>
  #   <assignment_overrides>
  #   </assignment_overrides>
  #   <quiz_identifierref>{guid}</quiz_identifierref>
  #   <allowed_extensions></allowed_extensions>
  #   <has_group_category>false</has_group_category>
  #   <points_possible>10.0</points_possible>
  #   <grading_type>points</grading_type>
  #   <all_day>false</all_day>
  #   <submission_types>online_quiz</submission_types>
  #   <position>1</position>
  #   <turnitin_enabled>false</turnitin_enabled>
  #   <vericite_enabled>false</vericite_enabled>
  #   <peer_review_count>0</peer_review_count>
  #   <peer_reviews>false</peer_reviews>
  #   <automatic_peer_reviews>false</automatic_peer_reviews>
  #   <anonymous_peer_reviews>false</anonymous_peer_reviews>
  #   <grade_group_students_individually>false</grade_group_students_individually>
  #   <freeze_on_copy>false</freeze_on_copy>
  #   <omit_from_final_grade>false</omit_from_final_grade>
  #   <intra_group_peer_reviews>false</intra_group_peer_reviews>
  #   <only_visible_to_overrides>false</only_visible_to_overrides>
  #   <post_to_sis>false</post_to_sis>
  #   <moderated_grading>false</moderated_grading>
  #   <grader_count>0</grader_count>
  #   <grader_comments_visible_to_graders>true</grader_comments_visible_to_graders>
  #   <anonymous_grading>false</anonymous_grading>
  #   <graders_anonymous_to_graders>false</graders_anonymous_to_graders>
  #   <grader_names_visible_to_final_grader>true</grader_names_visible_to_final_grader>
  #   <anonymous_instructor_annotations>false</anonymous_instructor_annotations>
  #   <post_policy>
  #     <post_manually>false</post_manually>
  #   </post_policy>
  #   </assignment>
  #   <assignment_group_identifierref>g74aee8be22838d8f9a91a74a5f1fa{randint(111,999)}</assignment_group_identifierref>
  #   <assignment_overrides>
  #   </assignment_overrides>
  #   </quiz>'''
  #   return meta
  # def build_manifest(self,questions):
  #   manifest = f'''<?xml version="1.0" encoding="UTF-8"?>
  #   <manifest identifier="gc1c043c4d56096c5d62f1217d8a35bf3" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">
  #     <metadata>
  #       <schema>IMS Content</schema>
  #       <schemaversion>1.1.3</schemaversion>
  #       <imsmd:lom>
  #         <imsmd:general>
  #           <imsmd:title>
  #             <imsmd:string>QTI Quiz Export for course "TEM-CIS-156-JM"</imsmd:string>
  #           </imsmd:title>
  #         </imsmd:general>
  #         <imsmd:lifeCycle>
  #           <imsmd:contribute>
  #             <imsmd:date>
  #               <imsmd:dateTime>2020-12-25</imsmd:dateTime>
  #             </imsmd:date>
  #           </imsmd:contribute>
  #         </imsmd:lifeCycle>
  #         <imsmd:rights>
  #           <imsmd:copyrightAndOtherRestrictions>
  #             <imsmd:value>yes</imsmd:value>
  #           </imsmd:copyrightAndOtherRestrictions>
  #           <imsmd:description>
  #             <imsmd:string>Private (Copyrighted) - http://en.wikipedia.org/wiki/Copyright</imsmd:string>
  #           </imsmd:description>
  #         </imsmd:rights>
  #       </imsmd:lom>
  #     </metadata>
  #     <organizations/>
  #     <resources>'''
  #   for question in questions:
  #     guid_append = question.gen_guid()
  #     manifest += f'''<resource identifier="{question.guid}" type="imsqti_xmlv1p2">
  #         <file href="{question.guid}/{question.guid}.xml"/>
  #         <dependency identifierref="ge4d8d35e8e41f702d320795e0d{guid_append}"/>
  #       </resource>
  #       <resource identifier="ge4d8d35e8e41f702d320795e0d{guid_append}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{question.guid}/assessment_meta.xml">
  #         <file href="{question.guid}/assessment_meta.xml"/>
  #       </resource>'''
        
  #   manifest += '''</resources>
  #   </manifest>
  #   '''
  #   return manifest
  # def get_idents(self):
  #   idents = ""
  #   for question in self.questions:
  #     for answer in question.answers:
  #       for response in answer[1]:
  #         idents += response.ident+","    
  #   return idents[:-1]
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

      # if question["type"] == 'multiblank':
      #   questions.append(FillQuestion(question))
      # if question["type"] == 'multiselect':
      #   questions.append(SelectQuestion(question))
    
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
      return 'fill_in_multiple_blanks_question'
    elif question_type == 'multiselect':
      return 'multiple_dropdowns_question'
    
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

# class FillQuestion:
#     quiz_identifier = 'g8ce2009aaab3283573f3ef0ef1'
#     #0-35
#     def __init__(self,quiz_title,question_title,text,answers,feedback ):
#       self.guid = FillQuestion.quiz_identifier+self.gen_guid()
#       self.quiz_title = quiz_title[0]
#       self.question_title = question_title[0]
#       self.text = text
#       self.answers = self.format_answers(answers)
#       self.idents = self.get_idents()
#       self.feedback = self.format_feedback(feedback)
#       self.number = len(self.answers)

#     def gen_guid(self):
#       guid = ""
#       for i in range(0,6):
#         num = randint(0,15)
#         if(num <= 9):
#           num += 48
#         else:
#           num += 87
#         guid += chr(num)
#       return guid
      
#     def format_answers(self, answers):
#         new_answers = []
#         answer_set = []

#         for answer in answers:
#           answer_set = answer.split("~")
#           responses = []
#           for response in range(1,len(answer_set)):
#             new_response = Response(answer_set[response])
#             responses.append(new_response)
#           new_answers.append([answer_set[0],responses])
#         return new_answers

#     def format_feedback(self, feedback):
#         new_feedback = []
#         feedback_set = []

#         for feeditem in feedback:
#           if("~" in feeditem):
#             feedback_set = feeditem.split("~")
#             new_feedback.append(feedback_set[0])
#             new_feedback.append(feedback_set[1])
#           else:
#             new_feedback.append(feeditem)
#         return new_feedback
#     def get_idents(self):
#       idents = ""
#       for answer in self.answers:
#         for response in answer[1]:
#             idents += response.ident+","
#       return idents[:-1]

# class DropQuiz:
#   quiz_identifier = 'g8ce2009aaab3283573f3ef0ef1'
#   #0-35
#   def __init__(self,quiz_title,questions ):
#     self.guid = DropQuiz.quiz_identifier+self.gen_guid()
#     self.quiz_title = quiz_title[0]
#     self.dropdowns = questions

#   def gen_guid(self):
#     guid = ""
#     for i in range(0,6):
#       num = randint(0,15)
#       if(num <= 9):
#         num += 48
#       else:
#         num += 87
#       guid += chr(num)
#     return guid
    
  

#   def format_feedback(self, feedback):
#       new_feedback = []
#       feedback_set = []

#       for feeditem in feedback:
#         if("~" in feeditem):
#           feedback_set = feeditem.split("~")
#           new_feedback.append(feedback_set[0])
#           new_feedback.append(feedback_set[1])
#         else:
#           new_feedback.append(feeditem)
#       return new_feedback
#   def get_idents(self):
#     idents = ""
#     for answer in self.answers:
#       for response in answer[1]:
#           idents += response.ident+","
#     return idents[:-1]





# class DropQuestion:
#   def __init__(self,question_title,text,answers,feedback ):
#     self.question_title = question_title[0]
#     self.text = text
#     self.answer = self.format_answers(answers)
#     self.idents = self.get_idents()
#     self.feedback = self.format_feedback(feedback)
#   def format_answers(self, answers):
#     new_answers = []
#     answer_set = []

#     for answer_set in answers:
#       options_set = answer_set.split("~")
#       responses = []
#       for x in range(1,len(answer_set)):
#         new_response = Response(answer_set[x])
#         responses.append(new_response)
#       new_answers.append([answer_set[0],responses])
#     return new_answers

#   def get_idents(self):
#     idents = ""
#     for answer in self.answers:
#       for response in answer[1]:
#           idents += response.ident+","
#     return idents[:-1]




# class Response:
#     id = 1111
#     def __init__(self,text):
      
#       self.text = text
#       Response.id += 1
#       self.ident = str(Response.id)
      