import json
import datetime
#import plotly.offline as pyoff
import matplotlib.pyplot as plt
import glob
from collections import Counter
import numpy as np
import pandas as pd
from collections import defaultdict
from scipy.sparse import dok_matrix

from flask import Flask, request
from flask_restful import Resource, Api


class LocationInverse:
    def __init__(self):
        self.paths = {'readdic':'loc_dir.json',
                      'readcount':'loc_count.json',
                      'data':'/home/filipe/cmu/data/clean/',
                      'writedic':'loc_dir_new.json',
                      'writecount':'loc_count_new.json'}
        self.dir = defaultdict(list)
        self.count = Counter()
        self.min_locs_filter = 5
        self.resolution = 0.1
        self.lock = False

    def set_path(self, key, val):
        self.paths[key] = val

    def load_precomputed(self):
        with open(self.paths['readdic']) as f:
            self.dir = defaultdict(list, json.load(f))
        # with open(self.paths['readcount']) as f:
        #     self.count = Counter(json.load(f))
        
    def load_data(self):
        list_paths = glob.glob(self.paths['data']+'*.json')
        for geo_path in list_paths:
            self.load_datum(geo_path)

    def load_datum(self,geo_path):
        with open(geo_path) as f:
            var = json.load(f)
        filtered_var = [elem for elem in var if elem['loc'] != '']
        for elem in filtered_var:
            self.process_elem(elem)

    def process_elem(self,elem):
        ori_loc = elem['loc']
        if ori_loc != None:
            ori_loc = ori_loc.lower()
            ori_list = [elemi.strip() for elemi in ori_loc.split(',')]
            self.dir[ori_loc].append(elem['geo'])
            self.count[ori_loc] += 1
            if len(ori_list) > 1:
                for elemi in ori_list:
                    self.dir[elemi].append(elem['geo'])
                    self.count[elemi] += 1

    def query_elem(self,ori_loc):
        out = []
        if ori_loc != None:
            ori_loc = ori_loc.lower()
            ori_list = [elemi.strip() for elemi in ori_loc.split(',')]
            out += self.dir[ori_loc]
            if len(ori_list) > 1:
                for elemi in ori_list:
                    out += self.dir[elemi]
        return out
        #return {ori_loc:out}

    def dump_data(self):
        with open(self.paths['writedic'],'w') as f:
            json.dump(self.dir,f)
        # with open(self.paths['writecount'],'w') as f:
        #     json.dump(self.count,f)

    def prune_dic(self):
        for key in self.dir.keys():
            vax = [elem for elem in loc_dir[key] if elem != []]
            if len(vax) < 0 or key == '':
                del self.dir[key]

	def lock(self):
		self.lock = True

	def unlock(self):
		self.unlock = False

    def coordinate_map(self,key):
        vec = self.dir[key]
        coord = np.array([vec])
        orig_coordinates = (np.round(np.array(coord)/float(self.resolution)))
        len_coor = orig_coordinates.shape[0]
        val = 1.0/len_coor
        x = 360/self.resolution
        y = 180/self.resolution
        xoffset = int(180/self.resolution)
        yoffset = int(90/self.resolution)
        matr = dok_matrix((x,y))
        for elem in orig_coordinates:
            #matr[int(np.mod(elem[0],x)),int(np.mod(elem[1],y))]+=val
            matr[int(elem[1]+xoffset),int(elem[0]+yoffset)]+=val
        return matr

    def process_geo_loc(self,geo,loc):
        if loc != '' and geo != None:
            loc = loc.lower()
            ori_list = [elemi.strip() for elemi in loc.split(',')]
            self.dir[loc].append(geo)
            self.count[loc] += 1
            if len(ori_list) > 1:
                for elemi in ori_list:
                    self.dir[elemi].append(elem['geo'])
                    self.count[elemi] += 1

Locs = LocationInverse()
Locs.load_precomputed()

class QueryLoc(Resource):
    def get(self, location):
	    return {elem: Locs.query_elem(elem) for elem in location.split('&')}

class QueryPos(Resource):
	def get(self,location):
		return

class LivingQuery(Resource):
	def get(self,location):
		return

class Dump(Resource):
	def get(self,dumpQ):
		if dumpQ== 'True':
			write_path = 'data_dump/dir_loc' + str(datetime.datetime.now()) + '.json'
			Locs.set_path('writedic',write_path)
			Locs.dump_data()
		return


app = Flask(__name__)
api = Api(app)
#api.add_resource(QueryLoc,'/location=<string:location>')
api.add_resource(QueryLoc,'/location=<string:location>')
api.add_resource(QueryPos,'/location=<string:location>')
api.add_resource(LivingQuery,'/location=<string:location>')
api.add_resource(Dump,'/dump_dictionary=<string:dumpQ>')

if __name__ == '__main__':
    app.run()