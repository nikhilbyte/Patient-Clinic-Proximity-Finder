import json
import os
import pandas as pd
import googlemaps
from datetime import datetime

#modify the API_Key and file paths in config.json

absPath = os.path.join("config.json")
with open(absPath) as file:
    config = json.load(file)


clinics = pd.read_csv(config["clinic_file_path"],index_col=0)
patients = pd.read_csv(config["patients_file_path"],index_col=0)
gmaps = googlemaps.Client(key=config["API_Key"])


#getting the address ready in the format required by the Google API

#clinics's address example: "8308 114 St Nw Suite 2020" + "Edmonton" + "AB"
clinics['Complete_Address'] = clinics['Clinic Address'] + "," + clinics['Clinic City'] + "," + clinics['Province']
clinics['Complete_Address_FSA'] = clinics['FSA'] + "," + clinics['Clinic City'] + "," + clinics['Province'] # approximate address


clinics['ID'] = clinics.index
clinics.index = clinics['Clinic Name']


#patients's address emaple : same as clinics
patients['Complete_Address'] = patients['Address'] + "," + patients['City'] + "," + patients['Province']
patients['Complete_Address_FSA'] = patients['FSA'] + "," + patients['City'] + "," + patients['Province'] #approximate address


# initializing two lists for absolute and approximate address(FSA+Province)
geocode_results_clinic_absolute = []
geocode_results_clinic_approx = []
lat=[]
lng = []

#geocoding all the addresses in both the csv files one by one
print("Geocoding started")
for add in clinics.Complete_Address.values:
  geocode_results_clinic_absolute.append(gmaps.geocode(add))

for add in clinics.Complete_Address_FSA.values:
  geocode_results_clinic_approx.append(gmaps.geocode(add))


for i in range(len(geocode_results_clinic_absolute)):
  try:
    lat.append(geocode_results_clinic_absolute[i][0]['geometry']['location']['lat'])
  except:
    lat.append(geocode_results_clinic_approx[i][0]['geometry']['location']['lat'])
  try:
    lng.append(geocode_results_clinic_absolute[i][0]['geometry']['location']['lng'])
  except:
    lng.append(geocode_results_clinic_approx[i][0]['geometry']['location']['lng'])

clinics['lat'] = lat
clinics['lng'] = lng


geocode_results_patients_absolute = []
geocode_results_patients_approx = []
lat_patients=[]
lng_patients = []

for add in patients.Complete_Address.values:
  geocode_results_patients_absolute.append(gmaps.geocode(add))

for add in patients.Complete_Address_FSA.values:
  geocode_results_patients_approx.append(gmaps.geocode(add))

for i in range(len(geocode_results_patients_absolute)):
  try:
    lat_patients.append(geocode_results_patients_absolute[i][0]['geometry']['location']['lat'])
  except:
    lat_patients.append(geocode_results_patients_approx[i][0]['geometry']['location']['lat'])
  try:
    lng_patients.append(geocode_results_patients_absolute[i][0]['geometry']['location']['lng'])
  except:
    lng_patients.append(geocode_results_patients_approx[i][0]['geometry']['location']['lng'])

patients['lat'] = lat_patients
patients['lng'] = lng_patients

print("Geocoding Finished")


print("Finding the closest clinic to all the patients")

distances = dict()
closest = []
closest_dist = []
for i1, row1 in patients.iterrows():
  LatOrigin = row1['lat'] 
  LongOrigin = row1['lng']
  origin = (LatOrigin,LongOrigin)
  for i2,row2 in clinics.iterrows():
    LatDest = row2['lat']
    LongDest = row2['lng'] 
    destination = (LatDest,LongDest)
    distances[row2["Clinic Name"]] = gmaps.distance_matrix(origin, destination, mode='walking')["rows"][0]["elements"][0]["distance"]["value"]
  closest.append(sorted(distances.items(), key=lambda x: x[1])[0][0])
  closest_dist.append(sorted(distances.items(), key=lambda x: x[1])[0][1])
closest_dist = [x / 1000 for x in closest_dist] # the result is returned in meters, therefore converting it into KMs

print("Distance Calculation Done")

clinics['geo_codes'] =  list(zip(clinics.lat, clinics.lng))

print("Generating the output File")

clinicid = []
for v in closest:  
  clinicid.append(clinics.loc[v]['ID'])

clinicgeocols = []
for v in closest:  
  clinicgeocols.append(clinics.loc[v]['Complete_Address'])

clinicgeocodes = []
for v in closest:  
  clinicgeocodes.append(clinics.loc[v]['geo_codes'])

clinicaddress = []
for v in closest:
  clinicaddress.append(clinics.loc[v]['Clinic Address'])

clinicpostalcode = []
for v in closest:
  clinicpostalcode.append(clinics.loc[v]['Postal Code'])

clinicfsa = []
for v in closest:  
  clinicfsa.append(clinics.loc[v]['FSA'])



initial = patients.columns


patients['Patient_ID'] = patients.index
patients['Pat_Geo_Cols'] = patients['Complete_Address']
patients['Pat_Geocode'] = list(zip(patients.lat, patients.lng))
patients['Pat_Address']=patients['Address']
patients['Pat_Postal_Code']=patients['Postal Code']
patients['Pat_FSA']=patients['FSA']
patients['Nearest_Clinic_ID']=clinicid
patients['Clinic_Geo_Cols']=clinicgeocols
patients['Clinic_Geocode']=clinicgeocodes
patients['Clinic_Address'] = clinicaddress
patients['Clinic_Postal Code'] = clinicpostalcode
patients['Clinic_FSA'] = clinicfsa
patients['Clinic_Distance'] = closest_dist

patients.drop(columns=initial,inplace = True)

patients.to_csv('Output.csv',index=False)

print("Done")


