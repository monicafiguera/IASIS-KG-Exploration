
import csv
from collections import Counter
import numpy as np
import json
import os
import math


file_drugs_toxs = './data/drugs_toxicities.csv'
file_non_onco = './data/nonOncologycalTreatments.csv'
mapToxToNum = {
    "GENERAL": 0,
    "GASTROINTESTINAL": 1,
    "ENDOCRINE": 2,
    "CUTANEOUS": 3,
    "PNEUMOLOGICAL": 4,
    "ANALYTICAL": 7,
    "NEUROLOGICAL": 6,
    "OTHER": 5,
    "CARDIOLOGICAL": 8
}
nodes = ["GENERAL", "GASTROINTESTINAL", "ENDOCRINE", "CUTANEOUS", "PNEUMOLOGICAL",
         "OTHER", "NEUROLOGICAL", "ANALYTICAL", "CARDIOLOGICAL"]
modes = ["exp", "exp_and_noonco", "obs"]
treatments = ["all", "ant", "imm", "qt", "tki"]


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
    dict['locked'] = True
    dict['grapped'] = False
    dict['grabbable'] = True
    dict['classes'] = "fn10273 fn6944 fn9471 fn10569 fn8023 fn6956 fn6935 fn8147 fn6939 fn6936 fn6629 fn7928 fn6947 fn8612 fn6957 fn8786 fn6246 fn9367 fn6945 fn6946 fn10024 fn10022 fn6811 fn9361 fn6279 fn6278 fn8569 fn7641 fn8568 fn6943"
    dict['position'] = id_to_pos(id)
    return dict


def id_to_pos(id):
    """
    Calculates the coordinates of a node in a nonagon.
    :param id: the id of the node
    :return: x- and y-coordinate of the node in a nonagon
    """
    position = {}
    radius = 180
    position['x'] = radius * math.cos(math.radians(-90 + id * 40))
    position['y'] = radius * math.sin(math.radians(-90 + id * 40))
    return position


def to_json_edge(source, target, weight, patients, edge_count):
    dict = {}
    data = {}
    data['source'] = source
    data['target'] = target
    data['weight'] = weight
    data['id'] = "e" + str(edge_count)
    data['patients'] = patients
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


def get_tox_drugs():
    with open(file_drugs_toxs) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        drugs = []
        toxicities = []
        dict_drugs = {}
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[0] in dict_drugs.keys():
                    dict_drugs[row[0]].add(row[3])
                else:
                    dict_drugs[row[0]] = set()
                    dict_drugs[row[0]].add(row[3])
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

    # set tox_drugs[t][d] to 1 for all occurrences in the data
    with open(file_drugs_toxs) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[3] != 'toxicity_type':
                tox_drugs[row[3]][row[0]] = 1

    return tox_drugs, dict_drugs


def init_drugs_and_tox_people_cnt_drug(tox_drugs):
    drugsAndToxs = {}
    peopleCountPerDrug = {}

    for keys in tox_drugs:
        for keys2 in tox_drugs:
            toxs_related = ('', '')
            for x in tox_drugs[keys]:
                if tox_drugs[keys][x] > 0:
                    if tox_drugs[keys2][x] > 0:
                        if keys != keys2:  # not the diagonal
                            toxs_related = (keys, keys2)
                            if drugsAndToxs.get(x) is None:
                                drugsAndToxs[x] = []
                                drugsAndToxs[x].append(toxs_related)
                            else:
                                drugsAndToxs[x].append(toxs_related)

                            peopleCountPerDrug[x] = 0

    return drugsAndToxs, peopleCountPerDrug


def get_patients_from_file(file, peopleCountPerDrug, dict_drugs, mode):
    files_to_analyze = [file]
    if mode == "exp_and_noonco":
        files_to_analyze.append(file_non_onco)
    if mode == "obs":
        toxicities = []

    patients = []
    patient_tox = {}

    for f in files_to_analyze:
        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif mode == "obs":
                    pid = row[0]
                    tox = row[1]
                    patients.append(pid)
                    toxicities.append(tox)
                    if pid not in patient_tox.keys():
                        patient_tox[pid] = set()
                    patient_tox[pid].add(tox)
                else:
                    pid = row[0]
                    did = row[1]
                    patients.append(pid)
                    if did not in dict_drugs.keys():
                        continue
                    if pid not in patient_tox.keys():
                        patient_tox[pid] = set()

                    for tox in dict_drugs[did]:
                        patient_tox[pid].add(tox)

                    if peopleCountPerDrug.get(did) != None:
                        peopleCountPerDrug[did] += 1
                    else:
                        line_count += 1
                        # print("drug does not relate to a pair o tox", drug_id)

    patients = Counter(patients).keys()
    if mode == "obs":
        toxicities = Counter(toxicities).keys()
        tox_patients = {}
        for t in toxicities:
            tox_patients[t] = {}
            for p in patients:
                tox_patients[t][p] = 0

        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    tox_patients[row[1]][row[0]] = 1
        drugsAndToxs, peopleCountPerDrug = init_drugs_and_tox_people_cnt_drug(tox_patients)
    else:
        drugsAndToxs = None

    return patients, patient_tox, peopleCountPerDrug, drugsAndToxs


