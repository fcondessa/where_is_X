import samt_utils
import glob
import json
import re
import pandas as pd
import numpy as np
import time
from pprint import pprint
from collections import defaultdict
from collections import Counter


__author__ = 'Filipe Condessa'

global nonus_countries, states, nominal_states, list_us_names

# states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
#           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
#           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
#           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
#           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
# nominal_states =['alabama', 'alaska', 'arizona', 'arkansas', 'california',   'colorado', 'connecticut', 'district of columbia', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']

list_us_names=['united states','usa','america','usofa']
state_codes = {'rhode island': 'us_RI', 'ga': 'us_GA', 'nevada': 'us_NV', 'maine': 'us_ME', 'tx': 'us_TX', 'la': 'us_LA', 'wyoming': 'us_WY', 'minnesota': 'us_MN', 'tn': 'us_TN', 'maryland': 'us_MD', 'texas': 'us_TX', 'iowa': 'us_IA', 'michigan': 'us_MI', 'de': 'us_DE', 'utah': 'us_UT', 'dc': 'us_DC', 'hawaii': 'us_HI', 'district of columbia': 'us_DC', 'nv': 'us_NV', 'ohio': 'us_OH', 'oklahoma': 'us_OK', 'delaware': 'us_DE', 'arkansas': 'us_AR', 'ri': 'us_RI', 'arizona': 'us_AZ', 'wisconsin': 'us_WI', 'wa': 'us_WA', 'wi': 'us_WI', 'wv': 'us_WV', 'california': 'us_CA', 'new mexico': 'us_NM', 'wy': 'us_WY', 'ok': 'us_OK', 'oh': 'us_OH', 'florida': 'us_FL', 'alaska': 'us_AK', 'or': 'us_OR', 'co': 'us_CO', 'colorado': 'us_CO', 'ca': 'us_CA', 'washington': 'us_WA', 'tennessee': 'us_TN', 'ct': 'us_CT', 'mississippi': 'us_MS', 'south dakota': 'us_SD', 'new jersey': 'us_NJ', 'north carolina': 'us_NC', 'pa': 'us_PA', 'indiana': 'us_IN', 'louisiana': 'us_LA', 'west virginia': 'us_WV', 'oregon': 'us_OR', 'connecticut': 'us_CT', 'hi': 'us_HI', 'me': 'us_ME', 'md': 'us_MD', 'georgia': 'us_GA', 'ma': 'us_MA', 'ut': 'us_UT', 'mo': 'us_MO', 'mn': 'us_MN', 'mi': 'us_MI', 'kentucky': 'us_KY', 'mt': 'us_MT', 'nebraska': 'us_NE', 'new hampshire': 'us_NH', 'ms': 'us_MS', 'south carolina': 'us_SC', 'va': 'us_VA', 'north dakota': 'us_ND', 'ak': 'us_AK', 'al': 'us_AL', 'ar': 'us_AR', 'vt': 'us_VT', 'il': 'us_IL', 'in': 'us_IN', 'ia': 'us_IA', 'az': 'us_AZ', 'id': 'us_ID', 'nh': 'us_NH', 'nj': 'us_NJ', 'nm': 'us_NM', 'nc': 'us_NC', 'nd': 'us_ND', 'ne': 'us_NE', 'illinois': 'us_IL', 'ny': 'us_NY', 'idaho': 'us_ID', 'kansas': 'us_KS', 'virginia': 'us_VA', 'montana': 'us_MT', 'massachusetts': 'us_MA', 'new york': 'us_NY', 'fl': 'us_FL', 'alabama': 'us_AL', 'vermont': 'us_VT', 'pennsylvania': 'us_PA', 'ks': 'us_KS', 'missouri': 'us_MO', 'sc': 'us_SC', 'ky': 'us_KY', 'sd': 'us_SD'}
country_codes = {"BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BA": "Bosnia and Herzegovina", "BB": "Barbados", "WF": "Wallis and Futuna", "BL": "Saint Barthelemy", "BM": "Bermuda", "BN": "Brunei", "BO": "Bolivia", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BT": "Bhutan", "JM": "Jamaica", "BV": "Bouvet Island", "BW": "Botswana", "WS": "Samoa", "BQ": "Bonaire, Saint Eustatius and Saba ", "BR": "Brazil", "BS": "Bahamas", "JE": "Jersey", "BY": "Belarus", "BZ": "Belize", "RU": "Russia", "RW": "Rwanda", "RS": "Serbia", "TL": "East Timor", "RE": "Reunion", "TM": "Turkmenistan", "TJ": "Tajikistan", "RO": "Romania", "TK": "Tokelau", "GW": "Guinea-Bissau", "GU": "Guam", "GT": "Guatemala", "GS": "South Georgia and the South Sandwich Islands", "GR": "Greece", "GQ": "Equatorial Guinea", "GP": "Guadeloupe", "JP": "Japan", "GY": "Guyana", "GG": "Guernsey", "GF": "French Guiana", "GE": "Georgia", "GD": "Grenada", "GB": "United Kingdom", "GA": "Gabon", "SV": "El Salvador", "GN": "Guinea", "GM": "Gambia", "GL": "Greenland", "GI": "Gibraltar", "GH": "Ghana", "OM": "Oman", "TN": "Tunisia", "JO": "Jordan", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "HK": "Hong Kong", "HN": "Honduras", "HM": "Heard Island and McDonald Islands", "VE": "Venezuela", "PR": "Puerto Rico", "PS": "Palestinian Territory", "PW": "Palau", "PT": "Portugal", "SJ": "Svalbard and Jan Mayen", "PY": "Paraguay", "IQ": "Iraq", "PA": "Panama", "PF": "French Polynesia", "PG": "Papua New Guinea", "PE": "Peru", "PK": "Pakistan", "PH": "Philippines", "PN": "Pitcairn", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "ZM": "Zambia", "EH": "Western Sahara", "EE": "Estonia", "EG": "Egypt", "ZA": "South Africa", "EC": "Ecuador", "IT": "Italy", "VN": "Vietnam", "SB": "Solomon Islands", "ET": "Ethiopia", "SO": "Somalia", "ZW": "Zimbabwe", "SA": "Saudi Arabia", "ES": "Spain", "ER": "Eritrea", "ME": "Montenegro", "MD": "Moldova", "MG": "Madagascar", "MF": "Saint Martin", "MA": "Morocco", "MC": "Monaco", "UZ": "Uzbekistan", "MM": "Myanmar", "ML": "Mali", "MO": "Macao", "MN": "Mongolia", "MH": "Marshall Islands", "MK": "Macedonia", "MU": "Mauritius", "MT": "Malta", "MW": "Malawi", "MV": "Maldives", "MQ": "Martinique", "MP": "Northern Mariana Islands", "MS": "Montserrat", "MR": "Mauritania", "IM": "Isle of Man", "UG": "Uganda", "TZ": "Tanzania", "MY": "Malaysia", "MX": "Mexico", "IL": "Israel", "FR": "France", "IO": "British Indian Ocean Territory", "SH": "Saint Helena", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands", "FM": "Micronesia", "FO": "Faroe Islands", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NA": "Namibia", "VU": "Vanuatu", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NZ": "New Zealand", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "CK": "Cook Islands", "XK": "Kosovo", "CI": "Ivory Coast", "CH": "Switzerland", "CO": "Colombia", "CN": "China", "CM": "Cameroon", "CL": "Chile", "CC": "Cocos Islands", "CA": "Canada", "CG": "Republic of the Congo", "CF": "Central African Republic", "CD": "Democratic Republic of the Congo", "CZ": "Czech Republic", "CY": "Cyprus", "CX": "Christmas Island", "CR": "Costa Rica", "CW": "Curacao", "CV": "Cape Verde", "CU": "Cuba", "SZ": "Swaziland", "SY": "Syria", "SX": "Sint Maarten", "KG": "Kyrgyzstan", "KE": "Kenya", "SS": "South Sudan", "SR": "Suriname", "KI": "Kiribati", "KH": "Cambodia", "KN": "Saint Kitts and Nevis", "KM": "Comoros", "ST": "Sao Tome and Principe", "SK": "Slovakia", "KR": "South Korea", "SI": "Slovenia", "KP": "North Korea", "KW": "Kuwait", "SN": "Senegal", "SM": "San Marino", "SL": "Sierra Leone", "SC": "Seychelles", "KZ": "Kazakhstan", "KY": "Cayman Islands", "SG": "Singapore", "SE": "Sweden", "SD": "Sudan", "DO": "Dominican Republic", "DM": "Dominica", "DJ": "Djibouti", "DK": "Denmark", "VG": "British Virgin Islands", "DE": "Germany", "YE": "Yemen", "DZ": "Algeria", "US": "United States", "UY": "Uruguay", "YT": "Mayotte", "UM": "United States Minor Outlying Islands", "LB": "Lebanon", "LC": "Saint Lucia", "LA": "Laos", "TV": "Tuvalu", "TW": "Taiwan", "TT": "Trinidad and Tobago", "TR": "Turkey", "LK": "Sri Lanka", "LI": "Liechtenstein", "LV": "Latvia", "TO": "Tonga", "LT": "Lithuania", "LU": "Luxembourg", "LR": "Liberia", "LS": "Lesotho", "TH": "Thailand", "TF": "French Southern Territories", "TG": "Togo", "TD": "Chad", "TC": "Turks and Caicos Islands", "LY": "Libya", "VA": "Vatican", "VC": "Saint Vincent and the Grenadines", "AE": "United Arab Emirates", "AD": "Andorra", "AG": "Antigua and Barbuda", "AF": "Afghanistan", "AI": "Anguilla", "VI": "U.S. Virgin Islands", "IS": "Iceland", "IR": "Iran", "AM": "Armenia", "AL": "Albania", "AO": "Angola", "AQ": "Antarctica", "AS": "American Samoa", "AR": "Argentina", "AU": "Australia", "AT": "Austria", "AW": "Aruba", "IN": "India", "AX": "Aland Islands", "AZ": "Azerbaijan", "IE": "Ireland", "ID": "Indonesia", "UA": "Ukraine", "QA": "Qatar", "MZ": "Mozambique"}

