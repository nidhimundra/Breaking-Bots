import csv
from sklearn.cluster import KMeans

K = 5
data_arr = []
url_name_arr = []
MY_FILE = 'output.csv'
top_row = []
errors = {"HttpError": 1, "DNSLookupError": 2, "TimeoutError": 3, "Other": 4}

with open(MY_FILE, 'rb') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            top_row = row
            continue
        data = []
        for i, e in enumerate(row):
            if i == 0:
                url_name_arr.append(e)
            elif '[' in e and ']' in e:
                data.append(len(e) - 2)
            elif str.isdigit(e):
                data.append(int(e))
            elif e in errors.keys():
                data.append(errors[e])
            else:
            	if "status" in top_row[i]:
            		data.append(500)
            	elif "flags" in top_row[i]:
            		data.append(0)
            	elif "number_of_tags" in top_row[i]:
            		data.append(1500)
            	elif "length" in top_row[i]:
            		data.append(2000)
            	elif "error_message" in top_row[i]:
            		data.append(0)
            	elif "error_type" in top_row[i]:
            		data.append(5)


        if len(data) > 0:
            data_arr.append(data)

top_row.append("Label")
output_file = open("clustered_output_" + str(K) + ".csv", "wb")
output_writer = csv.writer(output_file)
output_writer.writerow(top_row)

# computing K-Means with K (clusters)
estimator = KMeans(n_clusters=K)

centroids = estimator.fit_predict(data_arr)

labels = estimator.labels_

for k in range(K):
	c = 0
	for i in range(len(data_arr)):
		if labels[i] == k:
			c += 1
			row = []
			row.append(url_name_arr[i])
			row = row + data_arr[i]
			row.append(k)
			output_writer.writerow(row)
	print "Cluster " + str(k) + " size: " + str(c)

output_writer.writerow([])

output_writer.writerow(["Results"])

k = 0
for cluster_center in estimator.cluster_centers_:
	row = ["Cluster"]
	for c in cluster_center:
		row.append(c)
	row.append(k)
	output_writer.writerow(row)
	k += 1


	
