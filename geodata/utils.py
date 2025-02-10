import logging
import os
import csv

logger = logging.getLogger("logger")
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))  # 设置最低日志级别

console_handler = logging.StreamHandler()

# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# 添加处理器到 logger
logger.addHandler(console_handler)

GEODATA_HEADER = [
    "longitude",
    "latitude",
    "country",
    "admin_1",
    "admin_2",
    "admin_3",
    "admin_4",
]


def load_geo_data(file_path):
    result = {}
    if os.path.exists(file_path):
        # 读取 CSV 文件
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # 遍历每行数据
            for row in reader:
                # 获取 (lon, lat) 作为键
                key = (str(row["longitude"]), str(row["latitude"]))

                # 将其他字段作为值存入字典
                value = {
                    "country": row["country"],
                    "admin_1": row["admin_1"],
                    "admin_2": row["admin_2"],
                    "admin_3": row["admin_3"],
                    "admin_4": row["admin_4"],
                }

                result[key] = value

    return result


def ensure_folder_exists(file_path):
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)


def load_alternate_name(file_path):
    # 定义语言优先级列表，索引越小优先级越高
    priority = ["zh", "zh-Hans", "zh-SG", "zh-Hant", "zh-HK"]
    # mapping 存储：数字 -> (名称, 优先级, id, prefer)
    mapping = {}
    count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            count += 1
            if count % 1000000 == 0:
                logger.info(f"{count} 条 alternateName 数据已处理")
            parts = line.split("\t")
            if len(parts) < 5:
                continue  # 忽略格式不正确的行

            alt_id, number, lang, name, prefer = parts[:5]
            alt_id = int(alt_id)

            if lang not in priority:
                continue

            current_priority = priority.index(lang)
            # 如果该数字尚未记录，则直接保存
            if number not in mapping:
                mapping[number] = (name, current_priority, alt_id, prefer)
            else:
                stored_name, stored_priority, stored_id, stored_prefer = mapping[number]
                # 如果当前记录的语言优先级更高，则更新（无论 prefer 与否）
                if current_priority < stored_priority:
                    mapping[number] = (name, current_priority, alt_id, prefer)
                # 如果优先级相同，则需要做进一步判断
                elif current_priority == stored_priority:
                    # 如果已有记录已经是 prefer 的，则保持不变，不允许被覆盖
                    if stored_prefer == "1":
                        continue
                    else:
                        # 如果新记录的 prefer 为 "1"，说明它具有更高优先级，更新映射
                        if prefer == "1":
                            mapping[number] = (name, current_priority, alt_id, prefer)
                        # 否则在没有 prefer 的情况下，若 id 不同则更新（即认为是新的记录）
                        elif alt_id >= stored_id:
                            mapping[number] = (name, current_priority, alt_id, prefer)
                        # 否则（id 相同且都没有 prefer），保持原记录不变
    logger.info(f"共加载 {len(mapping)} 条中文 alternateName 数据")
    # 返回最终映射字典，仅保留数字到中文名的映射
    d = {key: value[0] for key, value in mapping.items()}

    with open("./dict.txt") as f:
        for l in f:
            if len(l) == 0:
                continue
            id, name = l.strip().split("\t")
            d[id] = name

    return d
