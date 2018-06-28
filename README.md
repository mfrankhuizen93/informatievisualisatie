# Informatievisualisatie
UvA Informatiekunde Informatievisualisatie Project - juni 2018

## Doel van de visualisatie
Het doel van deze visualisatie is om de gebruiker een inzicht te tonen in het verloop van global warming sinds de Industriële Revolutie en de waarden te toetsen aan de afspraken gemaakt in het Klimaatakkoord van Parijs in 2015. De twee hoofdafspraken van dit akkoord luiden als volgt:  

1. De gemiddelde temperatuur van de hele aarde mag niet meer dan 2 graden Celsius opwarmen ten opzichte van de "pre-industriële" temperatuur. 1850 is hier de benchmark. Dit jaar wordt in de meeste berekeningen gebruikt als de pre-industriële temperatuur omdat men pas vanaf dat jaar betrouwbare temperatuurmetingen is gaan doen.

2. De globale uitstoot van broeikasgassen moet minder dan de helft van de uitstoot in 1990 worden. Hier zijn pas metingen over sinds 1960, dus de visualisatie is ook pas vanaf daar beschikbaar.

 De gebruiker kan voor een specifiek land of voor de hele wereld zien wat het temperatuurverschil en de C02-uitstoot is per decennium. Tevens zijn de doelstellingen uit het Klimaatakkoord weergegeven zodat in een opslag duidelijk is. Er zijn pas metingen van broeikasgassenuitstoot sinds 1960, dus die visualisatie is ook pas vanaf daar beschikbaar.


## Gebruik van het dashboard
Het gebruik van het dashboard is simpel: het enige dat de gebruiker hoeft te doen is de sliders gebruiken om een tijdsperiode te selecteren en een land uit te dropdown selecteren. Voor de wereldkaart geldt dat voor een zelf te kiezen periode de opwarming wordt gekozen, bij de onderste twee grafieken wordt dit steeds voor 10 jaar gedaan. 

##  Dependencies
Voor het runnen van de visualisatie is een aantal libraries nodig:

``` plotly ```

``` pandas ```

``` numpy ```

``` scipy ```

## Data
De volgende datasets zijn benodigd
- [Global emissions](https://drive.google.com/open?id=1DE0RoYx-XKpALXNaPE-wnrEnvHhNVI1N) 
- [Land temperatures by city](https://drive.google.com/open?id=11PvWsnvA14jVF7TyJPUlqYYnBoGtXffb)
- [Global temperatures](https://drive.google.com/open?id=12_sKTg0ciAlRS9YZRN0ZA8fiMrx8OD_Q)

**Let op**: de namen van de datasets moeten hetzelfde blijven. 

## Uitvoering

Download de vier datasets

Plaats de datasets in een map 'data', zodat de folderstructuur er als volgt uitziet
```
.
├── data
│   ├── GlobalCarbonAtlas_territorial.csv
│   ├── GlobalLandTemperaturesByCity.csv
│   ├── GlobalLandTemperaturesByCountry.csv
│   └── GlobalTemperatures.csv
├── license.md
├── README.md
├── app.py
├── bubblemap.py
├── co2.py
└── line.py
1 directory, 10 files

```
Navigeer naar de repo in Terminal en run:

```python app.py```

Navigeer in een browser naar keuze naar:

``` http://127.0.0.1:8050/ ```


## Auteurs
| Naam                   | Studentnummer   | Studie              |
|----------------------- | --------------- | --------------------|
| Michelle Frankhuizen   | 10365354        | Informatica         |
| Ossip Kupperman        | 11013583        | Informatiekunde     |
| Laura Hilhorst         | 11048999        | Informatiekunde     |

## License
Dit project is gelicenseerd onder de MIT License. Zie [license.md](license.md) voor details