with open('/home/filipe/code/samt/data/d_countries.json','r') as f:
    rev_dict_countries = defaultdict(Counter,json.load(f))
    for key in rev_dict_countries.keys():
        rev_dict_countries[key] = Counter(rev_dict_countries[key])

        
with open('/home/filipe/code/samt/data/d_states.json','r') as f:
    rev_dict_states = defaultdict(Counter,json.load(f))
    for key in rev_dict_states.keys():
        rev_dict_states[key] = Counter(rev_dict_states[key])

rev_country_codes = {v.lower():k.lower() for k,v in country_codes.items()}
rev_country_codes = defaultdict(str,rev_country_codes)
state_codes = defaultdict(str,state_codes)


def get_locations_data_blocks(core_data_path,out_location_path):
    ''' obtaing all the locations from the data '''
    locations = []
    for data_path in glob.glob(core_data_path):
        data = samt_utils.load_block(data_path)

        try:
            aux_loc = list(set(data['loc']))
            locations += aux_loc
            pprint(data_path)
        except KeyError:
            pprint('KeyError '+data_path)

    locations = list(locations)
    locations = [elem for elem in locations if (elem != None) and (elem != 'None')]
    with open(out_location_path,'w') as f:
        json.dump(list(locations),f)
    return 1

def load_locations(path='locations.json'):
    with open(path,'r') as f:
        return json.load(f)

