
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
        dict_drugs = {}  # contains all possible drug ids with the toxicity types they are related to
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                did = row[0]  # drug id
                tox_type = row[3]
                if did in dict_drugs.keys():
                    dict_drugs[did].add(tox_type)
                else:
                    dict_drugs[did] = set()
                    dict_drugs[did].add(tox_type)
                drugs.append(did)
                toxicities.append(tox_type)
                line_count += 1
        # print(f'Processed {line_count} lines.')

    drugs = Counter(drugs).keys()
    toxicities = Counter(toxicities).keys()
    drug_in_tox = {}  # specifies if a drug belongs to a toxicity type
    for t in toxicities:
        drug_in_tox[t] = {}
        for d in drugs:
            drug_in_tox[t][d] = 0

    # set drug_in_tox[t][d] to 1 for all occurrences in the data
    with open(file_drugs_toxs) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                did = row[0]
                tox_type = row[3]
                drug_in_tox[tox_type][did] = 1

    return drug_in_tox, dict_drugs


def init_drugs_and_tox_people_cnt_drug(drug_in_tox):
    drugs_rel_toxs = {}  # drugs ids as object props with all possible pair of toxicities related to it
    patient_cnt_per_drug = {}

    for key_t1 in drug_in_tox:
        for key_t2 in drug_in_tox:
            for did in drug_in_tox[key_t2]:
                if drug_in_tox[key_t1][did] > 0:
                    if drug_in_tox[key_t2][did] > 0:
                        if key_t1 != key_t2:  # not the diagonal
                            toxs_related = (key_t1, key_t2)
                            if drugs_rel_toxs.get(did) is None:
                                drugs_rel_toxs[did] = []
                                drugs_rel_toxs[did].append(toxs_related)
                            else:
                                drugs_rel_toxs[did].append(toxs_related)

                            patient_cnt_per_drug[did] = 0

    return drugs_rel_toxs, patient_cnt_per_drug


def get_patients_from_file(file, patient_cnt_per_drug, dict_drugs, mode):
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
                    if did not in dict_drugs.keys():
                        continue
                    if f != file_non_onco:
                        patients.append(pid)
                        if pid not in patient_tox.keys():
                            patient_tox[pid] = set()

                    for tox in dict_drugs[did]:
                        if pid in patient_tox.keys():
                            patient_tox[pid].add(tox)

                    if (patient_cnt_per_drug.get(did) is not None) and (pid in patients):
                        patient_cnt_per_drug[did] += 1
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
        drugs_rel_toxs, patient_cnt_per_drug = init_drugs_and_tox_people_cnt_drug(tox_patients)
    else:
        drugs_rel_toxs = None

    return patients, patient_tox, patient_cnt_per_drug, drugs_rel_toxs


def calculate_cooccurrence_matrix(drugs_rel_toxs, patient_cnt_per_drug, patients):
    coocMatrix = np.zeros((9, 9))

    for keys in drugs_rel_toxs:
        for tup in drugs_rel_toxs[keys]:
            i = mapToxToNum[tup[0]]
            j = mapToxToNum[tup[1]]
            if patient_cnt_per_drug is None:
                coocMatrix[i][j] += 1
            else:
                coocMatrix[i][j] += int(patient_cnt_per_drug[keys])  # different number of patients taking the drug

    for i, row in enumerate(coocMatrix):
        for j, col in enumerate(coocMatrix[i]):
            if len(patients) > 0:
                coocMatrix[i][j] = (coocMatrix[i][j] / len(patients)) * 100

    # print(coocMatrix)
    return coocMatrix


def get_file_list(dir):
    return sorted(os.path.join(dir, file) for file in os.listdir(dir))


if __name__ == "__main__":
    drug_in_tox, dict_drugs = get_tox_drugs()

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
                patient_cnt_per_drug = None
                if mode == "obs":
                    patients, patient_tox, _, drugs_rel_toxs = get_patients_from_file(file, None, dict_drugs, mode)
                else:
                    drugs_rel_toxs, patient_cnt_per_drug = init_drugs_and_tox_people_cnt_drug(drug_in_tox)
                    patients, patient_tox, patient_cnt_per_drug, _ = get_patients_from_file(file, patient_cnt_per_drug, dict_drugs, mode)

                coocMatrix = calculate_cooccurrence_matrix(drugs_rel_toxs, patient_cnt_per_drug, patients)

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

                                npatients = 0
                                for patient in patient_tox.keys():
                                    if src in patient_tox[patient] and dest in patient_tox[patient]:
                                        npatients += 1
                                links.append({"source": i, "target": j, "weight": elem, "patients": npatients})

                data = []

                for i, n in enumerate(nodes):
                    for k, v in mapToxToNum.items():
                        if v == i:
                            src = k

                    npat = 0
                    for patient in patient_tox.keys():
                        if src in patient_tox[patient]:
                            npat += 1

                    data.append(to_json_node(i, n, npat))

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
