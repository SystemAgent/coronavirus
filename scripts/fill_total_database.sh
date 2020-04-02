#!/bin/bash
# My first script
countries=(Bulgaria Spain Italy Germany "United Kingdom" France 
           Ukraine Poland Romania Netherlands Belgium Greece 
           Portugal Sweeden Hungary Belarus Austria
           Serbia Switzerland Denmark Finland Slovakia
           Norway Irelainf Croatia Moldova Albania Lithuania 
           Slovenia Latvia Estonia "North Macedonia" 
           "Bosnia and Herzegovina" Czechia)

for country in "${countries[@]}"
do
    echo $country
    python manage.py country_spread "$country"
done

