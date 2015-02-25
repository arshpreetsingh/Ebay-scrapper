import json
import csv
import os
import sys
from ebaysdk.soa.finditem import Connection as FindItem
from optparse import OptionParser
sys.path.insert(0, '%s/../' % os.path.dirname(__file__))
from common import dump
import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

def init_options():
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-d", "--debug",
	action="store_true", dest="debug", default=False,
	help="Enabled debugging [default: %default]")
	parser.add_option("-y", "--yaml",
	dest="yaml", default='ebay.yaml',
	help="Specifies the name of the YAML defaults file. [default: %default]")
	parser.add_option("-a", "--appid",
	dest="appid", default=None,
	help="Specifies the eBay application id to use.")
	(opts, args) = parser.parse_args()
	parser.add_option("-c","--consumer_id",dest="consumer_id",
	default="arshp.us2015",help="")
	
	(opts,args)= parser.parse_args()
		
	return opts, args

def run(opts):
	try:
		api = finding(debug=opts.debug, appid=opts.appid,
		config_file=opts.yaml, warnings=True)
		
		api_request = {
		'keywords': u'Fashion Men Women Kids',
		'affiliate': {'trackingId': 5337368933},
		'affiliate':{'networkId':902099},
		'affiliate':{'customId':200},
		
		}
		
		retval = api.execute('findItemsAdvanced', api_request)
		error=api.error()
		if not api.error():
			items=api.response.reply.searchResult.item
			for item_ in items:
	
				print item_.title
		                print item_.galleryURL
				print item_.viewItemURL
				print dir(item_)
		mywriter = csv.writer(open("fashion.csv","wb"))
		head = ("Title","Image","ItemURL")
		mywriter.writerow(head)
		for i in range(0,len(items)):
			mywriter.writerow([items[i].title,items[i].galleryURL,items[i].viewItemURL])					
			dump(api)

		
	except ConnectionError as e:
		print(e)
		print(e.response.dict())

if __name__ == "__main__":
	print("Finding samples for SDK version %s" % ebaysdk.get_version())
	(opts, args) = init_options()
	run(opts)

