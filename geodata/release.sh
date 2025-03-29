#!/bin/bash

set -e

# 设置时间格式和文件名
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
TODAY_DATE=$(date -u +"%Y-%m-%d")

export CURRENT_DATE=$CURRENT_DATE
export TODAY_DATE=$TODAY_DATE

# 运行 prepare_geoname_data.sh
echo "运行 prepare_geoname_data.sh..."
bash prepare_geoname_data.sh
if [[ $? -ne 0 ]]; then
    echo "运行 prepare_geoname_data.sh 失败！退出。"
    exit 1
fi

rm -rf output
rm -rf output_tmp
rm -rf geodata

LIST=("{admin_2}" "{admin_3}" "{admin_4}" "{admin_2} {admin_3}" "{admin_2} {admin_4}" "{admin_3} {admin_4}" "{admin_2} {admin_3} {admin_4}")
for item in "${LIST[@]}"; do
    striped_name="${item//\{/}"
    striped_name="${striped_name//\}/}"
    bash generate_data.sh --cn-pattern "$item" --output "output/geodata_${striped_name// /_}.zip"
    bash generate_data.sh --cn-pattern "$item" --output "output/geodata_${striped_name// /_}_full.zip" --full
done

cp output/geodata_admin_2.zip output/geodata.zip
cp output/geodata_admin_2_full.zip output/geodata_full.zip
