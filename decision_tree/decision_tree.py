import math


def parser(filepath):
    with open(filepath) as file:
        lines = file.read().splitlines()

    attribute_list = []
    train_dataset = []
    for attribute in lines[0].split('\t'):
        attribute_list.append(attribute)

    for line in lines[1:]:
        value_count = 0
        temp_dict = {}
        for value in line.split('\t'):
            temp_dict[attribute_list[value_count]] = value
            value_count += 1

        train_dataset.append(temp_dict)

    res = {}
    res["attribute_list"] = attribute_list
    res["dataset"] = train_dataset

    return res


def preprocessing(data):
    attribute_info = {"attribute": {}, "class": {}}
    train_data = []
    for i, attribute in enumerate(data["attribute_list"]):
        if i < len(data["attribute_list"]) - 1:
            attribute_info["attribute"][attribute] = set([])
        else:
            attribute_info["class"][attribute] = set([])

    for record in data["dataset"]:
        temp_record = {"attribute": {}, "class": {}}
        for key in record:
            if key in attribute_info["attribute"]:
                attribute_info["attribute"][key].add(record[key])
                temp_record["attribute"][key] = record[key]
            else:
                attribute_info["class"][key].add(record[key])
                temp_record["class"][key] = record[key]
        train_data.append(temp_record)

    res = {}
    res["attribute_info"] = attribute_info
    res["train_data"] = train_data

    return res


def calculate_entropy(data):
    class_dict = {}
    for class_element in data["attribute_info"]["class"].values()[0]:
        class_dict[class_element] = 0

    for record in data["train_data"]:
        class_dict[record["class"].values()[0]] += 1

    entropy = float(0)
    record_count = len(data["train_data"])

    for class_element in class_dict:
        if class_dict[class_element] > 0 and record_count > 0:
            ratio = float(class_dict[class_element]) / float(record_count)
            entropy += -(ratio * math.log(ratio, 2))
        else:
            entropy += 0

    return entropy


def calculate_information_gain(data, attribute):
    origin_entropy = calculate_entropy(data)
    information_gain = origin_entropy

    information_gain_dict = {}
    attribute_subset_dict = {}

    for value in data["attribute_info"]["attribute"][attribute]:
        attribute_subset_dict[value] = []

    for record in data["train_data"]:
        attribute_subset_dict[record["attribute"][attribute]].append(record)

    for value in attribute_subset_dict:
        subset_data = {}
        subset_data["train_data"] = attribute_subset_dict[value]
        subset_data["attribute_info"] = data["attribute_info"]
        information_gain_dict[value] = calculate_entropy(subset_data)

    for value in attribute_subset_dict:
        if len(data["train_data"]) > 0:
            information_gain -= float(len(attribute_subset_dict[value])) / float(len(data["train_data"])) * information_gain_dict[value]

    return information_gain


def select_attribute(data):
    if len(data["attribute_info"]["attribute"]) is 0:
        return None

    information_gain_dict = {}

    for attribute in data["attribute_info"]["attribute"]:
        information_gain_dict[attribute] = calculate_information_gain(data, attribute)

    highest_info_gain = sorted(information_gain_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True)[0]
    if highest_info_gain[1] > float(0.0):
        return highest_info_gain[0]
    else:
        return None


def build_decision_tree(data):
    tree = {}

    divider_attribute = select_attribute(data)

    if len(data["attribute_info"]["attribute"]) is 0 or divider_attribute is None:
        for value in data["attribute_info"]["class"].values()[0]:
            tree[value] = 0
        for record in data["train_data"]:
            tree[record["class"].values()[0]] += 1
        tree["is_leafnode"] = -1
        return tree

    tree["attribute"] = divider_attribute

    divided_train_data = {}
    for value in data["attribute_info"]["attribute"][divider_attribute]:
        divided_train_data[value] = []

    sub_attribute_info = {"attribute": {}, "class": {}}
    for attribute in data["attribute_info"]["attribute"]:
        sub_attribute_info["attribute"][attribute] = data["attribute_info"]["attribute"][attribute]
    sub_attribute_info["class"] = data["attribute_info"]["class"]
    del sub_attribute_info["attribute"][divider_attribute]

    for record in data["train_data"]:
        value = record["attribute"][divider_attribute]
        divided_train_data[value].append(record)

    for divided_list in divided_train_data:
        subset_data = {}
        subset_data["train_data"] = divided_train_data[divided_list]
        subset_data["attribute_info"] = sub_attribute_info
        if len(divided_train_data[divided_list]) > 0:
            tree[divided_list] = build_decision_tree(subset_data)

    return tree


def prediction(tree, record, class_name):
    temp_tree = dict(tree)
    while "is_leafnode" not in temp_tree:
        if record[temp_tree["attribute"]] in temp_tree:
            temp_tree = temp_tree[record[temp_tree["attribute"]]]
        else:
            alter_prediction_dict = {}
            alter_prediction(temp_tree, alter_prediction_dict)
            return sorted(alter_prediction_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True)[0][0]

    return sorted(temp_tree.iteritems(), key=lambda (k, v): (v, k), reverse=True)[0][0]


def alter_prediction(tree, alter_prediction_dict):
    for attribute in tree:
        if "is_leafnode" in tree:
            for value in tree:
                if value in alter_prediction_dict:
                    alter_prediction_dict[value] += tree[value]
                else:
                    alter_prediction_dict[value] = tree[value]
        else:
            if attribute is not "attribute":
                alter_prediction(tree[attribute], alter_prediction_dict)
