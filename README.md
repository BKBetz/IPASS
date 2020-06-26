# IPASS

### Wat is wat

#### rapportage:
* Een deel van mijn PvA (met wat aanpasisngen) en een terugblik op et project
* Bronvermelding

#### Poster:
* Poster om kort te tonen wat mijn project inhoud

#### Program:
* Project die bestaat uit meerdere folders en bestanden
1. backend:
    * Bijna alles wat op de achtergrond staat hier
        1. activities.json: Json file met alle bestanden erin wordt gebruikt om advies te geven over de gevraagde activiteit
        2. download.py: Klein bestand om nltk mee te downloaden.. pip install nltk wel eerst.
        3. permission.py: Vraagt de gebruiker om zijn exacte locatie of om een locatie in te voeren.
        4. request.py: Krijgt de locatie binnen van de gebruiker en gebruikt dit om het huidige weer en weersvoorspellingen te krijgen
        5. user_input.pt: Ontleed de vraag van de gebruiker. Kijkt of er datums in zitten en welke woorden belangrijk zijn
2. Html:
    * Documentatie. Elke filenaam is de documentatie voor dat bestand
3. Static:
     * Css voor de frontend
4. Templates:
    * De website
5. Tests:
    * Testfile voor pytests  
6. machine.py:
    * Backend bestand die voor wat voor reden dan ook de json niet goed kon importen tenzij het hier stond..dus dat.
    Maakt gebruik van weersvoorspellingen en de user input die is gefiltered door functies in de backend bestanden om op een 
    antwoord te komen en als nodig is advies te geven.
    
7. main.py:
    * Bestand die de flask pagina runt en werkt als brug tussen html en python. Run dit bestand om heel de applicatie te testen.