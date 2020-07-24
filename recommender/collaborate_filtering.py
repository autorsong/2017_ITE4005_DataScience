from math import pow, sqrt


def add_float(value):
    if value > 0:
        return value
    else:
        return 1


def parser(input_filepath):
    with open(input_filepath, 'r') as input_file:
        max_user = 0
        max_movie = 0

        for line in input_file:
            parsed_line = line.split('\t')

            max_user = max_user if max_user > int(parsed_line[0]) else int(parsed_line[0])
            max_movie = max_movie if max_movie > int(parsed_line[1]) else int(parsed_line[1])

        rating_matrix = []
        for i in range(max_user + 1):
            rating_matrix.append([0] * (max_movie + 1))

        input_file.seek(0)

        for line in input_file:
            parsed_line = map(int, line.split('\t'))
            rating_matrix[parsed_line[0]][parsed_line[1]] = parsed_line[2]

        return rating_matrix


def similarity(rating_matrix):
    user_similarity_matrix = []
    user_average_rating_matrix = [0] * len(rating_matrix)
    for i in range(len(rating_matrix)):
        user_similarity_matrix.append([0] * len(rating_matrix))

    for index, user in enumerate(rating_matrix):
        if index == 0:
            continue
        else:
            user_average_rating_matrix[index] = float(sum(user)) / add_float(float(len([x for x in user if x > 0])))

    for index_a, user_a in enumerate(rating_matrix):
        for index_b, user_b in enumerate(rating_matrix):
            if index_a > index_b or index_b == 0:
                continue
            if index_a > (len(rating_matrix) / 2) + 1:
                break

            common_rating_list = []
            for index in xrange(len(rating_matrix[0])):
                if user_a[index] > 0 and user_b[index] > 0:
                    common_rating_list.append(index)

            user_a_avg = user_average_rating_matrix[index_a]
            user_b_avg = user_average_rating_matrix[index_b]

            dividend = float(0.0)
            divisor_a = float(0.0)
            divisor_b = float(0.0)

            for index in common_rating_list:
                dividend += (user_a[index] - user_a_avg) * (user_b[index] - user_b_avg)
                divisor_a += pow((user_a[index] - user_a_avg), 2)
                divisor_b += pow((user_b[index] - user_b_avg), 2)

            user_similarity_matrix[index_a][index_b] = dividend / add_float((sqrt(divisor_a) * sqrt(divisor_b)))
            user_similarity_matrix[index_b][index_a] = user_similarity_matrix[index_a][index_b]

    return user_similarity_matrix


def predict_rating(rating_matrix, user_similarity_matrix, user, movie):
    similar_user_list = []

    if user >= len(rating_matrix):
        movie_sum = []
        for index in range(len(rating_matrix)):
            if rating_matrix[index][movie] > 0:
                movie_sum.append(rating_matrix[index][movie])
        return float(sum(movie_sum)) / add_float(float(len(movie_sum)))

    if movie >= len(rating_matrix[0]):
        return float(sum(rating_matrix[user])) / add_float(float(len([x for x in rating_matrix[user] if x > 0])))

    for index, rating in enumerate(user_similarity_matrix[user]):
        if rating > 0.5 and rating_matrix[index][movie] > 0:
            similar_user_list.append(index)

    if len(similar_user_list) >= 5:
        rating_sum = float(0.0)
        for index in similar_user_list:
            rating_sum += rating_matrix[index][movie]
        return float(rating_sum) / float(len(similar_user_list))
    else:
        user_average = float(sum(rating_matrix[user])) / add_float(float(len([x for x in rating_matrix[user] if x > 0])))

        movie_sum = []
        for index in range(len(rating_matrix)):
            if rating_matrix[index][movie] > 0:
                movie_sum.append(rating_matrix[index][movie])
        movie_average = float(sum(movie_sum)) / add_float(float(len(movie_sum)))

        return (user_average + movie_average) / 2
