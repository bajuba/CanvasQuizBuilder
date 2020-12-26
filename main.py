from question import FillQuestion, Quizzes
from pprint import pprint
import os
my_file = open("input.txt","r")

def para(text):
    return "&lt;p&gt;"+text+"&lt;p&gt;"

lines = my_file.readlines()
# print(lines)
stripped_lines = []
for line in lines:
  stripped_lines.append(line.strip())

#parts = str().split("###")

# pprint(lines)
# print("\n\n------------------------------\n\n")
# pprint(stripped_lines)



#print(stripped_lines)
parts = []
section = []
for line in stripped_lines:
  if line == "###":
    parts.append(section)
    section = []
  else:
    section.append(line)


count = 0

# self.title = title
#         self.text = text
#         self.answers = answers
#         self.feedback = feedback

questions = []
#pprint(parts)
for part in parts:
  if count==0:
    quiztitle=part
  elif count==1:
    questiontitle = part
  elif count==2:
    text = part
  elif count==3:
    answers = part
  elif count==4:
    feedback = part
    newQ = FillQuestion(quiztitle,questiontitle,text,answers,feedback)
    questions.append(newQ)
    count = 0
    continue
  count+=1
theQuiz = Quizzes(questions)

#pprint(theQuiz.questions[0].answers)


  


# for line in parts:
#   print(line,"\n")

