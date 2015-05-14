#whenever you run this script you will be creating 200 HITS and costing 2$ to the Account owner (whosoever key is used)
#creates a HIT for one image from Thomas' flickr account

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,FormattedContent,FreeTextAnswer

#Your keys here
ACCESS_ID ='*******************'
SECRET_KEY = '************************'
HOST = 'mechanicalturk.amazonaws.com'

conn = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

def creating_hits(hitters, location='https://c9.io/gibolt/wordcloud565/workspace/aws-python-example/IMG_5109.JPG'): 
    title = 'First thoughts on the photo'
    description = ('Enter the first word that comes to your mind'
                   ' after seeing this photo')
    keywords = 'photo,easy,short,describe,one,word'
    
    string='<p><img src="'+location+'" alt="oops.image missing" height="400" width="500" /></p>'
    
    overview = Overview()
    overview.append_field('Title', 'What is Your First Impression?')
    overview.append(FormattedContent(string))
     
    
    qc1 = QuestionContent()
    qc1.append_field('Title','First word that comes to mind')
    fta1 = FreeTextAnswer()
    q1 = Question(identifier='photo', content=qc1, answer_spec=AnswerSpecification(fta1))
    qc2 = QuestionContent()
    qc2.append_field('Title', 'Second Word')
    q2typ = FreeTextAnswer()
    q2 = Question(identifier="second", content=qc2, answer_spec=AnswerSpecification(q2typ))
    qc3 = QuestionContent()
    qc3.append_field('Title', 'Third Word')
    q3typ = FreeTextAnswer()
    q3 = Question(identifier="third", content=qc3, answer_spec=AnswerSpecification(q3typ))
    
    question_form = QuestionForm()
    question_form.append(overview)
    question_form.append(q1)
    question_form.append(q2)
    question_form.append(q3)
     
    for x in range(1,hitters):
        my_hit = conn.create_hit(questions=question_form,
                   max_assignments=1,
                   title=title,
                   description=description,
                   keywords=keywords,
                   duration = 60*5,
                   reward=0.01)
        
# creates 200 HITs, each worker might attempt more than one HIT           
creating_hits(200)