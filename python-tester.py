import eel
import sys
import os
import csv
import time
import inspect

# Funktionen
@eel.expose
def tabelleSpeichern(skriptname, funktionsname, parameter, testfallDaten):

	with open('test-tabellen/' + skriptname + "-" + funktionsname, 'w') as f:

		write = csv.writer(f)
		write.writerow([funktionsname])
		param = [param.replace('"""', '"') for param in parameter]
		for testfall in testfallDaten:
			testfall = [paramWert.replace('"""', '"') for paramWert in testfall]
		write.writerow(parameter)
		write.writerows(testfallDaten)

@eel.expose
def tabelleEinlesen(skript, funktion):
	''' liest Tabellendaten aus der Datei tabellen aus
	'''
	zeilen = []
	try:
		with open('test-tabellen/' + skript + "-" + funktion, 'r') as f:
			for zeile in f.readlines():
				zeile = zeile.replace('"""', '"').replace('""', '"')
				zeile = zeile.replace('"[', '[').replace(']"', ']')
				if len(zeile.strip()) > 0:
					zeilen.append(zeile.replace('\n', ''))
	except:
		eel.prompt_alerts("Zur Funktion {} aus dem Programm {} gibt es noch keine Test-Tabelle".format(funktion, skript))
		return

	# Liste aus der Datei in Python-Liste umwandeln
	eintraege = []
	# Keine angefangene Liste -> listeStart = -1
	listeStart = -1
	for i in range(1, len(zeilen)):
		# Kommas innerhalb von Listen führen nicht zur Trennung
		kommaSepariert = zeilen[i].split(",") 
		eintrag = []
		for j in range(len(kommaSepariert)):
			if "[" in kommaSepariert[j] and "]" in kommaSepariert[j]:
				# ein-elementige Liste
				eintrag.append(kommaSepariert[j])
			elif "[" in kommaSepariert[j]:
				# Start einer Liste
				listeStart = j 
			elif "]" in kommaSepariert[j]:
				# Ende einer Liste
				if listeStart < j:
					listeEintrag = kommaSepariert[listeStart]
					for k in range(listeStart + 1, j+1):
						listeEintrag += ", "
						listeEintrag += kommaSepariert[k]
					eintrag.append(listeEintrag)
					listeStart = -1
			elif listeStart == -1:
				# regulärer Eintrag
				eintrag.append(kommaSepariert[j])
		eintraege.append(eintrag)
	
	eel.tabelleUpdaten(eintraege)


def fehlendeParameterBestimmen(zuordnungParameter, parameterNamen):
	''' bestimmt welche Parameter der Funktion vom Nutzer
	in der Tabelle nicht angegeben wurden
	'''
	fehlendeParameter = []
	for i in range(len(parameterNamen)):
		if i not in zuordnungParameter:
			fehlendeParameter.append(parameterNamen[i])

	return fehlendeParameter

@eel.expose
def skriptSchreiben(skriptname, skriptAlsString):
	''' schreibt ein in JS importiertes Skript als Datei in 
	das Arbeitsverzeichnis
	'''
	text_file = open(skriptname, "w", newline='')
	n = text_file.write(skriptAlsString)
	text_file.close()

def funktionImportieren(funktionsname, skriptname):
	try:
		funktion = getattr(__import__(skriptname), funktionsname)
	except:
		return None

	return funktion

def parameterZuordnungBestimmen(parameterNamen, nutzerParameter):
	''' bestimmt zu den Parametern der Funktion, in welcher
	Spalte der Tabelle dieser Parameter eingetragen ist.
	'''
	anzahlParameter = len(parameterNamen)
	zugehoerigeSpalten = [None for i in range(anzahlParameter)]
	for spaltenNr in range(4):
		eintrag = nutzerParameter[spaltenNr]
		if eintrag in parameterNamen:
			# korrekter Eingabewert
			zugehoerigeSpalten[parameterNamen.index(eintrag)] = spaltenNr
	
	return zugehoerigeSpalten