def state(text):
    list_text = re.split('\W+',text)
    return [state_codes[elem.lower()] for elem in list_text if state_codes[elem.lower()] != '']

def country(text):
    is_us = any([elem in text.lower() for elem in list_us_names])
    # list_countries = [ elem for elem in nonus_countries if elem in text.lower()]
    list_countries = [ rev_country_codes[key] for key in rev_country_codes.keys() if key in text.lower()]
    is_nonus = len(list_countries)>0
    return (is_us,is_nonus,list_countries)

def process_location(text,rev_dict_countries,rev_dict_states,num_return=3):
    min_len = 0
    if is_ascii(text):
        (is_us,is_nonus,list_countries) = country(text)
        list_text = re.split('\W+',text)
        if is_nonus:
            country_1 = list_countries
            state_1 = []
        elif is_us:
            country_1 = ['us']
            state_1 = state(text)
        else:
            country_1  = []
            state_1 = state(text)
        
        country_2 = [rev_dict_countries[elem.lower()].most_common(num_return) for elem in list_text if len(rev_dict_countries[elem.lower()])>0 and len(elem)>=min_len]
        state_2 = [rev_dict_states[elem.lower()].most_common(num_return) for elem in list_text if  len(rev_dict_states[elem.lower()])>0  and len(elem)>=min_len]
        return (country_1,country_2,state_1,state_2)
    else:
        return([],[],[],[])

