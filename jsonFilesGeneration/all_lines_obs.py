import csv
from collections import Counter
import numpy as np
import json
import os

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
    dict['classes'] = "fn10273 fn6944 fn9471 fn10569 fn8023 fn6956 fn6935 fn8147 fn6939 fn6936 fn6629 fn7928 fn6947 fn8612 fn6957 fn8786 fn6246 fn9367 fn6945 fn6946 fn10024 fn10022 fn6811 fn9361 fn6279 fn6278 fn8569 fn7641 fn8568 fn6943"
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


'''
    for the expected files case we analyze:
    './data/patient_drug_by_treatment_line_v2/patient-drug_line1.csv',
'''

drugLineFiles = [
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line1.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line2.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line3.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line4.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line5.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line6.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line7.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line8.csv',
    './data/Patient_Tox_by_Treatment_Line_v2/treatment_line10.csv'
]

for file in drugLineFiles:
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        patients = []
        toxicities = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                patients.append(row[0])
                toxicities.append(row[1])
                line_count += 1
        print(f'Processed {line_count} lines.')

    patients = Counter(patients).keys()
    toxicities = Counter(toxicities).keys()
    tox_patients = {}
    for t in toxicities:
        tox_patients[t] = {}
        for d in patients:
            tox_patients[t][d] = 0

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                tox_patients[row[1]][row[0]] = 1

    patientsAndToxs = {}
    peopleCountPerDrug = {}

    for keys in tox_patients:
        for keys2 in tox_patients:
            toxs_related = ('','')
            for x in tox_patients[keys]: # x being the patient
                if tox_patients[keys][x] > 0:
                    if tox_patients[keys2][x] > 0:
                        if keys != keys2: # not the diagonal
                            toxs_related = (keys,keys2)
                            if patientsAndToxs.get(x) == None:
                                patientsAndToxs[x] = []
                                patientsAndToxs[x].append(toxs_related)
                            else:
                                patientsAndToxs[x].append(toxs_related)
                            
                            peopleCountPerDrug[x] = 0

    #print(patientsAndToxs)

    mapToxToNum = {"GENERAL": 0,
                       "GASTROINTESTINAL": 1,
                       "ENDOCRINE": 2,
                       "CUTANEOUS": 3,
                       "PNEUMOLOGICAL": 4,
                       "ANALYTICAL": 5,
                       "NEUROLOGICAL": 6,
                       "OTHER": 7,
                       "CARDIOLOGICAL": 8}


    coocMatrix = np.zeros((9, 9))

    for keys in patientsAndToxs:
        for tup in patientsAndToxs[keys]:
            i = mapToxToNum[tup[0]]
            j = mapToxToNum[tup[1]]
            coocMatrix[i][j] += 1


    print(coocMatrix)
    sums = []
    for i, row in enumerate(coocMatrix):
        sums.append(0)
        for j, col in enumerate(coocMatrix[i]):
            sums[i] += coocMatrix[i][j]

    #print("*")
    print(sums)
    #print("*")
    
    nodes = ["GENERAL","GASTROINTESTINAL","ENDOCRINE","CUTANEOUS",
                "PNEUMOLOGICAL","ANALYTICAL","NEUROLOGICAL","OTHER","CARDIOLOGICAL"];
                
    strMatrix = ""
    strMatrix += "AA,GENERAL,GASTROINTESTINAL,ENDOCRINE,CUTANEOUS,PNEUMOLOGICAL,ANALYTICAL,NEUROLOGICAL,OTHER,CARDIOLOGICAL\n"
    for i, row in enumerate(coocMatrix):
        for j, col in enumerate(coocMatrix[i]):
            #if coocMatrix[i][j] > 0:
            #    print(i,j,coocMatrix[i][j])
            coocMatrix[i][j] = (coocMatrix[i][j] / len(patients)) * 100

        strMatrix += nodes[i] + ","
        strMatrix += ','.join(str(x) for x in coocMatrix[i])
        strMatrix +='\n'

    print(coocMatrix)
    #print(strMatrix)

    links = []
    for i, n in enumerate(nodes):
        for j, elem in enumerate(coocMatrix[i]):
            if coocMatrix[i][j] > 0:
                addLink = True;
                for link in links:
                    if link["source"] == j and link["target"] == i:
                        addLink = False;
                
            
                if addLink:
                    links.append({"source": i, "target": j, "weight": elem});

    #print("nodes",nodes)
    #print("links", links)

    data = []

    for i, n in enumerate(nodes):
        data.append(to_json_node(i, n, sums[i]))

    for i, l in enumerate(links):
        data.append(to_json_edge(l["source"], l["target"], l["weight"], i))

    json_data = json.dumps(data, indent=2, sort_keys=True)

    subStrFile = "treatment_line"
    subStrFileIndex = file.index(subStrFile);
    index = file[subStrFileIndex + len(subStrFile) : -4]

    dirname = "./jsons_all/json_line" + str(index)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    open(dirname + "/line" + str(index) + "_all_obs.json", "w", encoding="utf8").write(json_data)
