import sys
import time
import collaborate_filtering as cf

input_filepath = sys.argv[1]
test_filepath = sys.argv[2]
output_filepath = sys.argv[1] + '_prediction.txt'

start_time = time.time()

print "- parsing input file.."
base_rating_matrix = cf.parser(input_filepath)

print "- calculating similarity of each pair of users.."
user_similarity_matrix = cf.similarity(base_rating_matrix)

print "- generating predicted rating.."
with open(test_filepath, 'r') as testfile:
    with open(output_filepath, 'w') as writefile:
        for i, line in enumerate(testfile):
            parsed_line = line.split('\t')

            user = int(parsed_line[0])
            movie = int(parsed_line[1])
            expected_rating = cf.predict_rating(base_rating_matrix, user_similarity_matrix, user, movie)

            writefile.write(str(user) + '\t' + str(movie) + '\t' + str(expected_rating) + '\n')

print("--- %s seconds ---" % (time.time() - start_time))