def skriptExistiert(skriptname):
	''' prüft, ob das angegebene Skript im Arbeitsverzeichnis existiert
	nur dann kann eine Funktion aus dem Skript importiert werden
	'''
	try:
		f = open(skriptname + ".py")
		f.close()
	except IOError:
		# die angegebene Datei existiert nicht im Arbeitsverzeichnis
		log = "Die Datei {} existiert leider nicht im Ordner \n {}. \n\nDamit ein Python-Programm ausgeführt werden kann, muss es im selben Ordner wie der Python-Tester gespeichert sein. \n\nTipp: \nWenn Du eine Datei über das Ordnersymbol rechts neben dem Eingabefeld für den Programm-Namen auswählst, wird automatisch eine Kopie im richtigen Ordner erstellt.".format(
			skriptname + ".py"		, os.getcwd())
		eel.testlogAendern(log)
		eel.prompt_alerts(log)
		return False

	return True


@eel.expose
def testsAusfuehren(funktionsname, skriptname, parameter, testdaten):
	''' wird beim Drücken des "Tests ausführen"-Buttons 
	in der GUI aufgerufen
	'''
	log = ""
	anzahlZeilen = len(testdaten)
	anzahlSpalten = 5
	skriptname = skriptname.strip()
	if skriptname[-3:] == ".py":
		# Dateiendung falls vorhanden entfernen
		skriptname = skriptname[:-3]

	if not skriptExistiert(skriptname):
		eel.zeilenEinfaerben(["rgba(255, 123, 0, 0.4)"]*len(testdaten))
		return
	
	funktion = funktionImportieren(funktionsname, skriptname)
	if funktion is None:
		# Funktion mit dem angegebenen Namen existiert nicht im Arbeitsverzeichnis
		log += "Die Funktion: {} existiert in der Datei '{}' nicht. \n\nTipp: \nÖffne das Python-Programm im Editor und kopiere den Funktionsnamen.".format(funktionsname 
		, skriptname + ".py") 
		eel.zeilenEinfaerben(["rgba(255, 123, 0, 0.4)"]*len(testdaten))
		eel.testlogAendern(log)
		eel.testlogAendern(log)
		eel.prompt_alerts(log)
		return
	else:
		log += "Test-Programm: {} \n".format(skriptname + ".py")

	# Spaltennr der Parameter der Funktion
	parameterNamen = inspect.getfullargspec(funktion)[0]
	parameterZuordnung = parameterZuordnungBestimmen(parameterNamen, parameter)
	fehlendeParameter = fehlendeParameterBestimmen(parameterZuordnung, parameterNamen)
	if len(fehlendeParameter) > 0:
		# nicht alle Parameter gegeben
		log += "Es fehlen noch die folgenden Eingabewerte in Deiner Tabelle: \n{}".format(fehlendeParameter)
		eel.testlogAendern(log)
		eel.prompt_alerts(log)
		eel.zeilenEinfaerben(["rgb(30, 30, 10"]*len(testdaten))
	else:
		# Testfälle durchführen
		testen(funktion, parameterZuordnung, testdaten, log, funktionsname)

def testen(funktion, parameterZuordnung, testdaten, log, funktionsname):
	''' führt die einzelnen in der Tabelle beschriebenen Testfälle durch
	'''
	testErgebnisse = []
	for testfall in range(len(testdaten)):
		log += "\nTestfall {}:  ".format(testfall + 1)
		parameterWerte = []
		for i in range(len(parameterZuordnung)):
			parameterWerte.append(testdaten[testfall][parameterZuordnung[i]])

		parameterWerte = inDatentypUmwandeln(parameterWerte)
		parameterAlsString = str(parameterWerte[0])
		for i in range(1, len(parameterWerte)):
			parameterAlsString += ", " + str(parameterWerte[i])
		[ergebnis, ausfuehrungszeit] = funktionAusfuehren(funktion, parameterWerte)
		
		log += "{}({})".format(funktionsname, parameterAlsString)
		log += " = {}\n".format(ergebnis)

		erwartetesErgebnis = inDatentypUmwandeln([testdaten[testfall][4]])[0]
		log += "Erwarteter Rückgabewert: {}\n".format(erwartetesErgebnis)
		if isinstance(ergebnis, str) and ergebnis[:16] == "nicht ausführbar":
			# nicht ausführbar
			testErgebnisse.append("rgba(255, 123, 0, 0.4)")
			log += "Test nicht ausführbar\n"
		elif ergebnis == erwartetesErgebnis:
			# erfolgreich
			testErgebnisse.append("rgb(10, 50, 10)")
			log += "Ausführungszeit: {} ms\n".format(ausfuehrungszeit)
			log += "Test erfolgreich\n"
		else:
			# fehlerhaft
			testErgebnisse.append("rgb(50, 10, 10)")
			log += "Ausführungszeit: {} ms\n".format(ausfuehrungszeit)
			log += "Test fehlgeschlagen\n"

	eel.testlogAendern(log)
	eel.zeilenEinfaerben(testErgebnisse)

