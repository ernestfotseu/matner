import json
from pprint import pprint

from materials_entity_recognition import MatRecognition
from materials_entity_recognition import MatIdentification
from material_parser.material_parser import MaterialParser

__author__ = 'Tanjin He'
__maintainer__ = 'Tanjin He'
__email__ = 'tanjin_he@berkeley.edu'

if __name__ == "__main__":
	# load data
	with open('dataset/test_paras.json', 'r') as fr:
		paras = json.load(fr)

	mp = MaterialParser(pubchem_lookup=False, verbose=False)
        # find materials
	# model_new = MatIdentification()
	# for tmp_para in paras:
	#	all_materials = model_new.mat_identify(tmp_para)

	# find targets/precursors
	model_new = MatRecognition()
	for tmp_para in paras:
		all_materials, precursors, targets, other_materials = model_new.mat_recognize(tmp_para)
	# print('all_materials', all_materials)	     
	# Get material for list
	first = 0
	for material_string in all_materials:
	   material_propriety=mp.parse_material_string(material_string['text'])
	   text = material_string['text']
	   start = material_string['start']
	   end = material_string['end']	   
	   sentence = material_string['sentence']
	   # Parcourir le json
	   propieties = json.loads(json.dumps(material_propriety))
	   material_string = propieties["material_string"]
	   material_name = propieties["material_name"]
	   material_formula = propieties["material_formula"]
	   phase = propieties["phase"]
	   additives = propieties["additives"]
	   oxygen_deficiency = propieties["oxygen_deficiency"]
	   is_acronym = propieties["is_acronym"]
	   amounts_vars = propieties["amounts_vars"]
	   elements_vars = propieties["elements_vars"]
	   formula = propieties["composition"][0]["formula"]
	   amount = propieties["composition"][0]["amount"]
	   elements = propieties["composition"][0]["elements"]
	   species = propieties["composition"][0]["species"]

	   if first == 0:
	       all_materialsfield = text+"_/_"+str(start)+"_/_"+str(end)+"_/_"+material_string+"_/_"+material_name+"_/_"+material_formula+"_/_"+phase+"_/_"+str(additives)+"_/_"+str(oxygen_deficiency)+"_/_"+str(is_acronym)+"_/_"+str(amounts_vars)+"_/_"+str(elements_vars)+"_/_"+str(formula)+"_/_"+str(amount)+"_/_"+str(elements)+"_/_"+str(species)+"_/_"+str(sentence)
	       first = 1
	   else:
	       all_materialsfield = all_materialsfield+"#/#"+text+"_/_"+str(start)+"_/_"+str(end)+"_/_"+material_string+"_/_"+material_name+"_/_"+material_formula+"_/_"+phase+"_/_"+str(additives)+"_/_"+str(oxygen_deficiency)+"_/_"+str(is_acronym)+"_/_"+str(amounts_vars)+"_/_"+str(elements_vars)+"_/_"+str(formula)+"_/_"+str(amount)+"_/_"+str(elements)+"_/_"+str(species)+"_/_"+str(sentence)

        # all_material_propieties:
	print('_//_',all_materialsfield)

