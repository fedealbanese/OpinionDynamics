#coding:utf-8
import fileinput
from pycorenlp import StanfordCoreNLP
import numpy as np
import ast

#list of words
list_rig = ['market share','market','Bank','Banks','China','Free Trade Agreement','NAFTA','TPP','Trans-Pacific Partnership', 'bonds','businesses', "big business", 'charity','company','controlling inflation','corporation','corporations','corporations','corporation','currency','disadvantaged','earned','employees','employers','free market','freedom','full-time employees','highly taxed','imported products','increase the tax','individual freedom','industry','inflation','invest','job','jobs','legal currency','liberty','manipulate money','market','money','nationality','offshore bank accounts','offshore','increased','reduce','open market','paid','pay','personal fortunes','private companies','privately','privately managed accounts','profit','profits','property','property taxes','raise taxes','real estate','recession','required','rich','salaried employees','sales tax','same job','sellers','shareholders','stocks','successful corporations','tax','tax incentives','tax rate','taxes','taxpayers','the economy,economy','the rich','the same salary', 'salary', 'same salary','trans-national corporations','unemployment']
list_lef = ['Bank', 'Banks', 'Federal Reserve Bank', 'basic income', 'big government', 'class', 'corporations', 'economic globalisation', 'economic stimulus', 'employees', 'employers', 'environment', 'for the people', 'full-time employees', 'government', 'income', 'income program', 'services', 'increase the tax', 'industry', 'job', 'jobs', 'labor unions', 'medical care', 'minimum wage', 'more restrictions', 'obamacare', 'paid', 'pay', 'penalise businesses', 'pension payments', 'pension plans', 'profits', 'property taxes', 'protectionism', 'public funding', 'public spending', 'public','increased', 'reduce', 'raise', 'recession', 'reduce debt', 'regulation', 'require regulation', 'required', 'restrictions', 'salaried employees', 'sales tax', 'same job', 'serve humanity', 'social insurance', 'social plan', 'social security', 'subsidize', 'subsidize farmers', 'tax', 'tax business', 'tax rate', 'taxes', 'the economy', 'economy', 'the government', 'the national debt', 'national debt', 'the same salary', 'salary', 'same salary', 'unions', 'universal basic income', 'wage', 'workers',"government", "job", "standard of living", "intervention","labor union", "union", "unions","income", "family income", "salaries", "wages", "pensions", "dividends", "interest", "tax", "taxes", "small businesses"]
list_lib = ['allow', 'Planned Parenthood', 'abortion', 'adoption', 'adoption rights', 'anarchism', 'anti-discrimination', 'anti-discrimination laws', 'artist', 'assisted suicide', 'be allowed', 'black lives matter', 'child adoption', 'civil liberties', 'classroom attendance', 'contamination', 'cultures', 'democracy', 'democratic', 'democratic political system', 'different cultures', 'discriminate', 'discrimination', 'drugs', 'environment', 'free', 'free birth control', 'freedom', 'gay couples,gay', 'gender identity', 'health insurance,insurance', 'homosexual', 'homosexuality', 'immigrants', 'immigration', 'keep secretes', 'legal', 'legalization', 'legalize', 'liberty', 'marijuana', 'naturally homosexual', 'openness about sex', 'personal use', 'poet', 'pollution', 'pornography', 'possessing drugs', 'possessing marijuana', 'privacy', 'private', 'pro choice', 'rehabilitation', 'same sex', 'same sex couple', 'same sex marriage', 'same sex relationship', 'equal', 'secretes', 'societys support', 'transgender', 'transgender people',"abortion", "law", "The law", "permit abortion", "incest", "personal choice", "choice","help blacks", "blacks", "black", "minorities", "minority","Women", "equal roles"]
list_aut = ['combat roles', 'the U.S. Military', 'AntiFa', 'Confederate', 'Confederate flag', 'Confederate monuments,Confederate memorials', 'First-generation immigrants', 'God', 'Multinational companies', 'accept discipline', 'allowed to reproduce', 'army', 'authority', 'businessperson', 'capital punishment', 'catholicism', 'church', 'command', 'commanded', 'confederate', 'counter-terrorism', 'country', 'country of birth', 'crime', 'criminal', 'criminal justice', 'criminal offence', 'death penalty', 'death penalty,military', 'deny service', 'discipline', 'discriminate', 'discrimination', 'domestic terrorist organization', 'education', 'establishment', 'fully integrated', 'government control', 'homophobic', 'immigrant', 'immigration', 'judge', 'manufacturer', 'marital rape', 'maturity', 'military', 'military action', 'moral', 'nation', 'nationalism', 'nationality', 'non-marital rape', 'obey', 'obeyed', 'official surveillance', 'one-party state', 'population control', 'prison', 'prisoner', 'prisoners', 'pro life', 'punished', 'punishment', 'race', 'religion', 'religious', 'religious beliefs', 'religious values', 'soldier', 'superior race', 'surveillance', 'terrorism', 'terrorist', 'terrorist organization', 'war',"united states military", "military", "military action", "iraq", "terrorism", "terrorist","case of rape","religion", "religious"]

