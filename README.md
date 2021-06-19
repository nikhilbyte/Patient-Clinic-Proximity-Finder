# Patient-Clinic-Proximity-Finder
Matches a patient to their nearest clinic using Google's Geocoding API.

## Formats and descriptions of the processed datasets:
patients data sample

| "ID" | "Address" | "Postal Code" | "FSA" | "City" | "Province" |
|  ----  | ----  | ----  | ----  | ----  | ----  | 
| 1 | 722 85 ST SW UNIT 215 | T3H 1S6 | T3H | CALGARY  | AB  | 


clinics data sample

| "Clinic ID" | "Clinic Address" | "Postal Code" | "FSA" | "Clinic City" | "Province" |
|  ----  | ----  | ----  | ----  | ----  | ----  | 
| 1 | 8308 114 St Nw Suite 2020 | T3H 1S6 | T3H | CALGARY  | AB  | 


## Settings
modify the config.json with the API key(See Document.txt).
## How to use
after modifying the data location and setting the API key, run ```python Proximity_Finder.py```. 

Dependencies:
- [numpy](https://github.com/numpy/numpy)
- [pandas](https://github.com/pandas-dev/pandas)
- [googlemaps](https://pypi.org/project/googlemaps/)