def filter_location(text,country='us'):
    (c1,c2,s1,s2) = process_location(text,rev_dict_countries,rev_dict_states,num_return=3)
    is_target_country = is_country(country,c1,c2)


def decouple(input_list):
    out = Counter()
    for elem in input_list:
        
        for elem1 in elem:
            out[elem1[0]] += elem1[1]
    return (out,out.keys())

def purge_state_country(s1,s2,country_code):
    s1out = [elem for elem in s1 if elem[:2] == country_code]
    s2out = []
    for elem in s2:
        auxa = [elemi for elemi in elem if elemi[0][:2] == country_code]
        if len(auxa)>0:
            s2out.append(auxa)
    return (s1out,s2out)
        

def get_state(s1,s2,country_code):

    # extend this to take in account the country and select the states from the country
    (s1,s2) = purge_state_country(s1,s2,country_code)
    # done!
    (s2c,s2l) = decouple(s2)
    common_ct = 5
    TH = 1.5
    s2set = set([elem[0] for elem in s2c.most_common(common_ct)])
    intersection = list(s2set.intersection(set(s1)))
    if len(intersection) == 1:
        return intersection[0]
    if len(intersection) > 1:
        # if more than one state possible, return the most probable
        for elem in s2l:
            if elem in intersection:
                return elem
        return ''
    if len(s1) == 1:
        # there is one single state indication in s1 and no intersection with s2
        return s1[0]
    else:
        # nothing on s1 ,
        if len(s2l) == 1:
            return s2l[0]
        if len(s2l)>1:
            rax = [1.0*elem[1] for elem in s2c.most_common(2)]
            if rax[0]/rax[1]>= TH:
                return s2l[0]
            else:
                return ''

def is_country(country_code,country1,country2):
    if len(country1) == 1 and country1[0] == country_code:
        return True
    if len(country1) == 1 and country1[0] != country_code:
        return False
    (c2_counter,c2_list) = decouple(country2)
    if country_code in country1:
        if country_code in c2_list:
             return True
        if len(set(country1).intersection(set(c2_list)))==0:
            # the logic behind this step is that if there is no overlap between the lists of countries c1 and c2, then if no other is there, it's ok
             return True
    elif country_code in c2_list:
        if c2_counter.most_common(1)[0][0] != country_code:
            return False
        if len(set(country1).intersection(set(c2_list)))==0:
            # accounts for empty c1 and c2 with multiple stuff
            # accounts for nonoverlapping countries
             return True
    return False    

