import json
import csv

file_name = "top-100-https"
json_file = open(file_name + ".json","r")
objects = json.load(json_file)

output_file = open(file_name + ".csv", "wb")
output_writer = csv.writer(output_file)

output_writer.writerow(["Website", "Status", "Error", "Message"])

for obj in objects:
	row = [obj["url"], "", "", ""]
	if "status" in obj.keys():
		row[1] = obj["status"]
	if "type" in obj.keys():
		row[2] = obj["type"]
	if "reason" in obj.keys():
		row[3] = obj["reason"]
	output_writer.writerow(row)

output_file.close()




