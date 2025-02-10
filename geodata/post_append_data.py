import os
import csv
import glob
from utils import logger

ADMIN2_LIST = None
# 可以改成 id 从而只增加特定城市的数据，id 可以从 admin2Codes.txt 里找到
# {
#     "CN.16.4514",
#     "CN.29.5328",
# }

admin2_dict = {}
admin2_codes_path = os.path.join("output", "admin2Codes.txt")
with open(admin2_codes_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # 按制表符分割
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        admin_id = parts[0]
        admin_name = parts[1]
        admin2_dict[admin_id] = admin_name


data_base_dir = "./geoname_data"
extra_data_folder = os.path.join(data_base_dir, "extra_data/")
output_file_path = os.path.join("output", "cities500.txt")

id_set = set()
loc_set = set()
with open(output_file_path, "r", encoding="utf-8") as outfile:
    for l in outfile:
        d = l.split("\t")
        id_set.add(d[0])
        loc_set.add((d[4], d[5]))


with open(output_file_path, "a", encoding="utf-8") as outfile:
    c = 0
    for csv_file in glob.glob(os.path.join(extra_data_folder, "*.txt")):
        with open(csv_file, "r", encoding="utf-8") as infile:
            for line in infile:
                row = line.split("\t")
                if row[0] in id_set:
                    continue
                if len(row) < 12:
                    continue

                country_code = row[8]
                admin1_code = row[10]
                admin2_code = row[11]

                if "" in [country_code, admin1_code, admin2_code]:
                    continue

                code = f"{country_code}.{admin1_code}.{admin2_code}"

                if ADMIN2_LIST is not None and code not in ADMIN2_LIST:
                    continue

                if (row[4], row[5]) not in loc_set:
                    if code not in admin2_dict:
                        continue
                    name = admin2_dict[code]

                    row[1] = name
                    row[2] = name
                    loc_set.add((row[4], row[5]))

                    c += 1
                    outfile.write("\t".join(row))
logger.info(f"共 {c} 条数据被追加")