def finder(text,country_tag='us',rev_dict_countries=rev_dict_countries,rev_dict_states=rev_dict_states):
     (c1,c2,s1,s2) = process_location(text,rev_dict_countries,rev_dict_states)
     is_tag = is_country(country_tag,c1,c2)
     if is_tag:
         state = get_state(s1,s2,country_tag)
         return (1,state)
     else:
         return (0,'')

    

# def state_location(text):
#     state = is_state(text)
#     us = is_us(text)
#     if us and len(state)==0:
#         state = is_state(text.upper())
#     if len(state)>0 and not us:
#         us = 1
#     return (us,state)


# def run_data(data):
#     for datum in data:
#         (us,state) = state_location(datum)
#         if us:
#             pprint([us,state,datum])

def learn_locations(data):
    state_dict_val = defaultdict(Counter)
    iter_counter = 0
    for datum in data:
        iter_counter +=1
        (us,state_list) = state_location(datum)
        if len(state_list)>0:
            lower_list_text = [elem.lower() for elem in re.split('\W+',datum)]
            for elem in lower_list_text:
                for state in state_list:
                    state_dict_val[elem][state] += 1
    return state_dict_val

def relative_frequence_dict(state_dict):
    norm_fact = 1E-3
    for key in state_dict:
        norm_val = sum(state_dict[key].values())
        if norm_val >0:
            for val_key in state_dict[key].keys():
                state_dict[key][val_key] = state_dict[key][val_key] / (1.0*(norm_val))
    return state_dict
        

def save_dict(dict_val,dict_loc='dict_words.json'):
    with open(dict_loc,'w') as f:
        json.dump(dict_val,f)

def load_dict(dict_loc='dict_words.json'):
    with open(dict_loc,'r') as f:
        return json.load(f)
                
# def apply_dict(dict_val,location_text, min_size = 5):
#     # probable_location = Counter()
#     probable_location = []
#     lower_list_text = [elem.lower() for elem in re.split('\W+',location_text)]
#     lower_list_text = [elem for elem in lower_list_text if len(elem)>= min_size]
#     for elem in lower_list_text:
#         probable_location.append( dict_val[elem])
#     return probable_location

# THIS IS ALREADY IN samt_utils
def is_ascii(text):
    return all([ord(x)<128 for x in text])


# def probable_state(rel_dict_val,location_text):
#     # this needs to account for different weight of words
#     # more words -> more weight on clearly distinguishable
#     (us,state_list) = state_location(location_text)
#     probable_locations = apply_dict(rel_dict_val,location_text)
#     TH = 0.5
#     out_vals = []
#     if is_ascii(location_text):
#         for elem in probable_locations:
#             # print  elem
#             #print aux
#             if len(elem)>0:
#                 aux = elem.most_common(1)[0]
#                 # print aux[0]
#                 if aux[1]>TH:
#                     out_vals.append(aux)
#     # out_vals = [elem.most_common(1) for elem in probable_locations if elem.most_common(1)[1]> TH ]
#     return (location_text,us, state_list,out_vals)
        
    
# def build_lookup_table(data):
#     county = data['county']
#     state = data['state']
#     city = data['city']
#     county_dict_val = defaultdict(Counter)
#     city_dict_val = defaultdict(Counter)
#     all_dict_val = defaultdict(Counter)    
#     for elem in range(len(city)):
#         try:
#             county_dict_val[county[elem].lower()][state[elem]] +=1
#             city_dict_val[city[elem].lower()][state[elem]] +=1
#             for city_part in city[elem].split():
#                 all_dict_val[city_part.lower()][state[elem]] +=1
#             for county_part in county[elem].split():
#                 all_dict_val[county_part.lower()][state[elem]] +=1
#         except:
#             pass
#     return (all_dict_val,county_dict_val,city_dict_val)

