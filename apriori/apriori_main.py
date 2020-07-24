import apriori
import sys

# command line arguments
min_support_percent = int(sys.argv[1])
input_filepath = sys.argv[2]
output_filepath = sys.argv[3]

# initialize
transaction_list = apriori.parser(input_filepath)
min_support = len(transaction_list) / 100 * min_support_percent
min_confidence = 0

# first candidate set
candidate_dict = {}
candidate_count = 1
candidate_set = apriori.initialize(set().union(*transaction_list))

# iteration
while True:
    apriori.support_count(transaction_list, candidate_set)
    if len(apriori.pruning(candidate_set, min_support)) is 0:
        break
    else:
        candidate_set = apriori.pruning(candidate_set, min_support)
        candidate_dict[candidate_count] = candidate_set
        candidate_count += 1
        candidate_set = apriori.join(candidate_set, candidate_count)

# generate association rules and print it to the output file
association_rules_list = apriori.generating_association_rules(transaction_list, 
    candidate_dict[candidate_count-1], min_confidence, len(transaction_list))
apriori.print_association_rules(association_rules_list, output_filepath)

