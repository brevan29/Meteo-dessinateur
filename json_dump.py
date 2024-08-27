def remove(x:str, ch:str):
	car=[]
	for i in range(len(ch)-len(x)+1):
		if ch[i:i+len(x)]==x:
			car.append(i)
	for index in car:
		ch=ch[:index]+ch[index+len(x):]
	return ch	
##### Horoscope #####
def Horosocope_search(date):
	rdate=refait(date).lower()
	for i in range(len(rdate)):
		if rdate[i]==" ":
			rdate=rdate[:i]+"-"+rdate[i+1:]
		elif rdate[i]=="û":
			rdate=rdate[:i]+"u"+rdate[i+1:]
		elif rdate[i]=="é":
			rdate=rdate[:i]+"e"+rdate[i+1:]

	for i in range(len(date)):
		if date[i]=="-":
			date=date[:i]+'/'+date[i+1:]
	import urllib.request
	print("https://www.legorafi.fr/"+date+"/horoscope-du-"+rdate)
	req = urllib.request.Request(url = "https://www.legorafi.fr/"+date+"/horoscope-du-"+rdate, headers = {'User-Agent': 'Mozilla/5.0'})
	request_url = urllib.request.urlopen(req)
	print("données récupérées")
	request_url=request_url.readlines()

	horoscope={}
	print("traitement de données")
	for ligne in request_url:
		ligne=remove('</strong>', ligne.decode('utf-8').strip())
		ligne=remove('</p>', ligne)

		if "<p><strong>" in ligne or "<p> <strong>" in ligne: 
			if "<p><strong>" in ligne:
				ligne = remove('<p><strong>', ligne)
			else:
				ligne = remove('<p> <strong>', ligne)
			
			for i in range(len(ligne)-3):
				if ligne[i:i+3] == " : ":
					horoscope[ligne[:i]] = ligne[i+2:]
					break
	return horoscope

	print('fin du traitement - début de la recherche du temps')
##### Lever et Coucher de soleil #####
def ephem ():
	from ephem import Observer, Sun, localtime
	
	o = Observer ()
	o.lat = "48:0:0"
	o.long = "-4:6:0"
	
	s = Sun ()
	s.compute ()
	
	if o.next_rising (s) < o.next_setting (s):
		lever =localtime (o.next_rising (s)).strftime ('%H:%M')
		coucher = localtime (o.next_setting (s)).strftime ('%H:%M')
	else:
		coucher= localtime (o.next_setting (s)).strftime ('%H:%M')
		lever = localtime (o.next_rising (s)).strftime ('%H:%M')
	
	return (lever , coucher)

from ephem import *
from ephem import Moon
import datetime

def get_moon_phase(date=None):
    """
    This function returns the moon phase for a given date.
    If no date is provided, the current date is used.

    :param date: The date for which the moon phase is fetched.
    :type date: datetime.date, optional
    :return: The moon phase (0: New Moon, 0.5: First Quarter, 1.0: Full Moon)
    :rtype: float
    """
	
    if date == None:
        date = datetime.datetime.now()
    moon = Moon(date)
    phase = moon.moon_phase
    return phase

def jourSuivant(date=None):
	limite={"1":31, "2":28, "3":31, "4":30, "5":31, "6":30, "7":31, "8":31, "9":30, "10":31, "11":30, "12":31}
	if date==None:
		date=str(datetime.datetime.now())[:10]
	date=str(date)
	jour=int(date[8:])
	mois=int(date[5:7])
	année=int(date[:4])
	if int(jour)+1>limite[str(mois)] and mois!=12:
		return datetime.date(année, mois+1, 1)
	elif jour+1>limite[str(mois)] and mois==12:
		return datetime.date(année+1,1,1)
	else:
		return datetime.date(année, mois, jour+1)
	
def comparer(illu):
	illup1 = get_moon_phase(jourSuivant(jourSuivant()))
	return illu < illup1

def lune():
	illumination = get_moon_phase(jourSuivant())
	if illumination<0.1:
		return "Nouvelle lune"
	elif illumination<0.3:
		if comparer(illumination) :
			return("1er croissant")
		else:
			return("dernier croissant")
	elif illumination<0.6:
		if comparer(illumination):
			return("1er quartier")
		else:
			return("dernier quartier")
	elif illumination<0.9:
		if comparer(illumination):
			return("gribbeuse croissante")
		else:
			return("gibbeuse décroissante")
	else:
		return("pleine lune")

