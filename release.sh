#!/bin/bash

set -e

rm -rf output
mkdir -p output

cd geodata
bash release.sh
cd ..
mv geodata/geodata.zip output
mv geodata/geodata_full.zip output

zip -r output/i18n-iso-countries.zip i18n-iso-countries/langs