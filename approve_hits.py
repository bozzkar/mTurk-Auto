# Approve hits and view all responses

from boto.mturk.connection import MTurkConnection

#Your keys here 
ACCESS_ID ='********************'
SECRET_KEY = '********************'
HOST = 'mechanicalturk.amazonaws.com'
 
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
 

def approve_hits(): 
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
						#full_response += word + ' '
			conn.approve_assignment(each_assignment.AssignmentId)
			x+=1
			print "--------------------Approved HIT %d" %(x)
			
							
	print full_response	
	return full_response


conn = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
approve_hits()