import csv
from collections import Counter
import numpy as np
import json
import os

file = './data/drugs_toxicities.csv'


def to_json_node(id, name, patients):
    dict = {}
    data = {}
    data['id'] = str(id)
    data['idInt'] = id
    data['name'] = name
    data['patients'] = int(patients)
    dict['data'] = data
    dict['group'] = "nodes"
    dict['removed'] = False
    dict['selected'] = False
    dict['selectable'] = True
    dict['locked'] = False
    dict['grapped'] = False
    dict['grabbable'] = True
    dict[
        'classes'] = "fn10273 fn6944 fn9471 fn10569 fn8023 fn6956 fn6935 fn8147 fn6939 fn6936 fn6629 fn7928 fn6947 fn8612 fn6957 fn8786 fn6246 fn9367 fn6945 fn6946 fn10024 fn10022 fn6811 fn9361 fn6279 fn6278 fn8569 fn7641 fn8568 fn6943"
    return dict


def to_json_edge(source, target, weight, edge_count):
    dict = {}
    data = {}
    data['source'] = source
    data['target'] = target
    data['weight'] = weight
    data['id'] = "e" + str(edge_count)
    dict['data'] = data
    dict['group'] = "edges"
    dict['removed'] = False
    dict['selected'] = False
    dict['selectable'] = True
    dict['locked'] = False
    dict['grapped'] = False
    dict['grabbable'] = True
    dict['classes'] = ""
    return dict


with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    drugs = []
    toxicities = []
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            drugs.append(row[0])
            toxicities.append(row[3])
            line_count += 1
    print(f'Processed {line_count} lines.')

drugs = Counter(drugs).keys()
toxicities = Counter(toxicities).keys()
tox_drugs = {}
for t in toxicities:
    tox_drugs[t] = {}
    for d in drugs:
        tox_drugs[t][d] = 0

with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[3] != 'toxicity_type':
            tox_drugs[row[3]][row[0]] = 1

mapToxToNum = {"GENERAL": 0,
               "GASTROINTESTINAL": 1,
               "ENDOCRINE": 2,
               "CUTANEOUS": 3,
               "PNEUMOLOGICAL": 4,
               "ANALYTICAL": 5,
               "NEUROLOGICAL": 6,
               "OTHER": 7,
               "CARDIOLOGICAL": 8}

drugLineFiles = [
    './data/exp_by_treatment_type/tki/patient-tki_line1.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line2.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line3.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line4.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line5.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line6.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line7.csv',
    './data/exp_by_treatment_type/tki/patient-tki_line8.csv'
]

for file in drugLineFiles:
    drugsAndToxs = {}
    peopleCountPerDrug = {}

    for keys in tox_drugs:
        for keys2 in tox_drugs:
            drugs = []
            toxs_related = ('', '')
            for x in tox_drugs[keys]:
                if tox_drugs[keys][x] > 0:
                    if tox_drugs[keys2][x] > 0:
                        if keys != keys2:  # not the diagonal
                            toxs_related = (keys, keys2)
                            if drugsAndToxs.get(x) == None:
                                drugsAndToxs[x] = []
                                drugsAndToxs[x].append(toxs_related)
                            else:
                                drugsAndToxs[x].append(toxs_related)

                            peopleCountPerDrug[x] = 0

    patients = []

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                patients.append(row[0])
                drug_id = row[1]
                if peopleCountPerDrug.get(drug_id) != None:
                    peopleCountPerDrug[drug_id] += 1
                else:
                    line_count += 1
                    # print("drug does not relate to a pair o tox", drug_id)

    patients = Counter(patients).keys()

    coocMatrix = np.zeros((9, 9))

    for keys in drugsAndToxs:
        for tup in drugsAndToxs[keys]:
            i = mapToxToNum[tup[0]]
            j = mapToxToNum[tup[1]]

            coocMatrix[i][j] += int(peopleCountPerDrug[keys])  # diff patients taking the drug

    sums = []
    for i, row in enumerate(coocMatrix):
        sums.append(0)
        for j, col in enumerate(coocMatrix[i]):
            sums[i] += coocMatrix[i][j]

    # print("*")
    print(sums)
    # print("*")

    nodes = ["GENERAL", "GASTROINTESTINAL", "ENDOCRINE", "CUTANEOUS",
             "PNEUMOLOGICAL", "ANALYTICAL", "NEUROLOGICAL", "OTHER", "CARDIOLOGICAL"];

    for i, row in enumerate(coocMatrix):
        for j, col in enumerate(coocMatrix[i]):
            coocMatrix[i][j] = (coocMatrix[i][j] / len(patients)) * 100

    print(coocMatrix)

    links = []
    for i, n in enumerate(nodes):
        for j, elem in enumerate(coocMatrix[i]):
            if coocMatrix[i][j] > 0:
                addLink = True;
                for link in links:
                    if link["source"] == j and link["target"] == i:
                        addLink = False;

                if addLink:
                    links.append({"source": i, "target": j, "weight": elem})

    data = []

    for i, n in enumerate(nodes):
        data.append(to_json_node(i, n, sums[i]))

    for i, l in enumerate(links):
        data.append(to_json_edge(l["source"], l["target"], l["weight"], i))

    json_data = json.dumps(data, indent=2, sort_keys=True)

    subStrFile = "patient-tki_line"
    subStrFileIndex = file.index(subStrFile)
    index = file[subStrFileIndex + len(subStrFile): -4]

    dirname = "./jsons_tki/json_line" + str(index)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    open(dirname + "/line" + str(index) + "_tki_exp.json", "w", encoding="utf8").write(json_data)
