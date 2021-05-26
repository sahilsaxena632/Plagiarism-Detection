import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
from flask import Flask, request, render_template
import re
import math

app = Flask("__name__")

q = ""

@app.route("/")
def loadPage():
	return render_template('PLAGIARISM.html', query="")

@app.route("/", methods=['POST'])
def cosineSimilarity():
	
	set_ofCollectedWords = []
	SimilarityPercentage = 0



##########   COLLECTING THE QUERY INPUT FROM THE USER   ##########
	
	inputquery = request.form['query']
	Q_lower = inputquery.lower()
	sw = stopwords.words('english')

	Q_WordList = re.sub("[^\w]", " ",Q_lower).split()                                               #using re module instead of nltk for tokenizing as well as removing punctuation marks#
	Q_WordList = {i for i in Q_WordList if not i in sw}                                             #removing stop words#
	for word in Q_WordList:
		if word not in set_ofCollectedWords:
			set_ofCollectedWords.append(word)
                


############  OPENING THE  DATABSE FILE   ##############


	cd = open("TotalFile.txt", "r")
	cd_lower = fd.read().lower()
	sw = stopwords.words('english')

	cd_WordList = re.sub("[^\w]", " ",cd_lower).split()                                                  #using re module instead of nltk for tokenizing as well as removing punctuation marks#
	cd_WordList = {w for w in cd_WordList if not w in sw}                                           #removing stop words#
	for word in cd_WordList:
		if word not in set_ofCollectedWords:
			set_ofCollectedWords.append(word)




#############  TF - IDF   AND    COSINE SIMILARITY    ############


	Q_TF = []
	cd_TF = []

	for word in set_ofCollectedWords:
		Q_TfCounter = 0
		cd_TfCounter = 0

		for word2 in Q_WordList:
			if word == word2:
				Q_TfCounter += 1
		Q_TF.append(Q_TfCounter)

		for word2 in cd_WordList:
			if word == word2:
				cd_TfCounter += 1
		cd_TF.append(cd_TfCounter)

	dot_Product = 0
	for i in range (len(Q_TF)):
		dot_.Product += Q_TF[i]*cd_TF[i]

	Q_VectorMagnitude = 0
	for i in range (len(Q_TF)):
		Q_VectorMagnitude += Q_TF[i]**2
	Q_VectorMagnitude = math.sqrt(Q_VectorMagnitude)

	cd_VectorMagnitude = 0
	for i in range (len(cd_TF)):
		cd_VectorMagnitude += cd_TF[i]**2
	cd_VectorMagnitude = math.sqrt(cd_VectorMagnitude)

	SimilarityPercentage = (float)(dot_Product / (Q_VectorMagnitude * cd_VectorMagnitude))*100

##########################   DISPLAY THE OUTPUT    ##########################

	output = "Query text that was submitted is similar %0.02f%% with database."%SimilarityPercentage

	return render_template('PLAGIARISM.html', query=inputquery, output=output)

app.run()
