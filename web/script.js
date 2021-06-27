document.getElementById("funktionsname").value = "produkt";
document.getElementById("skriptname").value = "rechnen.py";

document.getElementById("saveButton").addEventListener("click", () => { tabelleAbspeichern() }, false);
document.getElementById("loadButton").addEventListener("click", () => { tabelleLaden() }, false);

document.getElementById("runButton").addEventListener("click", () => { testen() }, false);
document.getElementById("testLogButton").addEventListener("click", () => { logAnzeigen() }, false);

let tabelle = document.getElementById("tabelle");
let header = tabelle.getElementsByTagName('th');
let eintraege = tabelle.getElementsByTagName('td');
let testLog = "Noch keine Tests ausgeführt";
let hinweisAngezeigt = false;
tabelleEditierbarMachen();
tabelleLaden();

function parameterAuslesen(header) {
  let parameter = [];
  for (let i = 0; i < header.length; i++) {
    parameter.push(header[i]['innerHTML']);
  }
  return parameter
}

function dateinamenAendern()
{
  let filepicker = document.getElementById("filepicker");
  let skriptname = filepicker.value.split(/(\\|\/)/g).pop();
  if (skriptname.length > 0)
  {
    document.getElementById("skriptname").value = skriptname;

    let skriptAlsString = "";
    let files = filepicker.files;
    let reader = new FileReader();
    reader.onload = function (event) {
      console.log('File content:', event.target.result);
      skriptAlsString = event.target.result;
      eel.skriptSchreiben(skriptname, skriptAlsString);
    };
    reader.readAsText(files[0]);
  }
}

function tabelleLaden()
{
  let skriptname = document.getElementById("skriptname").value;
  skriptname = skriptname.replace(".py", "");
  let funktionsname = document.getElementById("funktionsname").value;
  console.log("a");
  eel.tabelleEinlesen(skriptname, funktionsname);
}

function logAnzeigen()
{
  alert(testLog);
}

function testdatenAuslesen(tabellenEintraege) {
  let eintraegeListe = [];
  for (let i = 0; i < tabellenEintraege.length - 1; i++) {
    eintraegeListe.push(tabellenEintraege[i].innerHTML);
  }

  let testfallDaten = [];
  while (eintraegeListe.length) testfallDaten.push(eintraegeListe.splice(0, parameter.length));

  return testfallDaten;
}

function testen() {
  header = tabelle.getElementsByTagName('th');
  eintraege = tabelle.getElementsByTagName('td');
  funktion = document.getElementById("funktionsname").value;
  skript = document.getElementById("skriptname").value;

  parameter = parameterAuslesen(header);
  testdaten = testdatenAuslesen(eintraege);
  eel.testsAusfuehren(funktion, skript, parameter, testdaten);
}

eel.expose(zeilenEinfaerben);
function zeilenEinfaerben(farbenListe) 
{
  eintraege = tabelle.getElementsByTagName('td');
  for (let i = 0; i < farbenListe.length; i++)
  {
    for (let j = 0; j < 5; j++) 
    {
      eintraege[i * 5 + j].style.background = farbenListe[i];
    }
  }
}

eel.expose(testlogAendern);
function testlogAendern(log) 
{
  testLog = log;
}

eel.expose(tabelleUpdaten);
function tabelleUpdaten(neueEintraege) {

  console.log(neueEintraege);
  header = tabelle.getElementsByTagName('th');
  eintraege = tabelle.getElementsByTagName('td');
  for (let j = 0; j < 4; j++) 
  {
    header[j].innerHTML = neueEintraege[0][j];
  }
  for (let i = 1; i < neueEintraege.length; i++)
  {
    for (let j = 0; j < 5; j++) 
    {
      if ((i - 1) * 5 + j == eintraege.length - 1)
      {
        // neue Zeile einfügen
        neueZeile();
        eintraege = tabelle.getElementsByTagName('td');
      }
      eintraege[(i - 1) * 5 + j].innerHTML = neueEintraege[i][j];
    }
  }
  // überflüssige Zeilen löschen
  let anzahlZeilen = (eintraege.length - 1) / 5;
  let anzahlNeueZeilen = neueEintraege.length - 1;
  for (let i = anzahlZeilen - 1; i > anzahlNeueZeilen; i--)
  {
    tabelle.deleteRow(i);
  }
}

