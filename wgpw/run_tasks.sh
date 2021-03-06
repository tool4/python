#!/bin/bash
echo $(date +'%Y-%m-%d %H:%M') > ~/run_tasks.log
cd ~/wgpw/data

### mm/dd/yyyy ###
echo $(date +'%Y-%m-%d %H:%M')

output_dir=$(date +'%Y')
mkdir ${output_dir} -p
output_file=${output_dir}/wgpw_$(date +'%Y-%m-%d').txt
echo pwd
echo ${output_file}
python3 ~/git/python/wgpw/get_wgpw.py > ${output_file}

cp -f ${output_file} last_wgpw.txt
cat last_wgpw.txt | gawk -F, '{ print $1}' > wgpw_names.txt

cat last_wgpw.txt | grep -v Symbol > last_wgpw_pure.txt
python ~/git/python/wgpw/read_lines.py > ${output_dir}/wgpw_$(date +'%Y-%m-%d')_wybrane.txt