# def build_part2(data_path='data/zip_codes_states.csv'):
#     data = pd.DataFrame(pd.read_csv(data_path))
#     county = data['county']
#     state = data['state']
#     city = data['city']
#     out_list = []
#     for elem in range(len(city)):
#         try:
#             out_list.append((county[elem].lower(),state[elem],'united states'))
#             out_list.append((city[elem].lower(),state[elem],'united states'))
#         except:
#             pass
#     return out_list

# def load_countries_data(path):
#     with open(path) as f:
#         return json.load(f)

# def non_american_countries(path='data/countriesToCities.json'):
#     data = load_countries_data(path)
#     countries = data.keys()
#     out_data = []
#     for country in data.keys():
#         for city in data[country]:
#             out_data.append((city.lower(),'',country.lower()))
#     return out_data

# def list_foreign_countries(path='data/countriesToCities.json'):
#     data = load_countries_data(path)
#     countries = data.keys()
#     countries = [elem.lower() for elem in countries if len(elem)>1]
#     countries.pop(countries.index('united states'))
#     return countries

# def countries_states_cities(path1='data/countriesToCities.json',path2='data/zip_codes_states.csv'):
#     part1 = non_american_countries(path1)
#     part2 = build_part2(path2)
#     return list(set(part1+part2))

def countries_states_cities2(path1='data/worldcitiespop.txt'):
    with open(path1) as f:
        data=f.readlines()
    out_data = []
    
    for iter_i in range(1,len(data)):
            [country,city, accentcity, region, population, latitude, longitude] = data[iter_i][:-1].split(',')
            out_data.append((city,country+'_'+region,country,population))
    return out_data

def build_rev_dict(data):
    dict_states = defaultdict(Counter)
    dict_countries = defaultdict(Counter)
    for datum in data:
        (city,state,country,population) = datum
        if len(population) == 0:
            # this should be thought after
            population = 1
        else:
            population = int(population)
        for elem in city.split():
            dict_states[elem.lower()][state] += population
            dict_countries[elem.lower()][country] += population
    return (dict_states,dict_countries)

def build_rev_dict_req_pop(data):
    dict_states = defaultdict(Counter)
    dict_countries = defaultdict(Counter)
    for datum in data:
        (city,state,country,population) = datum
        if len(population) > 0:
            # this should be thought after
            population = int(population)
            for elem in city.split():
                dict_states[elem.lower()][state] += population
                dict_countries[elem.lower()][country] += population
    return (dict_states,dict_countries)

# (rev_dict_states,rev_dict_countries) = build_rev_dict(countries_states_cities2()) # 


    
locs =  load_locations(path='locations.json')
# for locum in locs:
#     pprint((locum,process_location(locum,rev_dict_countries,rev_dict_states)))


# data = pd.DataFrame(pd.read_csv('data/zip_codes_states.csv'))
# (all_dict_val,city_dict_val,county_dict_val) =build_lookup_table(data)


# learnt_dict = load_dict()
# learnt_dict = learn_locations(locs)
# rel_all_dict = relative_frequence_dict(all_dict_val)
# rel_learnt_dict = relative_frequence_dict(learnt_dict)
# locs =  load_locations(path='locations.json')

# for locum in locs:
#     ax = probable_state(rel_all_dict,locum)
#     bx = probable_state(rel_learnt_dict,locum)
#     pprint((locum,ax,bx))
#     time.sleep(0.05)

# if __name__ ==  "__main__":
#     core_data_path = 'data/data_blocks/*.json'
#     out_location_path = 'locations_all.json'
#     result = get_locations_data_blocks(core_data_path,out_location_path)



# with open('data/list_places.json','w') as f:
#     auxa = {}
#     iter_i = 0
#     iter_j = 0
#     for elem in locs:
#         (res,us_state) = finder(elem)
#         iter_i += 1
#         if res:
#             auxa[elem] = us_state
#             iter_j += 1
#             print (iter_i,iter_j)
#     json.dump(auxa,f)
