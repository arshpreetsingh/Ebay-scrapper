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
		'keywords': u'Toys',
		'affiliate': {'trackingId': 5337368933},
		'affiliate':{'networkId':902099},
		'affiliate':{'customId':200},
		
		}
		
		retval = api.execute('findItemsAdvanced', api_request)
		error=api.error()
		if not api.error():
			items=api.response.reply.searchResult.item
		#	print dir(api.response.reply.searchResult)
# pehlan tan eh upper wali line naal thoe pange lai ke ^^^^^^ saare attributes fins out karo
#fer csv wali header file check karo.
#fer header file de attributes jo incompletes ne oh check karo
	
#		for item_ in items:
	#
	#			print item_.title
	#	                print item_.galleryURL
	#			print item_.viewItemURL
	#			print dir(item_)
		mywriter = csv.writer(open("toys.csv","wb"))
		head =("sku","_store","_attribute_set","_type","_category","_root_category","_product_websites","color","cost","country_of_manufacture",
		"created_at","custom_design","custom_design_from","custom_design_to","custom_layout_update","description","gallery","gift_message_available","has_options","image","image_label",
		"manufacturer","media_gallery","meta_description","meta_keyword","meta_title","minimal_price","msrp","msrp_display_actual_price_type","msrp_enabled","name",
		"news_from_date","news_to_date","options_container","page_layout","price","required_options","short_description","small_image",
			"small_image_label","special_from_date","special_price","special_to_date","status","tax_class_id",
			"thumbnail","thumbnail_label","updated_at","url_key","url_path","visibility","weight","qty",
			"min_qty","use_config_min_qty","is_qty_decimal","backorders","use_config_backorders",
			"min_sale_qty","use_config_min_sale_qty","max_sale_qty","use_config_max_sale_qty",
			"is_in_stock","notify_stock_qty","use_config_notify_stock_qty","manage_stock","use_config_manage_stock",
			"stock_status_changed_auto","use_config_qty_increments",
			"qty_increments","use_config_enable_qty_inc","enable_qty_increments","is_decimal_divided",
			"_links_related_sku","_links_related_position","_links_crosssell_sku",
			"_links_crosssell_position","_links_upsell_sku","_links_upsell_position","_associated_sku",
			"_associated_default_qty","_associated_position","_tier_price_website","_tier_price_customer_group","_tier_price_qty",
			"_tier_price_price","_group_price_website","_group_price_customer_group","_group_price_price",
			"_media_attribute_id","_media_image","_media_lable","_media_position","_media_is_disabled")

		mywriter.writerow(head)
		for i in range(0,len(items)):
#		Logic theek aa file wala, bass thoda jeha kamm ereh gea, hun tan:)

			mywriter.writerow([i,"","Default","virtual","","","base","","","",
			"","","","","",items[i].primaryCategory.categoryName,"","","",items[i].galleryURL,
			"","","","","","","","","","",
			items[i].title.title,"","","","",items[i].sellingStatus.currentPrice.value,"","Toys","","",
			"","","","1","2","","","","","",
			2,10,"","","","","","","","","","","","","",
			"","","","","","","","","","","","","","",
			"","","","","","","","","",""])			
			dump(api)

# I got the error, Actually I am writing CSV in wrong way. I need to write one row for one product. But I am messing with it. :P 
#The thing I learned from this work is I need to read and understand code carefully before compiling it.
#Stackover flow te question puchan lai try karo jado question puchoge tan apne aap e samaj lagg jauga.	
#(If you know what to ask then you know what to do)	

	except ConnectionError as e:
		print(e)
		print(e.response.dict())

if __name__ == "__main__":
	print("Finding samples for SDK version %s" % ebaysdk.get_version())
	(opts, args) = init_options()
	run(opts)