def calculate_cooccurrence_matrix(drugsAndToxs, peopleCountPerDrug, patients):
    coocMatrix = np.zeros((9, 9))

    for keys in drugsAndToxs:
        for tup in drugsAndToxs[keys]:
            i = mapToxToNum[tup[0]]
            j = mapToxToNum[tup[1]]
            if peopleCountPerDrug is None:
                coocMatrix[i][j] += 1
            else:
                coocMatrix[i][j] += int(peopleCountPerDrug[keys])  # diff patients taking the drug

    sums = []
    for i, row in enumerate(coocMatrix):
        sums.append(0)
        for j, col in enumerate(coocMatrix[i]):
            sums[i] += coocMatrix[i][j]

    # print("*")
    # print(sums)
    # print("*")

    for i, row in enumerate(coocMatrix):
        for j, col in enumerate(coocMatrix[i]):
            if len(patients) > 0:
                coocMatrix[i][j] = (coocMatrix[i][j] / len(patients)) * 100

    # print(coocMatrix)
    return coocMatrix, sums


def get_file_list(dir):
    return sorted(os.path.join(dir, file) for file in os.listdir(dir))


if __name__ == "__main__":
    tox_drugs, dict_drugs = get_tox_drugs()

    for mode in modes:
        for treat in treatments:
            if mode == "obs":
                # observed
                if treat == "all":
                    files_to_be_processed = get_file_list('./data/Patient_Tox_by_Treatment_Line_v2')
                else:
                    dir = './data/obs_by_treatment_type/' + treat
                    files_to_be_processed = get_file_list(dir)
            else:
                # files are the same for exp and exp_noonco
                if treat == "all":
                    files_to_be_processed = get_file_list('./data/patient_drug_by_treatment_line_v2')
                else:
                    dir = './data/exp_by_treatment_type/' + treat
                    files_to_be_processed = get_file_list(dir)

            # process all the files
            for file in files_to_be_processed:
                peopleCountPerDrug = None
                if mode == "obs":
                    patients, patient_tox, _, drugsAndToxs = get_patients_from_file(file, None, dict_drugs, mode)
                else:
                    drugsAndToxs, peopleCountPerDrug = init_drugs_and_tox_people_cnt_drug(tox_drugs)
                    patients, patient_tox, peopleCountPerDrug, _ = get_patients_from_file(file, peopleCountPerDrug, dict_drugs, mode)

                coocMatrix, sums = calculate_cooccurrence_matrix(drugsAndToxs, peopleCountPerDrug, patients)

                links = []
                for i, n in enumerate(nodes):
                    for j, elem in enumerate(coocMatrix[i]):
                        if coocMatrix[i][j] > 0:
                            addLink = True
                            for link in links:
                                if link["source"] == j and link["target"] == i:
                                    addLink = False

                            if addLink:
                                src = dest = ''
                                for k, v in mapToxToNum.items():
                                    if v == i:
                                        src = k
                                    if v == j:
                                        dest = k

                                # npatients = []
                                npatients = 0
                                for patient in patient_tox.keys():
                                    if src in patient_tox[patient] and dest in patient_tox[patient]:
                                        # npatients.append(patient)
                                        npatients += 1
                                links.append({"source": i, "target": j, "weight": elem, "patients": npatients})

                data = []

                for i, n in enumerate(nodes):
                    data.append(to_json_node(i, n, sums[i]))

                for i, l in enumerate(links):
                    data.append(to_json_edge(l["source"], l["target"], l["weight"], l["patients"], i))

                json_data = json.dumps(data, indent=2, sort_keys=True)

                subStrFile = "_line"
                subStrFileIndex = file.rindex(subStrFile)
                index = file[subStrFileIndex + len(subStrFile): -4]

                dirname = "./jsons_" + treat
                if not os.path.exists(dirname):
                    os.mkdir(dirname)

                filename = "/line" + str(index) + "_" + treat + "_" + mode + ".json"
                open(dirname + filename, "w", encoding="utf8").write(json_data)
