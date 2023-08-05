class compute_completeness():
	def __init__(self):
		pass 
	def run(self,data):
		counter = 0
		for key in data[0].keys():
			# assert key in ['price','sqft','bed','bath','number_units','year_built',
			# 			   'year_renovated','listing_type','enhanced_amenities'], "The input column is not correct"
			if key == "enhanced_amenities":
				counter_list = [x[key] for x in data if x[key] is not None]
				filter_list = ('unit','building')
				filtered = [any(s in x for s in filter_list) for x in counter_list]
				counter += len(filter(lambda x: x is True, filtered))
			# print counter
			else:
				counter_list = [x[key] for x in data if x[key] is not None]
				counter += len(counter_list)

		raw_score = float(counter)/(len(data)*len(data[0].keys()))
		return raw_score
    


# data = [{'price':1000,'sqft':250,'bed':1,'bath':0,'number_units':1,'year_built':None,'year_renovated':None,'listing_type':'House','enhanced_amenities':'unit_has_kkk'},
# 		{'price':1500,'sqft':250,'bed':1,'bath':0,'number_units':100,'year_built':None,'year_renovated':1900,'listing_type':'House','enhanced_amenities':'kkk_has_kkk'}]
# result = compute_completeness().run(data)
# print result