function tabelleAbspeichern() {
  let skriptname = document.getElementById("skriptname").value;
  skriptname = skriptname.replace(".py", "");
  let funktionsname = document.getElementById("funktionsname").value;
  header = tabelle.getElementsByTagName('th');
  eintraege = tabelle.getElementsByTagName('td');

  parameter = parameterAuslesen(header);
  testdaten = testdatenAuslesen(eintraege);
  eel.tabelleSpeichern(skriptname, funktionsname, parameter, testdaten);
}

function tabelleEditierbarMachen() {
  header = tabelle.getElementsByTagName('th');
  eintraege = tabelle.getElementsByTagName('td');

  for (let i = 0; i < 4; i++) {
    header[i].onclick = function () {
      if (this.hasAttribute("data-clicked")) {
        return;
      }
      this.setAttribute("data-clicked", "yes");
      this.setAttribute("data-text", this.innerHTML);

      let input = document.createElement("input");
      input.setAttribute("type", "text");
      input.value = this.innerHTML;
      input.style.width = "6.7em";
      input.style.height = "1.4em";
      input.style.margin = "0px";
      input.style.border = "0px";
      input.style.fontFamily = "inherit";
      input.style.fontSize = "inherit";
      input.style.textAlign = "inherit";
      input.style.backgroundColor = "green";
      input.style.color = "white";

      input.onblur = function () {
        let th = input.parentElement;
        let originalText = input.parentElement.getAttribute("data-text");
        let currentText = this.value;

        if (originalText != currentText) {
          // Neuer Text eingegeben
          th.removeAttribute("data-clicked");
          th.removeAttribute("data-text");
          th.innerHTML = currentText;
          th.style.cssText = "padding: 15px";
          console.log(originalText + " hat sich geändert zu: " + currentText);
        }
        else {
          th.removeAttribute("data-clicked");
          th.removeAttribute("data-text");
          th.innerHTML = originalText;
          th.style.cssText = "padding: 15px";
          console.log("Keine Änderung");
        }
      };

      input.onkeydown = function (event) {
        if (event.isComposing || event.keycode == 229) {
          return;
        }
        else if (event.key == "Enter") {
          this.blur();
        }
      };

      this.innerHTML = "";
      this.style.cssText = "padding 0px 0px";
      this.append(input);
      this.firstElementChild.select();
    }
  }

  for (let i = 0; i < eintraege.length - 1; i++) {
    eintraege[i].onclick = function () {
      if (this.hasAttribute("data-clicked")) {
        return;
      }
      this.setAttribute("data-clicked", "yes");
      this.setAttribute("data-text", this.innerHTML);

      let input = document.createElement("input");
      input.setAttribute("type", "text");
      input.value = this.innerHTML;
      input.style.width = "6.7em";
      input.style.height = "1.4em";
      input.style.margin = "0px";
      input.style.border = "0px";
      input.style.fontFamily = "inherit";
      input.style.fontSize = "inherit";
      input.style.textAlign = "inherit";
      input.style.backgroundColor = "green";
      input.style.color = "white";

      input.onblur = function () {
        let td = input.parentElement;
        let originalText = input.parentElement.getAttribute("data-text");
        let currentText = this.value;

        if (originalText != currentText) {
          // Neuer Text eingegeben
          td.removeAttribute("data-clicked");
          td.removeAttribute("data-text");
          td.innerHTML = currentText;
          td.style.cssText = "padding: 15px";
          console.log(originalText + " hat sich geändert zu: " + currentText);
        }
        else {
          td.removeAttribute("data-clicked");
          td.removeAttribute("data-text");
          td.innerHTML = originalText;
          td.style.cssText = "padding: 15px";
          console.log("Keine Änderung");
        }
      };

      input.onkeydown = function (event) {
        if (event.isComposing || event.keycode == 229) {
          return;
        }
        else if (event.key == "Enter") {
          this.blur();
        }
      };

      this.innerHTML = "";
      this.style.cssText = "padding 0px 0px";
      this.append(input);
      this.firstElementChild.select();
    }
  }
}

function neueZeile() {
  let zeile = tabelle.insertRow(tabelle.rows.length - 1);

  let eintrag1 = zeile.insertCell(0);
  let eintrag2 = zeile.insertCell(1);
  let eintrag3 = zeile.insertCell(2);
  let eintrag4 = zeile.insertCell(3);
  let eintrag5 = zeile.insertCell(4);

  tabelleEditierbarMachen();
}


eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description); 
}
