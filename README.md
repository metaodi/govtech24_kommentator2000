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

## Ziele
Dieses Projekt hat folgende Ziele:

1. Daten im XML Format Akoma Ntoso umzuwandeln (z.B. JSON)
1. Die Daten pro Paragraph in einem Frontend darzustellen
1. Jeder Paragraph braucht eine eindeutige ID
1. Gemachte Änderungen sollen nachvollziehbar sein (z.B. als GitHub Pull Request)


## Installation

* Run `python_setup.sh`
* Copy `.env.dist` to `.env` and adapt the values
* Run the flask app using `flask run`
