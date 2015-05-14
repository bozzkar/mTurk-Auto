# Prints the total unique workers worked on HITs
from boto.mturk.connection import MTurkConnection

#Your keys here 
ACCESS_ID ='***********'
SECRET_KEY = '******************'
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
 

def workers_list(): 
	
	hits = pull_hits(conn)
	full_response = ""
	for each_hit in hits:
		assignments = conn.get_assignments(each_hit.HITId)
		for each_assignment in assignments:
			#print "Answers of the worker %s" % each_assignment.WorkerId
			#print "Worker ID: %s" %(each_assignment.WorkerId)
			full_response += each_assignment.WorkerId + " "
							
	#print full_response
	workers = full_response.split()
	#print len(workers)
	workers = list(set(workers))
	print "Total Unique workers %d" % len(workers)


conn = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
workers_list()