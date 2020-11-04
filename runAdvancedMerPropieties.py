import json
import random
import time
import multiprocessing as mp
import os

from materials_entity_recognition import MatRecognition
from materials_entity_recognition import MatIdentification
from material_parser.material_parser import MaterialParser

__author__ = 'Tanjin He'
__maintainer__ = 'Tanjin He'
__email__ = 'tanjin_he@berkeley.edu'

def save_results(results):
	if not os.path.exists('results'):
		os.mkdir('results')
	file_name = 'results/results_' + str(hash(str(results))) + '.json'  
	with open(file_name, 'w') as fw:
		json.dump(results, fw, indent=2)
	return file_name

def pipeline_in_one_thread(paragraphs, batch_size=100):
	"""
	if batch_size > 0, then save results into files which containing batch_size of paragraphs each
	results output would be list of names of files
	if batch_size == 0, then save results in memory and output together at last rather than saving 
	results into files 
	"""

	# find targets/precursors
	results = []
	batch_results = []

	# =======================================================
	# add initialization part of the pipeline here
	model_new = MatRecognition()
	# # if enabling dependency parsing as feature
	# model_new = MatRecognition(parse_dependency=True)
	# =======================================================

	for tmp_para in paragraphs:
		# =====================================================================================
		# add pipeline executing functions here
		all_materials, precursors, targets, other_materials = model_new.mat_recognize(tmp_para)
		batch_results.append({
						'paragraph': tmp_para, 
						'all_materials': all_materials,
						'precursors': precursors,
						'target': targets,
						'other_materials': other_materials
						})
		# =====================================================================================
		
		if batch_size > 0 and len(batch_results) >= batch_size:
			results.append(save_results(batch_results)) 
			batch_results = []
	if batch_size > 0:
		if len(batch_results) > 0:
			results.append(save_results(batch_results))
	else:
		results = batch_results
	return results

if __name__ == "__main__":
	# =======================================================
	# parallel work config
	num_cores = 8
	batch_size = 2
	# =======================================================

	# load data
	with open('dataset/test_paras.json', 'r') as fr:
		paras = json.load(fr)

	# execute pipeline in a parallel way
	last_time_time = time.time()
	# running
	parallel_arguments = []
	len_per_para_list = int(len(paras)/num_cores)	
	for i in range(num_cores):
		if i < num_cores-1:
			parallel_arguments.append((paras[i*len_per_para_list: (i+1)*len_per_para_list], batch_size))
		else:
			parallel_arguments.append((paras[i*len_per_para_list: ], batch_size))		

	p = mp.Pool(processes = num_cores)
	results = p.starmap(pipeline_in_one_thread, parallel_arguments)
	p.close()
	p.join()

	mpr = MaterialParser(pubchem_lookup=False, verbose=False)
	# reading results
	print("\n #################")
	print('TIME USED :', time.time()-last_time_time)
	# combine all results
	all_results = sum(results, [])
	# print('len(all_results)', len(all_results))
	# print(all_results)
	with open(all_results[0], 'r') as json_data:
		data_dict = json.load(json_data)   
		# print("Data Dictionnary Generated:",data_dict)
		print("\n ################# Print Results ################# \n ")
		for materialinit in data_dict:
			paragraphline = materialinit['paragraph']
			all_materials = materialinit['all_materials']
			print("\n *******************************************************************")
			print("\n Paragraph : ",paragraphline)			      
			for material_string in all_materials:
			  material_propriety=mpr.parse_material_string(material_string['text'])        			
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
			  print("\n ----------------------------------------------------------------")
			  print("\n Text :",text)
			  print("\n Start :",start)
			  print("\n End :",end)
			  print("\n Sentence :",sentence)
			  print("\n Propieties : ",propieties)