#build manifest
manifest = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="gc1c043c4d56096c5d62f1217d8a35bf3" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.1.3</schemaversion>
    <imsmd:lom>
      <imsmd:general>
        <imsmd:title>
          <imsmd:string>QTI Quiz Export for course "TEM-CIS-156-JM"</imsmd:string>
        </imsmd:title>
      </imsmd:general>
      <imsmd:lifeCycle>
        <imsmd:contribute>
          <imsmd:date>
            <imsmd:dateTime>2020-12-25</imsmd:dateTime>
          </imsmd:date>
        </imsmd:contribute>
      </imsmd:lifeCycle>
      <imsmd:rights>
        <imsmd:copyrightAndOtherRestrictions>
          <imsmd:value>yes</imsmd:value>
        </imsmd:copyrightAndOtherRestrictions>
        <imsmd:description>
          <imsmd:string>Private (Copyrighted) - http://en.wikipedia.org/wiki/Copyright</imsmd:string>
        </imsmd:description>
      </imsmd:rights>
    </imsmd:lom>
  </metadata>
  <organizations/>
  <resources>'''
for question in theQuiz.questions:
  guid_append = question.gen_guid()
  manifest += f'''<resource identifier="{question.guid}" type="imsqti_xmlv1p2">
      <file href="{question.guid}/{question.guid}.xml"/>
      <dependency identifierref="ge4d8d35e8e41f702d320795e0d{guid_append}"/>
    </resource>
    <resource identifier="ge4d8d35e8e41f702d320795e0d{guid_append}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{question.guid}/assessment_meta.xml">
      <file href="{question.guid}/assessment_meta.xml"/>
    </resource>'''
    
manifest += '''</resources>
</manifest>
'''
os.mkdir("non_cc_assessment")
myfile = open("imsmanifest.xml", "w")
myfile.write(manifest)
myfile.close()

quizcounter = 0;
#now to output
for question in theQuiz.questions:
  #print(theQuiz.questions[0].text)

  start = f'''
  <?xml version="1.0" encoding="UTF-8"?>
  <questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
    <assessment ident="{question.guid}" title="{question.quiz_title}">
      <qtimetadata>
        <qtimetadatafield>
          <fieldlabel>cc_maxattempts</fieldlabel>
          <fieldentry>unlimited</fieldentry>
        </qtimetadatafield>
      </qtimetadata>
      <section ident="root_section">
        <item ident="g5a12953047f11134eb0ab7cc6f037ecd" title="{question.question_title}">
          <itemmetadata>
            <qtimetadata>
              <qtimetadatafield>
                <fieldlabel>question_type</fieldlabel>
                <fieldentry>fill_in_multiple_blanks_question</fieldentry>
              </qtimetadatafield>
              <qtimetadatafield>
                <fieldlabel>points_possible</fieldlabel>
                <fieldentry>10.0</fieldentry>
              </qtimetadatafield>
              <qtimetadatafield>
                <fieldlabel>original_answer_ids</fieldlabel>
                <fieldentry>{question.idents}
                </fieldentry>
              </qtimetadatafield>
              <qtimetadatafield>
                <fieldlabel>assessment_question_identifierref</fieldlabel>
                <fieldentry>g3870a3575fef60c4c259b24d7d422fbd</fieldentry>
              </qtimetadatafield>
            </qtimetadata>
          </itemmetadata>
          <presentation>
            <material>
              <mattext texttype="text/html">&lt;div&gt;
  '''
  
  question_area = ""
  

  for line in question.text:
    question_area += para(line)
  # print("\n\n------------------------------\n\n")
  # print(question_area)
  # print("\n\n------------------------------\n\n")

  answers_area = f'''&lt;/div&gt;
    </mattext></material>'''
  #print(question.answers)
  for answer in question.answers:
    answers_area += f'''
          <response_lid ident="response_{answer[0]}">
          <material>
            <mattext>{answer[0]}</mattext>
          </material>
          <render_choice>
          '''
    for option in answer[1]:
      answers_area += f'''
              <response_label ident="{option.ident}">
                <material>
                  <mattext texttype="text/plain">{option.text}</mattext>
                </material>
              </response_label>
              '''
    answers_area += '''
              </render_choice>
            </response_lid>
            '''
            
  #print(answers_area)
  outcomes_area='''
          </presentation>
          
          <resprocessing>
            <outcomes>
              <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
            </outcomes>'''
  for answer in question.answers:        
    outcomes_area +=f'''
              <respcondition>
                <conditionvar>
                  <varequal respident="response_{answer[0]}">{answer[1][0].ident}</varequal>
                </conditionvar>
                <setvar varname="SCORE" action="Add">{format(100/question.number, '.2f')}</setvar>
              </respcondition>
              
            '''
  
  feedback_area=f'''
          <itemfeedback ident="correct_fb">
            <flow_mat>
              <material>
                <mattext texttype="text/html">{para(question.feedback[0])}&lt;a class="instructure_file_link inline_disabled" href="{question.feedback[2]}" target="_blank"&gt;{question.feedback[1]}&lt;/a&gt;&lt;/p&gt;</mattext>
              </material>
            </flow_mat>
          </itemfeedback>
        </item>
      </section>
    </assessment>
  </questestinterop>

  '''
  

  meta = f'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{question.guid}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>Chapter 1 - Exercise 1</title>
  <description></description>
  <shuffle_answers>true</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <hide_results></hide_results>
  <quiz_type>assignment</quiz_type>
  <points_possible>10.0</points_possible>
  <require_lockdown_browser>false</require_lockdown_browser>
  <require_lockdown_browser_for_results>false</require_lockdown_browser_for_results>
  <require_lockdown_browser_monitor>false</require_lockdown_browser_monitor>
  <lockdown_browser_monitor_data/>
  <show_correct_answers>false</show_correct_answers>
  <anonymous_submissions>false</anonymous_submissions>
  <could_be_locked>true</could_be_locked>
  <disable_timer_autosubmission>false</disable_timer_autosubmission>
  <allowed_attempts>-1</allowed_attempts>
  <one_question_at_a_time>false</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <available>true</available>
  <one_time_results>false</one_time_results>
  <show_correct_answers_last_attempt>false</show_correct_answers_last_attempt>
  <only_visible_to_overrides>false</only_visible_to_overrides>
  <module_locked>false</module_locked>
  <assignment identifier="g19a942d0e6d2cd3b55e47ac97123a655">
    <title>Chapter 1 - Exercise 1</title>
    <due_at/>
    <lock_at/>
    <unlock_at/>
    <module_locked>false</module_locked>
    <workflow_state>published</workflow_state>
    <assignment_overrides>
    </assignment_overrides>
    <quiz_identifierref>{question.guid}</quiz_identifierref>
    <allowed_extensions></allowed_extensions>
    <has_group_category>false</has_group_category>
    <points_possible>10.0</points_possible>
    <grading_type>points</grading_type>
    <all_day>false</all_day>
    <submission_types>online_quiz</submission_types>
    <position>1</position>
    <turnitin_enabled>false</turnitin_enabled>
    <vericite_enabled>false</vericite_enabled>
    <peer_review_count>0</peer_review_count>
    <peer_reviews>false</peer_reviews>
    <automatic_peer_reviews>false</automatic_peer_reviews>
    <anonymous_peer_reviews>false</anonymous_peer_reviews>
    <grade_group_students_individually>false</grade_group_students_individually>
    <freeze_on_copy>false</freeze_on_copy>
    <omit_from_final_grade>false</omit_from_final_grade>
    <intra_group_peer_reviews>false</intra_group_peer_reviews>
    <only_visible_to_overrides>false</only_visible_to_overrides>
    <post_to_sis>false</post_to_sis>
    <moderated_grading>false</moderated_grading>
    <grader_count>0</grader_count>
    <grader_comments_visible_to_graders>true</grader_comments_visible_to_graders>
    <anonymous_grading>false</anonymous_grading>
    <graders_anonymous_to_graders>false</graders_anonymous_to_graders>
    <grader_names_visible_to_final_grader>true</grader_names_visible_to_final_grader>
    <anonymous_instructor_annotations>false</anonymous_instructor_annotations>
    <post_policy>
      <post_manually>false</post_manually>
    </post_policy>
  </assignment>
  <assignment_group_identifierref>g74aee8be22838d8f9a91a74a5f1fa5f7</assignment_group_identifierref>
  <assignment_overrides>
  </assignment_overrides>
</quiz>'''
  
  #print(start,question_area,answers_area,outcomes_area,feedback_area)

  os.mkdir(question.guid)
  
  myfile = open(f"{question.guid}/{question.guid}.xml","w")
  myfile.write(start+question_area+answers_area+outcomes_area+feedback_area)
  myfile.close()

  myfile = open(f"{question.guid}/assessment_meta.xml","w")
  myfile.write(meta)
  myfile.close()



  quizcounter += 1