def refait(date):
	Mois = {'01':'Janvier', '02':"Février", "03":"Mars", '04':"Avril", "05":"Mai", "06":'Juin', '07':"Juillet", "08":"Août", "09":"Septembre", "10":"Octobre", "11":"Novembre", "12":"Décembre"}
	date=str(date)[:10]
	print(date, len(date))
	return date[8:]+' '+Mois[date[5:7]]+' '+date[:4]

def recup(date):
	Fetes = {"O1" : [["Jour de l'An", ""],["Basile", "Saint"],["Geneviève", "Sainte"],["Odilon", "Saint"],["Edouard", "Saint"],["Mélaine", "Saint"],["Raymond", "Saint"],["Lucien", "Saint"],["Alix", "Sainte"],["Guillaume", "Saint"],["Pauline", "Saint"],["Tatiana", "Sainte"],["Yvette", "Sainte"],["Nina", "Sainte"],["Rémi", "Saint"],["Marcel", "Saint"],["Roseline", "Sainte"],["Prisca", "Sainte"],["Brévan", "Saint"],["Fabien", "Saint"],["Agnès", "Sainte"],["Vincent", "Saint"],["Barnard", "Saint"],["François de Sales", "Saint"],["Conversion de Paul", ""],["Paule", "Sainte"],["Angèle", "Sainte"],["Thomas d'Aquin", "Saint"],["Gildas", "Saint"],["Martine", "Sainte"],["Marcelle", "Sainte"]],
	"02" : [["Ella", "Sainte"],["Fête de la Présention", ""],["Blaise", "Saint"],["Véronique", "Sainte"],["Agathe", "Sainte"],["Gaston", "Saint"],["Eugènie", "Sainte"],["Jacqueline", "Sainte"],["Apolline", "Sainte"],["Arnaud", "Saint"],["Notre Dame de Lourdes", "Sainte"],["Félix", "Saint"],["Béatrice", "Sainte"],["Valentin", "Saint"],["Claude", "Saint"],["Julienne", "Sainte"],["Alexis", "Saint"],["Bernadette", "Sainte"],["Gabin", "Saint"],["Aimée", "Sainte"],["Mercredi des Cendres", ""],["Isabelle", "Sainte"],["Lazare", "Saint"],["Modeste", "Sainte"],["Roméo", "Saint"],["Nestor", "Saint"],["Honorine", "Sainte"],["Romain", "Saint"],["Auguste", "Saint"]],
	"03" : [["Aubin", "Saint"],["Charles le Bon", "Saint"],["Guénolé", "Saint"],["Casimir", "Saint"],["Olive", "Saint"],["Colette", "Sainte"],["Félicité", "Sainte"],["Jean de Dieu", "Saint"],["Françoise", "Sainte"],["Vivien", "Saint"],["Rosine", "Sainte"],["Justine", "Sainte"],["Rodrigue", "Saint"],["Mathilde", "Sainte"],["Louise", "Sainte"],["Bénédicte", "Sainte"],["Patrice", "Saint"],["Cyrille", "Saint"],["Joseph", "Saint"],["Herbert", "Saint"],["Clémence", "Sainte"],["Léa", "Sainte"],["Victorien", "Saint"],["Karine", "Sainte"],["Anne", "Sainte"],["Larissa", "Sainte"],["Habib", "Saint"],["Gontran", "Saint"],["Gwladys", "Sainte"],["Amédée", "Saint"],["Benjamin", "Saint"]],
	"04" : [["Hugues", "Saint"],["Sandrine", "Sainte"],["Richard", "Saint"],["Isidore", "Saint"],["Irène", "Sainte"],["Marcellin", "Saint"],["Jean-Baptiste de la Salle", "Saint"],["Julie", "Sainte"],["Gautier", "Saint"],["Fulbert", "Saint"],["Stanislas", "Saint"],["Jules", "Saint"],["Ida", "Sainte"],["Maxime", "Saint"],["Paterne", "Saint"],["Benoît-Joseph", "Saint"],["Anicet", "Saint"],["Parfait", "Saint"],["Emma", "Sainte"],["Odette", "Sainte"],["Anselme", "Saint"],["Alexandre", "Saint"],["Georges", "Saint"],["Fidèle", "Saint"],["Marc", "Saint"],["Alida", "Sainte"],["Zita", "Sainte"],["Valérie", "Sainte"],["Catherine de Sienne", "Sainte"],["Robert", "Saint"]],
	"05" : [["Fête du travail", ""],["Boris", "Saint"],["Philippe", "Saint"],["Sylvain", "Saint"],["Judith", "Saint"],["Prudence", "Saint"],["Gisèle", "Sainte"],["Armistice de 1945", ""],["Pacôme", "Saint"],["Solange", "Sainte"],["Estelle", "Sainte"],["Achille", "Saint"],["Rolande", "Sainte"],["Matthias", "Saint"],["Denise", "Sainte"],["Honoré", "Saint"],["Pascal", "Saint"],["Eric", "Saint"],["Yves", "Saint"],["Bernardin", "Saint"],["Constantin", "Saint"],["Emile", "Saint"],["Didier", "Saint"],["Donatien", "Saint"],["Sophie", "Sainte"],["Bérenger", "Saint"],["Augustin", "Saint"],["Germain", "Saint"],["Aymar", "Saint"],["Ferdinand", "Saint"],["Ferdinand", "Saint"]],
	"06" : [["Justin", "Saint"],["Blandine", "Sainte"],["Kévin", "Saint"],["Clotilde", "Sainte"],["Igor", "Saint"],["Norbert", "Saint"],["Gilbert", "Saint"],["Médard", "Saint"],["Diane", "Sainte"],["Landry", "Saint"],["Barnabé", "Saint"],["Guy", "Saint"],["Antoine de Padoue", "Saint"],["Elisée", "Sainte"],["Germaine", "Sainte"],["Jean-François Régis", "Saint"],["Hervé", "Saint"],["Léonce", "Saint"],["Romuald", "Saint"],["Silvère", "Saint"],["Solstice d'été", ""],["Alban", "Saint"],["Audrey", "Sainte"],["Jean-Baptiste", "Saint"],["Prosper", "Saint"],["Anthelme", "Saint"],["Fernand", "Saint"],["Irénée", "Saint"],["Pierre", "Saint"],["Martial", "Saint"]],
	"07" : [["Thierry", "Saint"],["Martinien", "Saint"],["Thomas", "Saint"],["Florent", "Saint"],["Antoine", "Saint"],["Mariette", "Sainte"],["Raoul", "Saint"],["Thibault", "Saint"],["Amandine", "Sainte"],["Ulrich", "Saint"],["Benoît", "Saint"],["Olivier", "Saint"],["Henri", "Saint"],["Fête Nationale", ""],["Donald", ""],["Fête de Notre Dame du Mont Carmel", ""],["Charlotte", "Sainte"],["Frédéric", "Saint"],["Arsène", "Saint"],["Marina", "Sainte"],["Victor", "Saint"],["Marie-Madeleine", "Sainte"],["Brigitte", "Sainte"],["Christine", "Sainte"],["Jacques", "Saint"],["Anne", "Sainte"],["Nathalie", "Sainte"],["Samson", "Saint"],["Marthe", "Sainte"],["Juliette", "Sainte"],["Ignace de Loyola", "Saint"]],
	"08" : [["Alphonse", "Saint"],["Julien Eymard", "Saint"],["Lydie", "Sainte"],["Jean-Marie Vianney", "Saint"],["Abel", "Saint"],["Fête de la Transfiguration", ""],["Gaétan", "Saint"],["Dominique", "Saint"],["Amour", "Saint"],["Laurent", "Saint"],["Claire", "Sainte"],["Clarisse", "Sainte"],["Hippolyte", "Saint"],["Evrard", "Saint"],["Fête de l'Assomption", ""],["Armel", "Sainte"],["Hyacinthe", "Saint"],["Hélène", "Sainte"],["Jean-Eudes", "Saint"],["Bernard", "Saint"],["Christophe", "Saint"],["Fabrice", "Saint"],["Rose de Lima", "Sainte"],["Barthélémy", "Saint"],["Louis", "Saint"],["Natacha", "Sainte"],["Monique", "Sainte"],["Augustin", "Saint"],["Sabine", "Sainte"],["Fiacre", "Saint"],["Aristide", "Saint"]],
	"09" : [["Gilles", "Saint"],["Ingrid", "Sainte"],["Grégoire", "Saint"],["Rosalie", "Sainte"],["Raïssa", "Sainte"],["Bertrand", "Saint"],["Reine", "Sao,te"],["Fête de la Nativité", ""],["Alain", "Saint"],["Inès", "Sainte"],["Adelphe", "Saint"],["Apollinaire", "Saint"],["Aimé", "Saint"],["Fête de la Croix Glorieuse", ""],["Roland", "Saint"],["Edith", "Sainte"],["Renaud", "Saint"],["Nadège", "Sainte"],["Emilie", "Sainte"],["Davy", "Saint"],["Matthieu", "Saint"],["Maurice", "Saint"],["Equinoxe d'Automne", ""],["Thècle", "Sainte"],["Hermann", "Saint"],["Côme", "Saint"],["Vincent de Paul", "Saint"],["Venceslas", "Saint"],["Michel", "Saint"],["Jérôme", "Saint"]],
	"10" : [["Thérèse de l'Enfant Jésus", "Sainte"],["Léger", "Saint"],["Gérard", "Saint"],["François d'Assise", "Saint"],["Fleur", "Sainte"],["Bruno", "Saint"],["Serge", "Saint"],["Pélagie", "Sainte"],["Denis", "Saint"],["Ghislain", "Saint"],["Firmin", "Saint"],["Wilfried", "Saint"],["Géraud", "Saint"],["Juste", "Saint"],["Thérèse d'Avila", "Saint"],["Edwige", "Sainte"],["Baudoin", "Saint"],["Luc", "Saint"],["René", "Saint"],["Adeline", "Sainte"],["Céline", "Sainte"],["Elodie", "Sainte"],["Jean de Capistran", "Saint"],["Florentin", "Saint"],["Crépin", "Saint"],["Dimitri", "Saint"],["Emeline", "Sainte"],["Jude", "Saint"],["Narcisse", "Saint"],["Bienvenue", "Sainte"],["Quentin", "Saint"]],
	"11" : [["Toussaint", ""],["Fête des défunts", ""],["Hubert", "Saint"],["Charles", "Saint"],["Sylvie", "Sainte"],["Bertille", "Sainte"],["Carine", "Sainte"],["Geoffroy", "Saint"],["Théodore", "Saint"],["Léon", "Saint"],["Armistice de 1918", ""],["Christian", "Saint"],["Brice", "Saint"],["Sidoine", "Saint"],["Albert", "Saint"],["Marguerite", "Sainte"],["Elisabeth", "Sainte"],["Aude", "Sainte"],["Tanguy", "Saint"],["Edmond", "Saint"],["Présence de Marie", ""],["Cécile", "Sainte"],["Clément", "Saint"],["Flora", "Sainte"],["Catherine", "Sainte"],["Delphine", "Sainte"],["Sévrin", "Saint"],["Jacques de la Marche", "Saint"],["Saturnin", "Saint"],["André", "Saint"]],
	"12" : [["Florence", "Sainte"],["Viviane", "Sainte"],["François-Xavier", "Saint"],["Barbara", "Sainte"],["Gérald", "Saint"],["Nicolas", "Saint"],["Ambroise", "Sainte"],["Fête de l'Immaculée Conception", ""],["Pierre Fourier", "Saint"],["Romaric", "Saint"],["Daniel", "Saint"],["Jeanne-Françoise de Chantal", "Sainte"],["Lucie", "Sainte"],["Odile", "Sainte"],["Ninon", "Sainte"],["Alice", "Sainte"],["Gaël", "Saint"],["Gatien", "Saint"],["Urbain", "Saint"],["Théophile", "Saint"],["Solstice d'Hiver", ""],["Françoise-Xavière", "Sainte"],["Armand", "Saint"],["Adèle", "Sainte"],["Noël", ""],["Etienne", "Saint"],["Jean", "Saint"],["Innocents", "Saints"],["David", "Saint"],["Roger", "Saint"],["Sylvestre", "Saint"]]}
	return Fetes[str(date)[5:7]][int(str(date)[8:10])-1][0]