def pos2num_1(texto):
    if 'Negative' == texto:
        RV = -1
    elif 'Positive' == texto:
        RV = 1
    elif 'Neutral' == texto:
        RV = 0  
    elif 'Verynegative' == texto:
        RV = -2 
    elif 'Verypositive' == texto:
        RV = 2 
    return RV

def pos2num_2(texto):
    if 'Negative' == texto:
        RV = -0.5
    elif 'Positive' == texto:
        RV = 1.5 
    elif 'Neutral' == texto:
        RV = 0.5  
    elif 'Verynegative' == texto:
        RV = -1.5  
    elif 'Verypositive' == texto:
        RV = 2.5 
    return RV

#Sentiment 
nlp = StanfordCoreNLP('http://localhost:9000')

def annotate(text):
	return nlp.annotate(text, properties={
			'annotators': 'sentiment',
			'outputFormat': 'json'
		})



for line in fileinput.input(openhook=fileinput.hook_encoded("utf-8")):

	cant_men_Hillary=0
	cant_men_Trump=0
	cant_lef_complet=0
	cant_rig_complet=0
	cant_aut_complet=0
	cant_lib_complet=0
	
	if len(str(line))>10:
	
		try:	
			output = annotate(str(ast.literal_eval(line)[0]['text'])[2:-2])
			for sentence in output['sentences']:


				texto = ''
				for i in range(len(sentence['tokens'])):
				    		texto=texto+str(sentence['tokens'][i]['word'])+' '

				if "Hillary" in texto or "Clinton" in texto:
					cant_men_Hillary+=1

				if "Donald" in texto or "Trump" in texto:
					cant_men_Trump+=1

				if any(word in texto for word in list_rig):
					cant_rig_complet += pos2num_1(sentence['sentiment'])

				if any(word in texto for word in list_lef):
					cant_lef_complet += pos2num_1(sentence['sentiment'])

				if any(word in texto for word in list_aut):
					cant_aut_complet += pos2num_1(sentence['sentiment'])

				if any(word in texto for word in list_lib):
					cant_lib_complet += pos2num_1(sentence['sentiment'])
		

			#write the file
			result = [cant_men_Hillary, cant_men_Trump, cant_lef_complet, cant_rig_complet, cant_aut_complet, cant_lib_complet]

			if cant_men_Hillary > cant_men_Trump:
				file_output = 'Output_file_H.py'
			elif cant_men_Hillary < cant_men_Trump:
				file_output = 'Output_file_T.py'

			with open(file_output) as f:
			    lines = f.readlines()
			f.close()

			f = open(file_output, 'w')
			for i,line in enumerate(lines):
				line= line[0:-1]+str(resul_1[i])+", \n"
				f.write(line)

			f.close()

		except:
			pass 