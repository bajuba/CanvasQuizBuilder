from random import randint

def start_section(quiz):
  return f'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <assessment ident="{quiz.guid}" title="{quiz.title}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>unlimited</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">'''

def question_section(question):
  question_return = f'''<item ident="g55e6d962093946e0f770fe3ddd6ff{randint(100, 999)}" title="{question.title}">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>{question.type}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>points_possible</fieldlabel>
              <fieldentry>{question.points}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>original_answer_ids</fieldlabel>
              <fieldentry>{question.answer_ids}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>assessment_question_identifierref</fieldlabel>
              <fieldentry>g6e4260d49c837ae43ad2d7f28345ec03</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">&lt;div&gt;
            '''
  for text in question.text:
    question_return += para(text)

  question_return +='''
&lt;/div&gt;</mattext>
          </material>
          '''
  for answer in question.answers:
    question_return += answer_section(answer)

  question_return += f'''
        </presentation>
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>'''
  for answer in question.answers:
    question_return += outcome_section(answer)
  
  question_return += f'''
        </resprocessing>
        {feedback_section(question)}
      </item>'''

  return question_return

def answer_section(answer):
  answer_return = f'''
  <response_lid ident="response_{answer.text}">
            '''
  if not answer.type == "multiple_choice_question": 
    answer_return += f'''<material>
              <mattext>{answer.text}</mattext>
            </material>
            '''
  answer_return += '''<render_choice>'''
  for choice in answer.choices:
    answer_return += f'''
              <response_label ident="{choice.ident}">
                <material>
                  <mattext texttype="text/plain">{choice.text}</mattext>
                </material>
              </response_label>'''
  answer_return += '''
            </render_choice>
          </response_lid>
          '''
  return answer_return

def outcome_section(answer):
  return f'''<respcondition>
            <conditionvar>
              <varequal respident="response_{answer.text}">{answer.correct_ident}</varequal>
            </conditionvar>
            <setvar varname="SCORE" action="Add">{answer.point_weight}</setvar>
          </respcondition>'''

def feedback_section(question):
  feedback_return = f'''<itemfeedback ident="correct_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">
              '''
  for feedback_line in question.feedback:
    if "~" in feedback_line:
      feedback_return += para(build_link(feedback_line))
    else:
      feedback_return += para(feedback_line)

  feedback_return += '''
              </mattext>
            </material>
          </flow_mat>
        </itemfeedback>'''
  return feedback_return

def end_section():
  return '''
    </section>
  </assessment>
</questestinterop>'''

def assessment_file(quiz):
  return f'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{quiz.guid}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{quiz.title}</title>
  <description></description>
  <shuffle_answers>true</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <hide_results></hide_results>
  <quiz_type>assignment</quiz_type>
  <points_possible>20.0</points_possible>
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
  <assignment identifier="ged4093de460a387ad77fa62525ae18ee">
    <title>{quiz.title}</title>
    <due_at/>
    <lock_at/>
    <unlock_at/>
    <module_locked>false</module_locked>
    <workflow_state>published</workflow_state>
    <assignment_overrides>
    </assignment_overrides>
    <quiz_identifierref>g2570a9708dfba783c5dca2d4d9a978be</quiz_identifierref>
    <allowed_extensions></allowed_extensions>
    <has_group_category>false</has_group_category>
    <points_possible>20.0</points_possible>
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
  <assignment_group_identifierref>g2a696fd07b6cea713c9866d92bcb8c36</assignment_group_identifierref>
  <assignment_overrides>
  </assignment_overrides>
</quiz>
'''

def manifest_file(quizzes):
  manifest_return = f'''<?xml version="1.0" encoding="UTF-8"?>
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
            <imsmd:dateTime>2020-12-26</imsmd:dateTime>
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
  <resources>
    '''
  for quiz in quizzes:
    ref_num = quiz.gen_guid()
    manifest_return += f'''<resource identifier="{quiz.guid}" type="imsqti_xmlv1p2">
    <file href="{quiz.guid}/{quiz.guid}.xml"/>
    <dependency identifierref="ge4d8d35e8e41f702d320795e0d{ref_num}"/>
  </resource>
  <resource identifier="ge4d8d35e8e41f702d320795e0d{ref_num}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{quiz.guid}/assessment_meta.xml">
    <file href="{quiz.guid}/assessment_meta.xml"/>
  </resource>
  '''
  manifest_return += '''</resources>
</manifest>
'''
  return manifest_return

def para(text):
  return f"&lt;p&gt;{text}&lt;/p&gt;"

def build_link(feedback_line):
  link = feedback_line.split("~")
  return f'''&lt;a class="instructure_file_link inline_disabled external" href="{link[1]}" target="_blank"&gt;&lt;span&gt;{link[0]}&lt;/span&gt;&lt;span class="ui-icon ui-icon-extlink ui-icon-inline" title="Links to an external site."&gt;&lt;span class="screenreader-only"&gt;Links to an external site.&lt;/span&gt;&lt;/span&gt;&lt;/a&gt;'''