def verif(var):
	try:
		return int(var)
	except:
		print("qqch ne s'est pas passé comme prévu")
		return None
	
def JourEnLong(JourDeDépart):
	Jours=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche","Lundi", "Mardi"]
	dems=refait(jourSuivant())
	aprèdems=refait(jourSuivant(jourSuivant()))
	surdems=refait(jourSuivant(jourSuivant(jourSuivant())))
	i=Jours.index(JourDeDépart)
	return (JourDeDépart+' '+dems[:-5], Jours[i+1]+' '+aprèdems[:-5], Jours[i+2]+' '+surdems[:-5])
	

def mettreAJour(Récupéré):
	#Récupéré = [0 à 8 : Temps --- 9 à 17 : Température, 18 à 26 : Vent --- 27 : p1 - 28 : p2 - 29 J1] ------ Tout à été sous .get()
	import json
	with open('/Users/brevan/Documents/Brevan_Meteo/supplementaire.json','r') as f:
		data_hier = json.load(f)
	jours = JourEnLong(Récupéré[-1])
	soleil=ephem()
	if Récupéré[-3]:
		data={'jour':str(datetime.datetime.now())[8:10],
			'Horoscope':{
				"Aujourdhui":data_hier['Horoscope']['Demain'], 
				"Demain":Horosocope_search(data_hier['Horoscope']["date_dernier"]),
				"date_dernier":str(datetime.datetime.now())[:10]
				}, 
			'Ephemeride':{
				"Aujourdhui":{
					"Date":refait(datetime.datetime.now()),
					"Saint":recup(datetime.datetime.now()),
					"lever":data_hier["Ephemeride"]["Demain"]["lever"],
					"coucher":data_hier["Ephemeride"]["Demain"]["coucher"],
					"lune":data_hier["Ephemeride"]["Demain"]["lune"],
				}, 
				"Demain":{
					'Date':refait(jourSuivant()),
					"Saint":recup(jourSuivant()),
					'lever':soleil[0],
					'coucher':soleil[1],
					'lune':lune()
					}
				}
			}
	if not Récupéré[-3]:
		data={'jour':str(datetime.datetime.now())[8:10] ,
			'Horoscope':data_hier['Horoscope'], 
			'Ephemeride':{
				"Aujourdhui":{
					"Date":refait(datetime.datetime.now()),
					"Saint":recup(datetime.datetime.now()),
					"lever":data_hier["Ephemeride"]["Demain"]["lever"],
					"coucher":data_hier["Ephemeride"]["Demain"]["coucher"],
					"lune":data_hier["Ephemeride"]["Demain"]["lune"],
				}, 
				"Demain":{
					'Date':refait(jourSuivant()),
					"Saint":recup(jourSuivant()),
					'lever':soleil[0],
					'coucher':soleil[1],
					'lune':lune()
					}
				}
			}
	with open('/Users/brevan/Documents/Brevan_Meteo/supplementaire.json','w') as f:
		json.dump(data,f,indent=4, ensure_ascii=False)
	
	with open('/Users/brevan/Documents/Brevan_Meteo/météo.json','r') as f:
		data_hier = json.load(f)
	data={
		'aujourdhui':data_hier['demain'],
		'demain':{
			"jour" : jours[0],
			"matin":{
				"Temps":Récupéré[0][1:],
                "Température":int(Récupéré[9]),
                "Vent":verif(Récupéré[18])},
			"aprèsmidi" : {
				"Temps":Récupéré[1][1:],
                "Température":int(Récupéré[10]),
                "Vent":verif(Récupéré[19])},
			"soir" : {
				"Temps":Récupéré[2][1:],
                "Température":int(Récupéré[11]),
                "Vent":verif(Récupéré[20])},
		},
		'aprèdemain':{
			"jour" : jours[1],
			"matin":{
				"Temps":Récupéré[3][1:],
                "Température":int(Récupéré[12]),
                "Vent":verif(Récupéré[21])},
			"aprèsmidi" : {
				"Temps":Récupéré[4][1:],
                "Température":int(Récupéré[13]),
                "Vent":verif(Récupéré[22])},
			"soir" : {
				"Temps":Récupéré[5][1:],
                "Température":int(Récupéré[14]),
                "Vent":verif(Récupéré[23])},
		},
		'aprèsaprèsdemain':{
			"jour" : jours[2],
			"matin":{
				"Temps":Récupéré[6][1:],
                "Température":int(Récupéré[15]),
                "Vent":verif(Récupéré[24])},
			"aprèsmidi" : {
				"Temps":Récupéré[7][1:],
                "Température":int(Récupéré[16]),
                "Vent":verif(Récupéré[25])},
			"soir" : {
				"Temps":Récupéré[8][1:],
                "Température":int(Récupéré[17]),
                "Vent":verif(Récupéré[26])},
		}
	}
	with open('/Users/brevan/Documents/Brevan_Meteo/météo.json','w') as f:
		json.dump(data,f,indent=4, ensure_ascii=False)