def inDatentypUmwandeln(parameter):
	''' alle Parameter werden standardmäßig als string aus der
	Tabelle ausgelesen.
	Diese Funktion konvertiert sie falls möglich in integer, 
	floats, Listen oder Bools
	'''
	for i in range(len(parameter)):

		if parameter == "[]":
			# Leere Liste
			return []
		elif len(parameter) >= 2 and parameter[i][0] == '"' and parameter[i][-1] == '"':
			# string explizit angegeben
			parameter[i] = parameter[i][1:-1]
		elif parameter[i] == "True":
			parameter = True
		elif parameter[i] == "False":
			parameter[i] = False
		elif len(parameter[i]) > 0 and parameter[i][0] == "[":
			parameter[i] = inListeKonvertieren(parameter[i])
		elif "." in parameter[i]:
			# float möglich
			floatWert = None
			try:
				floatWert = float(parameter[i])
			except:
				pass
			if floatWert is not None:
				parameter[i] = floatWert
		else:
			# int möglich
			intWert = None
			try:
				intWert = int(parameter[i])
			except:
				pass
			if intWert is not None:
				parameter[i] = intWert

	return parameter


def inListeKonvertieren(text):
	'''wandelt Text in eine eindimensionale Liste um
	'''
	if text == "[]":
		return []

	text = text.replace("[", "").replace("]", "")
	eintraege = text.split(",")
	# direkt folgende Leerzeichen nach dem Komma entfernen
	eintraege = [eintrag.strip() for eintrag in eintraege]
	return inDatentypUmwandeln(eintraege)


def funktionAusfuehren(funktion, parameterWerte):
	'''ermittelt den Rückgabewert einer Funktion für gegebene 
	Parameter
	Falls die Funktion nicht ausführbar ist, wird der String
	'nicht ausführbar' zurückgegeben
	Außerdem wird die Ausführungszeit bestimmt und in ms zurückgegeben
	'''
	anzahlParameter = len(parameterWerte)
	ausfuehrungszeit = -1
	if anzahlParameter == 0:
		returnVal = None
		try:
			startzeit = time.perf_counter()
			returnVal = funktion()
			ausfuehrungszeit = time.perf_counter() - startzeit
		except Exception as e:
			returnVal = "nicht ausführbar\n" + str(e) 

	elif anzahlParameter == 1:
		returnVal = None
		try:
			startzeit = time.perf_counter()
			returnVal = funktion(
				parameterWerte[0])
			ausfuehrungszeit = time.perf_counter() - startzeit
		except Exception as e:
			returnVal = "nicht ausführbar\n" + str(e)

	elif anzahlParameter == 2:
		returnVal = None
		try:
			startzeit = time.perf_counter()
			returnVal = funktion(
				parameterWerte[0], parameterWerte[1])
			ausfuehrungszeit = time.perf_counter() - startzeit
		except Exception as e:
			returnVal = "nicht ausführbar\n" + str(e)

	elif anzahlParameter == 3:
		returnVal = None
		try:
			startzeit = time.perf_counter()
			returnVal = funktion(
				parameterWerte[0], parameterWerte[1], parameterWerte[2])
			ausfuehrungszeit = time.perf_counter() - startzeit
		except Exception as e:
			returnVal = "nicht ausführbar\n" + str(e)

	elif anzahlParameter == 4:
		returnVal = None
		try:
			startzeit = time.perf_counter()
			returnVal = funktion(
				parameterWerte[0], parameterWerte[1], parameterWerte[2], parameterWerte[3])
			ausfuehrungszeit = time.perf_counter() - startzeit
		except Exception as e:
			returnVal = "nicht ausführbar\n" + str(e)

	return [returnVal, ausfuehrungszeit * 1000]

if __name__ == '__main__':
	eel.init('web')
	eel.start('index.html', size=(1000, 600), mode='edge')
