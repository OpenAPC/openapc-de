import os
from os.path import dirname
from sys import path

path.append(dirname(dirname(dirname((path[0])))))

import openapc_toolkit as oat

esac_ids = {
    "wiley": {
        "2020": "wiley2019deal",
        "2021": "wiley2019deal",
        "2022": "wiley2019deal",
        "2023": "wiley2019deal",
        "2024": "wiley2024deal",
        "2025": "wiley2024deal",
    },
    "springer": {
        "2020": "sn2020deal",
        "2021": "sn2020deal",
        "2022": "sn2020deal",
        "2023": "sn2020deal",
        "2024": "sn2024deal",
        "2025": "sn2024deal",
    },
    "elsevier": {
        "2023": "els2023deal",
        "2024": "els2023deal",
    }
}

dois = {}
path = "deas/dois/gold"

for file_name in os.listdir(path):
    file_path = os.path.join(path, file_name)
    publisher, year = os.path.splitext(file_name)[0].split("_")
    with open(file_path, "r") as handle:
        for doi in handle:
            doi = doi.strip().lower()
            esac_id = esac_ids[publisher][year]
            dois[doi] = esac_id

apc = []
ta = []
header, content = oat.get_csv_file_content("../../../../data/mpg/APC_MPG_2017-2025_preprocessed.csv")
apc.append(list(header[0]))
ta.append(list(header[0]) + ["agreement"])

for line in content:
    doi = line[3].lower()
    if doi not in dois:
        apc.append(line)
    else:
        line += [dois[doi]]
        ta.append(line)

quotemask = [False, False, False, False, False, False]

with open('out_apc.csv', 'w') as out:
    for article in apc:
        out.write(";".join(article) + "\n")
    
with open('out_ta.csv', 'w') as out:
    for article in ta:
        out.write(";".join(article) + "\n")
