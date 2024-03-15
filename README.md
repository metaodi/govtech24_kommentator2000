# Kommentator 2000
## Analyse

[Akoma Ntoso](http://www.akomantoso.org/) ist komplex.

Verschiedene Akoma Ntoso Editoren gibt es am Markt:
- [Indigo by Laws.Africa](https://github.com/laws-africa/indigo)
- [Lime by University of Bologna](https://github.com/cirsfid-unibo/lime)
- [LEOS by EU](https://code.europa.eu/leos/core)

Für den Vernehmlassung Prozess abzuwickeln gibt es in der Schweiz folgende bekannte Akteure ausserhalb der Bundesverwaltung:
- [demokratis.ch](https://demokratis.ch/)
- [e-mitwirkung.ch](https://e-mitwirkung.ch/)
  - [E-Mitwirkung des Kanton Luzern](https://lu.e-mitwirkung.ch/de/)

Im Akamo Ntoso XML von Fedlex können folgende Identifikatoren verwendet werden:
```
// document/law identification
// e.g. "https://fedlex.data.admin.ch/eli/cc/1999/170/20240201"
/akomaNtoso/act/meta/identification/FRBRWork/FRBRuri[@value]
// paragraph identification
// e.g. "art_1/para_1"
//paragraph[@eId]
```
### Entwurfsentscheidungen
- Datenformat: Umwandlung in einfacheres Zwischenformat vs. mit der Komplexität von Akoma Ntoso umgehen
- Granularität des Editor: ein Editor pro Artikel oder Paragraph vs. ein Editor für den Rechtstext 


## Approach #1

1. Daten im XML Format Akoma Ntoso umzuwandeln (z.B. JSON)
1. Die Daten pro Paragraph in einem Frontend darzustellen
1. Jeder Paragraph braucht eine eindeutige ID
1. Gemachte Änderungen sollen nachvollziehbar sein (z.B. als GitHub Pull Request)

### Installation

* Run `python_setup.sh`
* Copy `.env.dist` to `.env` and adapt the values
* Run the flask app using `flask run`

## Approach #2

1. Daten im XML Format Akoma Ntoso direkt editieren

### Installation
* Run a local web server like "Live Server" and open https://localhost/prosemirror-k2k/prosemirror-k2k.html

# Pitch

1. Auf fedlex.admin.ch Rechtstext öffnen und die Artikel und Paragraphen markieren die geändert werden sollen
1. Kommentator 2000 zeigt den Rechtstext aufbereitet an
1. Änderungen können auf Paragraph Ebene eingegeben werden