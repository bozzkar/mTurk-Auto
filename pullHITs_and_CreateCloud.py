#Make wordCloud from HIT responses

from boto.mturk.connection import MTurkConnection
import unirest
import webbrowser

#Your keys here
ACCESS_ID ='************'
SECRET_KEY = '****************'
HOST = 'mechanicalturk.amazonaws.com'

#pull all HITs from my account 
def pull_hits(conn):
    page_size = 50
    hits = conn.get_reviewable_hits(page_size=page_size)
    #print "Total results to fetch %s " % hits.TotalNumResults
    #print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        #print "Request hits page %i" % pn
        temp_hits = conn.get_reviewable_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
    return hits
 
# returns the responses of all HITs as single string comma separated
def return_results(): 
	x = 0
	hits = pull_hits(conn)
	full_response = ""
	for each_hit in hits:
		assignments = conn.get_assignments(each_hit.HITId)
		for each_assignment in assignments:
			#print "Answers of the worker %s" % each_assignment.WorkerId
			for question_form_answer in (each_assignment.answers[0]):
				for response in question_form_answer.fields:
					unpacked = response.split()
					for word in unpacked:
						print "%s" % (word.lower()) + ' '
						full_response += '\'' + word.lower() + '\'' +','
					
			x+=1
			print "--------------------HIT %d" %(x)
	print full_response	
	return full_response[:-1]

#plots word cloud and prints its url in the end
def plot_wordcloud(data):
	# Test data
	# data = ['You','you','hate','peanuts','because','you','are','allergic','Why','did','you','eat','the','jam','jam','is','poisonous','to','peanuts']

	textblock = ""
	for i in range(0, len(data)):
		#if i>0 :
		#	textblock += " "
		textblock += data[i]
	height = 1000
	width = 800
	config = "n/a"

	print textblock
	print width
	print height
	print config

	response = unirest.post("https://gatheringpoint-word-cloud-maker.p.mashape.com/index.php",
	  
	  headers={
		"X-Mashape-Authorization": "pj3yluoHZ2vzfYavjyQL889fAFMy4Q5w"
	  },
	  params={ 
		"height": height,
		"textblock": textblock,
		"width": width,
		"config": config
	  }
	);

	print response.body['url']
	webbrowser.open(response.body['url'])
	

#make connection	
conn = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

# plot word cloud with argument as string containing results of HITs
plot_wordcloud(return_results())
