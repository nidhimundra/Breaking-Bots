import json
import csv
import sys

output_file = open("output.csv", "wb")
output_writer = csv.writer(output_file)

file_names = sys.argv[1:]

fields = ["status", "flags", "number_of_tags", "length", "error_message", "error_type"]
top_row = ["URL"]

# Create the top row
for field in fields:
	for file_name in file_names:
		top_row.append(file_name + '-' + field)

output_writer.writerow(top_row)

# Initialize dictionary
output = {}

for file_name in file_names:
	json_file = open(file_name + ".json","r")
	objects = json.load(json_file)
	for obj in objects:
		domain = obj["url"].split("//")[-1].split("/")[0].split('www.')[-1]
		if domain not in output.keys():
			output[domain] = {}
		for field in fields:
			output[domain][file_name + '-' + field] = obj[field]

for domain, values in output.iteritems():
	row = []
	desired_number_of_keys = len(top_row)-1
	if len(values.keys()) == desired_number_of_keys:
		for key in top_row:
			if key == "URL":
				row.append(domain)
			else:
				row.append(values[key])
	output_writer.writerow(row)
						
output_file.close()




