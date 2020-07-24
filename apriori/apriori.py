from itertools import chain, combinations


def parser(filepath):
    with open(filepath) as file:
        lines = file.read().splitlines()

    transaction_list = []

    for line in lines:
        temp = set()
        for value in line.split('\t'):
            temp.add(value)
        transaction_list.append(temp)

    return transaction_list


def initialize(value_set):
    candidate_list = []

    for value in value_set:
        temp_dict = {}
        temp_set = set([])
        temp_set.add(value)

        temp_dict['set'] = temp_set
        temp_dict['support'] = 0

        candidate_list.append(temp_dict)

    return candidate_list


def support_count(transaction_list, candidate_list):
    for candidate in candidate_list:
        for transaction in transaction_list:
            if len(candidate['set'].difference(transaction)) == 0:
                candidate['support'] = candidate['support'] + 1


def pruning(candidate_list, min_support):
    return [x for x in candidate_list if (x.get('support') > min_support)]


def join(candidate_list, iter_count):
    candidate_join_list = []

    for candidate_1 in candidate_list:
        for candidate_2 in candidate_list:
            union_set = candidate_1['set'].union(candidate_2['set'])
            if len(union_set) is iter_count and union_set not in [li['set'] for li in candidate_join_list]:
                temp_dict = {}
                temp_dict['set'] = union_set
                temp_dict['support'] = 0

                candidate_join_list.append(temp_dict)

    return candidate_join_list


def generating_association_rules(transaction_list, candidate_list, min_confidence, transaction_count):
    association_rules_list = []
    for candidate in candidate_list:
        candidate_subset = [x for x in chain.from_iterable(combinations(candidate['set'], r) 
            for r in range(1, len(candidate['set'])))]

        for subset in candidate_subset:
            itemset = set(subset)
            associative_itemset = candidate['set'].difference(itemset)
            confidence_count = 0
            count = 0

            for transaction in transaction_list:
                if len(itemset.difference(transaction)) is 0:
                    count += 1
                    if len(associative_itemset.difference(transaction)) is 0:
                        confidence_count += 1

            confidence = float(confidence_count) / float(count) * 100
            support = float(candidate['support']) / float(transaction_count) * 100

            temp_dict = {}
            temp_dict['itemset'] = itemset
            temp_dict['associative_itemset'] = associative_itemset
            temp_dict['confidence'] = confidence
            temp_dict['support'] = support

            association_rules_list.append(temp_dict)

    return association_rules_list


def print_association_rules(association_rules_list, write_file_name):
    write_file = open(write_file_name, 'w')

    for rule in association_rules_list:
        write_file.write("{" + ",".join(str(item) for item in rule['itemset'])
            + "}\t{" + ",".join(str(item) for item in rule['associative_itemset'])
            + "}\t" + str("%.2f" % rule['support'])
            + "\t" + str("%.2f" % rule['confidence']) + "\n")

    write_file.close()
