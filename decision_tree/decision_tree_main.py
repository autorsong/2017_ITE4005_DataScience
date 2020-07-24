import decision_tree as dt
import sys

train_data_filepath = sys.argv[1]
test_data_filepath = sys.argv[2]
result_filepath = sys.argv[3]

res = dt.parser(train_data_filepath)
res = dt.preprocessing(res)

tree = dt.build_decision_tree(res)
test_data = dt.parser(test_data_filepath)

test_data_attribute_list = []
with open(test_data_filepath, 'r') as file:
    lines = file.read().splitlines()
    for attribute in lines[0].split('\t'):
        test_data_attribute_list.append(attribute)

with open(result_filepath, 'w') as result_file:
    for attribute in test_data_attribute_list:
        result_file.write(attribute + '\t')
    result_file.write(res["attribute_info"]["class"].keys()[0] + '\n')

    for i, record in enumerate(test_data["dataset"]):
        for attribute in test_data_attribute_list:
            result_file.write(record[attribute] + '\t')
        result_file.write(dt.prediction(tree, record, res["attribute_info"]["class"].keys()[0]) + '\n')
