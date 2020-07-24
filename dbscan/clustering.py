import dbscan
import sys

input_file = sys.argv[1]
cluster_num = int(sys.argv[2])
epsilon = int(sys.argv[3])
minpts = int(sys.argv[4])


point_list = dbscan.parser(input_file)
dbscan.get_near_point(point_list, epsilon, minpts)

mark_list = dbscan.dbscan(point_list, cluster_num, epsilon, minpts)
dbscan.post_clustering(cluster_num, mark_list, point_list)

for i in range(0, cluster_num):
    with open(input_file.split('.')[0] + '_cluster_' + str(i) + '.txt', 'w') as writefile:
        writefile.seek(0)
        for index, num in enumerate(mark_list):
            if num is not None and num == i:
                writefile.write(str(index) + '\n')
