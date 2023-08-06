# Adresse

Det finnes allerede [Stedsnavnsøk gjennom kartverket](https://www.kartverket.no/data/stedsnavnsok/) men denne mangler i skrivende stund en funkjson for å finne adresser i nærheten av et geografisk punkt, eller et postnummer.

Dette prosjektet benytter data fra Kartverket, som kan hentes inn fra
[data.kartverket.no](http://data.kartverket.no/download/content/geodataprodukter?korttype=3637&aktualitet=All&datastruktur=All&dataskema=All).

Ettersom det er veldig mye data i `.csv`-filene deres, er dette naturlig nok mye man kanskje ikke trenger.

Dette prosjektet henter ut kun den informasjonen man trenger, og passer på at hver data-objekt er unikt, slik at man ikke får flere oppføringer på samme adressen.

Dette er absolutt ikke et komplett API.

## Generere data

Hent ut .csv-filene som du trenger i lenke over, og legg dem i mappen `data` inne i denne pakken.

Mappestrukturen skal da se noe slik ut:

```
├── norwegian_adresses
│   ├── data
│   │   ├── Dokumentasjon_Adresse.txt
│   │   ├── P13_01_OSTFOLD_Adresse.csv
│   │   ├── P13_02_AKERSHUS_Adresse.csv
│   │   ├── P13_03_OSLO_Adresse.csv
│   │   ├── P13_04_HEDMARK_Adresse.csv
│   │   ├── P13_05_OPPLAND_Adresse.csv
│   │   ├── P13_06_BUSKERUD_Adresse.csv
│   │   ├── P13_07_VESTFOLD_Adresse.csv
│   │   ├── P13_08_TELEMARK_Adresse.csv
│   │   ├── P13_09_AUST-AGDER_Adresse.csv
│   │   ├── P13_10_VEST-AGDER_Adresse.csv
│   │   ├── P13_11_ROGALAND_Adresse.csv
│   │   ├── P13_12_HORDALAND_Adresse.csv
│   │   ├── P13_14_SOGN\ OG\ FJORDANE_Adresse.csv
│   │   ├── P13_15_MORE\ OG\ ROMSDAL_Adresse.csv
│   │   ├── P13_16_SOR-TRONDELAG_Adresse.csv
│   │   ├── P13_17_NORD-TRONDELAG_Adresse.csv
│   │   ├── P13_18_NORDLAND_Adresse.csv
│   │   ├── P13_19_TROMS_Adresse.csv
│   │   ├── P13_20_FINNMARK_Adresse.csv
│   │   └── adresser.json // Denne filen blir opprettet som et mellomledd
```

kjør så følgende kommandoer:
```
pip install -r requirements.txt
python address_extractor.py
```

Programmet vil nå hente ut nødvendig informasjon fra .csv-filene og lagre de. Du vil få opp fremdriften.

Etter ca. 30 sekunder vil det blir opprettet filen `data/adresser.json`.

## Fylle databasen fra `data/adresser.json`

Denne filen kan nå brukes til å legge inn informasjonen i MongoDB.

For å gjøre dette kan du kjøre kommmandoen:

```
python populate_db_pymongo.py --setup
```

Merk at dette vil erstatte all data i samlingen. Du kan spesifisere adressen til samlingen med environment-variabelen `MONGODB_ADDON_URI`.

Etter noen sekunder vil det komme opp "Done", og den er klar til bruk.

### Bruk av apiet.

Klassen må først initialiseres, slik:
```
from norwegian_adresses import NorAddress

nor_address = NorAddress()
```

`NorAddress` tar imot følgende parametre:

- `as_dict`: (`True`) Sålenge denne er sann vil du få hver adresse ut som en `dict`, som er lettere å behandle. Vil du ha ut det originale MongoDB-objectet, setter du verdien til `False`.

#### Kommandoer

- `nor_address.by_post_code`:
  - `post_code`: postnummer du vil bruke til å hente ut data
  - `as_dict=None`: se as_dict
  - henter ut en adresse ut fra en post-kode.
- `nor_address.post_codes_by_post_area`:
  - `post_area`: poststedet du vil hente ut informasjon om
  - `as_dict=None`: se as_dict
  - henter ut en post-koder brukt for et poststed
- `nor_address.by_street_name`:
  - `street_name_with_house_number`: En adresse med/uten husnummer. F.eks. _Kongens Gate_ eller _Kongens gate 14b_
  - `post_code`: postnummer
  - `as_dict=None`: se as_dict
- `nor_address.by_street_name`_closest_to`
  - `street_name`: Gatenavn, f.eks. _Kongens gate_
  - `contains=True`,: Sett til falsk for å gi et strengt søk, hvor hele gatenavnet må være likt.
  - `near_post_code=0`: Søk nær et postnummer
  - `near_geo=None`: Søk nær en geolokasjon. Skal være en `list` med lengde to med breddegrad(latitude) først, så lengdegrad(longitude). Denne tar presedens over `near_post_code`, så om dennne er oppgitt vil den bare søke nær her. Eksempel `[58.16957350413589, 8.028893827316551]`
  - `limit=10`: Hvor mange resultater du vil ha ut på det meste.
  - `as_dict=None`: se as_dict
