import json
import csv
import sys

file_name = sys.argv[1]

json_file = open(file_name + ".json","r")
objects = json.load(json_file)

output_file = open(file_name + ".csv", "wb")
output_writer = csv.writer(output_file)

output_writer.writerow(["URL", file_name + "-status", file_name + "-flags", file_name + "-number_of_tags", file_name + "-length", file_name + "-error_message", file_name + "-error_type"])

for obj in objects:
	row = [obj["url"], obj["status"], obj["flags"], obj["number_of_tags"], obj["length"], obj["error_message"], obj["error_type"]]
	output_writer.writerow(row)
						
output_file.close()




