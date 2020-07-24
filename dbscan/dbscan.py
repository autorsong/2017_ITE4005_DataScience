from math import sqrt, fabs
import sys

NOT_VISITED = -1
VISITED = True
NOISE = None


def parser(filepath):
    point_list = []
    with open(filepath, 'r') as readfile:
        for line in readfile:
            parsed_data = line.split('\t')
            temp_dict = {}
            temp_dict['num'] = int(parsed_data[0])
            temp_dict['x'] = float(parsed_data[1])
            temp_dict['y'] = float(parsed_data[2])

            point_list.append(temp_dict)

    return point_list


def euclidean_distance(point_a, point_b):
    return sqrt(pow(fabs(point_a['x'] - point_b['x']), 2) + pow(fabs(point_a['y'] - point_b['y']), 2))


def get_near_point(point_list, epsilon, minpts):
    for point in point_list:
        point['near_point_list'] = []

        for target_point in point_list:
            if euclidean_distance(target_point, point) <= epsilon:
                point['near_point_list'].append(target_point)

        sys.stdout.write('\r')
        sys.stdout.write("get near point... %d%% (%s / %d)" % ((point['num'] + 1) * 100 / len(point_list), point['num'] + 1, len(point_list)))
        sys.stdout.flush()
    print ""


def dbscan(point_list, cluster_num, epsilon, minpts):
    cluster_index = 0
    mark_list = [NOT_VISITED] * len(point_list)

    print "clustering..."

    for point in point_list:
        if mark_list[point['num']] is NOT_VISITED:
            if expand_cluster(point, point_list, mark_list, cluster_index, minpts):
                cluster_index += 1

    return mark_list


def expand_cluster(point, point_list, mark_list, cluster_index, minpts):
    if len(point['near_point_list']) < minpts:
        mark_list[point['num']] = NOISE
        return False

    else:
        temp_queue = []
        mark_list[point['num']] = cluster_index
        for near_point in point['near_point_list']:
            mark_list[near_point['num']] = cluster_index
            temp_queue.append(near_point)

        while len(temp_queue) > 0:
            temp_point = temp_queue[0]
            if len(temp_point['near_point_list']) >= minpts:
                for i in range(0, len(temp_point['near_point_list'])):
                    result_point = temp_point['near_point_list'][i]
                    if mark_list[result_point['num']] is NOT_VISITED or mark_list[result_point['num']] is NOISE:
                        if mark_list[result_point['num']] is NOT_VISITED:
                            temp_queue.append(result_point)
                        mark_list[result_point['num']] = cluster_index

            temp_queue = temp_queue[1:]

        return True


def post_clustering(cluster_num, mark_list, point_list):
    print "post clustering..."
    for num in range(0, len(mark_list)):
        if mark_list[num] is not None and mark_list[num] >= cluster_num:
            count_list = [0] * cluster_num
            for near_point in find_point_by_num(point_list, num)['near_point_list']:
                if mark_list[near_point['num']] is not None and mark_list[near_point['num']] < cluster_num:
                    count_list[mark_list[near_point['num']]] += 1

            max_index = 0
            max_count = 0
            for index, count in enumerate(count_list):
                if count > max_count:
                    max_count = count
                    max_index = index

            mark_list[num] = max_index


def find_point_by_num(point_list, point_num):
    for point in point_list:
        if point['num'] == point_num:
            return point
