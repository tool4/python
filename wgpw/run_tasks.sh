#!/bin/bash

cd ~/wgpw/data

### mm/dd/yyyy ###
date +'%Y-%m-%d'

output_dir=$(date +'%Y')
mkdir ${output_dir} -p
output_file=${output_dir}/wgpw_$(date +'%Y-%m-%d').txt
echo pwd
echo ${output_file}
python3 ~/git/python/wgpw/get_wgpw.py > ${output_file}

cp -f ${output_file} last_wgpw.txt
cat last_wgpw.txt | gawk -F, '{ print $1}' > wgpw_names.txt

