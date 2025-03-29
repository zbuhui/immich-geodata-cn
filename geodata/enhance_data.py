import os
from utils import logger, GEODATA_HEADER
import argparse
import shutil

parser = argparse.ArgumentParser()

parser.add_argument("--full", action="store_true", help="Enable full mode")
parser.add_argument(
    "--output", type=str, default="./geoname_data/cities500.txt.tmp", help="Output cities500 file"
)

# 解析参数
args = parser.parse_args()

MIN_POPULATION = 100

# 文件路径
data_base_dir = "./geoname_data"
cities_file = os.path.join(data_base_dir, "cities500.txt")
extra_data_folder = os.path.join(data_base_dir, "extra_data/")
output_file = args.output

need_finer_admin_2_list = [
    "CN.23.12324204",  # 上海
    "CN.22.11876380",  # 北京
    "CN.33.8739734",  # 重庆
    "CN.28.12324202",  # 天津
]


def need_finer_data(data):
    if args.full:
        return True
    country_code = data[8]
    admin1_code = data[10]
    admin2_code = data[11]

    code = f"{country_code}.{admin1_code}.{admin2_code}"
    if code not in need_finer_admin_2_list:
        return False
    return True


# 读取 cities500.txt 中的所有 id
with open(cities_file, "r") as f:
    existing_ids = set()
    existing_loc = set()
    for line in f:
        d = line.split("\t")
        existing_ids.add(d[0])
        existing_loc.add((d[4], d[5]))

shutil.copyfile(cities_file, output_file)

with open(output_file, "a") as append_f:
    # 遍历 extra_data 文件夹中的所有 txt 文件
    for file_name in os.listdir(extra_data_folder):
        if file_name.endswith(".txt"):
            logger.info(f"开始处理 {file_name}")
            file_path = os.path.join(extra_data_folder, file_name)

            with open(file_path, "r") as f:
                c = 0
                for line in f:
                    columns = line.split("\t")

                    # 第一个 id
                    id_value = columns[0]
                    loc = (columns[4], columns[5])

                    try:
                        num_value = float(columns[14])
                    except ValueError:
                        continue  # 如果无法转换为数字，跳过此行

                    # 判断是否满足追加条件
                    if (
                        id_value not in existing_ids
                        and (num_value >= MIN_POPULATION or need_finer_data(columns))
                        and loc not in existing_loc
                    ):
                        c += 1
                        append_f.write(line)
                        existing_ids.add(id_value)  # 添加到已存在的 id 集合中
                        existing_loc.add(loc)

                logger.info(f"共 {c} 条数据被追加")
