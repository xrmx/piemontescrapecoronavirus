# piemontescrapecoronavirus

Questo repository contiene uno scraper della pagina di aggiornamento sul Coronavirus
della regione Piemonte. Ad oggi parsifica solo il conteggio dei decessi totali per
le singole province.

## Requisiti

Su una distribuzione basata su Debian dovresti poter usare tutti i pacchetti di sistema:

```
sudo apt install python3 python3-cssselect python3-lxml python3-html2text python3-requests
```

Altrimenti crea un virtualenv:

```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

e ricorda di attivarlo quando vuoi usare lo scraper

```
. ./venv/bin/activate
```

## Uso

```
$ python3 scraper.py
{"2020-03-14": {"AL": 28, "AT": 3, "BI": 4, "CN": 2, "NO": 5, "TO": 13, "VC": 3, "VCO": 1}, "2020-03-15": {"AL": 47, "AT": 5, "BI": 5, "CN": 5, "NO": 7, "TO": 19, "VC": 5, "VCO": 1}}
```

## Formato dati

Lo scraper ritorna un oggetto JSON con chiave la data in formato ISO e come valore un altro
oggetto JSON con chiave la sigla della provincia (più EXTRA per quelli di fuori regione) e
come valore il totale dei decessi a quel giorno per quella provincia.
