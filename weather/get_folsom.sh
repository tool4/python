#!/bin/bash


#wget "https://weather.cit.api.here.com/weather/1.0/report.json?product=observation&zipcode=95630&oneobservation=true&app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&metric=false" -O folsom.json -nv 2> /dev/null

# kamerka.blossom:
#app_id=2i2oc1wakxFhzlNTvn3v
#app_code=N3WPLlKU8J7sQR_-tdN1-A

wget "https://weather.cit.api.here.com/weather/1.0/report.json?product=observation&zipcode=95630&oneobservation=true&\
app_id=2i2oc1wakxFhzlNTvn3v&app_code=N3WPLlKU8J7sQR_-tdN1-A&metric=false" -O folsom_f.json -nv 

wget "https://weather.cit.api.here.com/weather/1.0/report.json?product=observation&zipcode=95630&oneobservation=true&\
app_id=2i2oc1wakxFhzlNTvn3v&app_code=N3WPLlKU8J7sQR_-tdN1-A&metric=true" -O folsom_c.json -nv 2> /dev/null
#$8 - high
#$5 - now
gawk -F, '{print $2 $5}' folsom_f.json | gawk -F\" '{ print $4 }' > folsom_desc.txt
gawk -F, '{print $2 $5}' folsom_f.json | gawk -F\" '{ print $8 }' > folsom_f.txt
gawk -F, '{print $2 $8}' folsom_f.json | gawk -F\" '{ print $8 }' > folsom_hf.txt
gawk -F, '{print $2 $5}' folsom_c.json | gawk -F\" '{ print $8 }' > folsom_c.txt
gawk -F, '{print $2 $8}' folsom_c.json | gawk -F\" '{ print $8 }' > folsom_hc.txt

date +'%Y-%m-%d'
output_dir=$(date +'%Y')
mkdir ${output_dir} -p

output_file=${output_dir}/folsom_f_$(date +'%Y-%m-%d').txt
echo $(date +'%H:%M:%S') ": " >> ${output_file}
cat folsom_f.txt >> ${output_file}
cat folsom_f.txt


output_file=${output_dir}/folsom_desc_$(date +'%Y-%m-%d').txt
echo $(date +'%H:%M:%S') ": " >> ${output_file}
cat folsom_desc.txt >> ${output_file}
cat folsom_desc.txt

output_file=${output_dir}/folsom_hf_$(date +'%Y-%m-%d').txt
echo $(date +'%H:%M:%S') ": " >> ${output_file}
cat folsom_hf.txt >> ${output_file}
cat folsom_hf.txt

output_file=${output_dir}/folsom_c_$(date +'%Y-%m-%d').txt
echo $(date +'%H:%M:%S') ": " >> ${output_file}
cat folsom_c.txt >> ${output_file}
cat folsom_c.txt

output_file=${output_dir}/folsom_hc_$(date +'%Y-%m-%d').txt
echo $(date +'%H:%M:%S') ": " >> ${output_file}
cat folsom_hc.txt >> ${output_file}
cat folsom_hc.txt



