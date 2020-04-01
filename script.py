import csv
from datetime import datetime, timedelta
from functools import reduce
import matplotlib.pyplot as plt

plt.style.use('seaborn-pastel')

data_source = "confirmed"
# data_source = "Deaths"
threshold = 100

with open("csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_" + data_source + "_global.csv") as f:
	reader = csv.DictReader(f)
	time_series = [l for l in reader]
	time_series_fields = reader.fieldnames


# first get a list of all the dates available.
# they seem to be everyt day from 1/22/20

# lets plot Pakistan over time.

parse_date = lambda d: datetime.strptime(d, "%m/%d/%y")

date_fields = time_series_fields[4:]

country_sets = [
	{
		"title": "country-comparison",
		"countries": [
			["", "Iran"],
			["", "Korea, South"],
			["", "Italy"],
			["", "US"],
			["", "Pakistan"],
			["", "India"]
		],
	},
# 	{
# 		"title": "states",
# 		"countries": [
# 			["New York", "US"],
# 			["New Jersey", "US"],
# 			["Massachusetts", "US"],
# 			["California", "US"],
# 			["Arizona", "US"],
# 		]
# 
# 	}
]

country_data = { }
country_plot_data = { }

fig = plt.figure()

def reducer(relevant):

	combined = {}
	for curr in relevant:
		for d in date_fields:
			old = int(combined.get(d, 0))
			c = curr.get(d)
			if c == '':
				c = '0'
			combined[d] = old + int(c)

	return combined

for group in country_sets:

	for c in group["countries"]:

		country_agg = c[0] == ""
		c_key = c[1] if country_agg else c[0] + ", " + c[1]

		c_data = {}
		relevant = filter(lambda row: row["Country/Region"] == c[1] and row["Province/State"] == c[0], time_series) if not country_agg else filter(lambda row: row["Country/Region"] == c[1], time_series)

		if country_agg:
			c_data = reducer(relevant)
			# c_data = reduce(lambda curr, agg: {d: int(agg[d]) + int(curr[d]) for d in date_fields}, relevant)
		else:
			c_data = list(relevant)[0]

		country_data[c_key] = c_data

		y_data = []
		for d in date_fields:
			if int(c_data[d]) >= threshold:
				y_data.append(int(c_data[d]))
		
		country_plot_data[c_key] = {"y": y_data}

		if c_key == "Pakistan":
			print(c_key, len(y_data))
			plt.plot(y_data, label=c_key, color="red")
		elif c_key == "India":
			print(c_key, len(y_data))
			plt.plot(y_data, label=c_key, color="orange")
		else:
			print(c_key, len(y_data))
			plt.plot(y_data, label=c_key)


	title = group["title"]
	plt.title(data_source + " Cases")
	plt.legend()
	plt.xlabel("Number of Days since " + str(threshold) + "th " + data_source + " Case")
	plt.yscale('log')
	plt.tight_layout()
	plt.plot()
	plt.savefig(title, dpi=360)
	plt.close()
# plt.show()