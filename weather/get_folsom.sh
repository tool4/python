#!/bin/bash


#wget "https://weather.cit.api.here.com/weather/1.0/report.json?product=observation&zipcode=95630&oneobservation=true&app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&metric=false" -O folsom.json -nv 2> /dev/null

# kamerka.blossom:
#app_id=2i2oc1wakxFhzlNTvn3v
#app_code=N3WPLlKU8J7sQR_-tdN1-A

wget "https://weather.cit.api.here.com/weather/1.0/report.json?product=observation&zipcode=95630&oneobservation=true&\
app_id=2i2oc1wakxFhzlNTvn3v&app_code=N3WPLlKU8J7sQR_-tdN1-A&metric=false" -O folsom_f.json -nv 2> /dev/null

wget "https://weather.cit.api.here.com/weather/1.0/report.json?product=observation&zipcode=95630&oneobservation=true&\
app_id=2i2oc1wakxFhzlNTvn3v&app_code=N3WPLlKU8J7sQR_-tdN1-A&metric=true" -O folsom_c.json -nv 2> /dev/null
#$8 - high
#$5 - now
gawk -F, '{print $2 $5}' folsom.json   | gawk -F\" '{ print $4 }' > folsom_desc.txt
gawk -F, '{print $2 $5}' folsom_f.json | gawk -F\" '{ print $8 }' > folsom_f.txt
gawk -F, '{print $2 $8}' folsom_f.json | gawk -F\" '{ print $8 }' > folsom_hf.txt
gawk -F, '{print $2 $5}' folsom_c.json | gawk -F\" '{ print $8 }' > folsom_c.txt
gawk -F, '{print $2 $8}' folsom_c.json | gawk -F\" '{ print $8 }' > folsom_hc.txt


cat folsom_desc.txt
cat folsom_high.txt

