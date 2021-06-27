# Python-Tester

## Einsatzzweck

ein didaktisch reduziertes Tool zum Testen von Python-Funktionen

## Benutzung

Testfälle werden analog zu Column-Fixtures in FitNesse erstellt (http://fitnesse.org/FitNesse.UserGuide.FixtureGallery.BasicFitFixtures.ColumnFixture)

Die ersten vier Spalten können für Eingabe-Parameter genutzt werden.
In der fünften Spalte wird der erwartete Rückgabewert der Funktion eingetragen.


## Technische Umsetzung

Das Hauptprogramm wurde in Python 3 geschrieben.
Die GUI wurde mit HTML & CSS erstellt.
Änderungen in der GUI werden mit JS durchgeführt.
Zur Kommunikation von JS und dem Python-Hauptprogramm wird das Python-Modul `Eel` (https://github.com/ChrisKnott/Eel) genutzt.
Dieses muss zusätzlich installiert werden (`pip install eel` unter Linux, `python -m pip install eel` unter Windows).