# CanvasQuizBuilder

Build Importable Canvas quizzes in a text file.
The file should begin with the title of the quiz. Each section of the quiz is separated by three pound symbols (&#35;&#35;&#35;)
Each quiz in the file must be followed by six pound symbols (&#35;&#35;&#35;&#35;&#35;&#35;) even if it is the only quiz in the file
The sections are as follows:

Quiz Title<br/>
&#35;&#35;&#35;<br/>
Question Title<br/>
&#35;&#35;&#35;<br/>
Question Type&#126;Points<br/>
&#35;&#35;&#35;<br/>
Question Text<br/>
&#35;&#35;&#35;<br/>
Answers<br/>
&#35;&#35;&#35;<br/>
Question Correct Feedback<br/>
&#35;&#35;&#35;&#35;&#35;&#35;<br/>

## Possible Types:
multiblank = multiple fill in the blank question<br/>
multiselect = multiple dropdown question<br/>
multichoice = multiple choice question<br/>

## Answers:
Answers are in the following format:<br/>
identifier&#126;answer1&#126;answer2&#126;answer3&#126;etc...

### multiblank answers:<br/>
The identifier matches the blank identifier in the question while each subsequent answer represents a possible correct answer for that blank<br/>
### multiselect answers:<br/>
The identifier matches the dropdown identifier in the question while each subsequent answer represents an option in the dropdown.<br/>
The correct answer for multiselect must be the first answer following the identifier. (all quizzes are created with shuffled answers)<br/>
### multichoice answers:<br/>
The identifier is not used but must be present. The first answer must be the correct one while subsequent answers are choices<br/>

## Feedback:
The feedback will display if a student gets the question correct. Leave this section blank if the question does not require feedback.<br/>
Note: The section separator must still be present even without feedback<br/>
If a link is included in the feedback, it must be on its own line in the following format:<br/>
link text~link address<br/>

## Example Quiz with all questions represented:
<pre>
Test Quiz
&#35;&#35;&#35;
01. Question 1
&#35;&#35;&#35;
multichoice~3
&#35;&#35;&#35;
Which of these is traditionally green?
&#35;&#35;&#35;
1&#126;tree&#126;fire hydrant&#126;television&#126;refrigerator&#126;fox
&#35;&#35;&#35;
Good job! We all know trees are green all the time forever!
&#35;&#35;&#35;
02. Question 2
&#35;&#35;&#35;
multiblank&#126;5
&#35;&#35;&#35;
[1] are red.
[2] are blue.
[3] is sweet, and so are you!
&#35;&#35;&#35;
1&#126;roses
2&#126;violets
3&#126;sugar
&#35;&#35;&#35;
&#35;&#35;&#35;
Third Question
&#35;&#35;&#35;
multiselect&#126;2
&#35;&#35;&#35;
Little Bo-Peep has lost her [1],
And can't tell where to find them;
Leave them alone, and they'll come [2],
Bringing their [3] behind them.
&#35;&#35;&#35;
1&#126;sheep&#126;dogs&#126;socks
2&#126;home&#126;back&#126;to dinner&#126;over for tea&#126;around
3&#126;tails&#126;babies&#126;lint
&#35;&#35;&#35;
Check out a full version of the poem:
little bo peep poem&#126;https://www.poetryfoundation.org/poems/46966/little-bo-peep
&#35;&#35;&#35;&#35;&#35;&#35;
</pre>
