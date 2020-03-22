import html2text
import lxml.html
import re
import requests

from collections import defaultdict
from datetime import date


PAGE = (
    "https://www.regione.piemonte.it/web/pinforma/notizie/"
    "coronavirus-gli-aggiornamenti-dalla-regione-piemonte"
)

LOCALIZED_MONTH_TO_INT = {
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12,
}

PROVINCES = ('AL', 'AT', 'BI', 'CN', 'NO', 'TO', 'VC', 'VCO', 'EXTRA')

DATE_RE = re.compile(r"^#### \w+ (?P<day>\d+) (?P<month>\w+)$")
DEATHS_RE = (
    re.compile(r"(?P<tot_deaths>\d+) deceduti risultati positivi al virus(?P<deaths>.*)"),
    re.compile(r"il numero dei deceduti positivi al virus e salito a (?P<tot_deaths>\d+) (?P<deaths>.*)"),
    re.compile(r"Complessivamente, il totale dei deceduti e di (?P<tot_deaths>\d+)(?P<deaths>.*)"),
    re.compile(r"Il totale complessivo e ora di (?P<tot_deaths>\d+)(?P<deaths>.*)"),
)
ALESSANDRIA_RE = (
    re.compile(r"(?P<deaths>\d+)( ad)? Alessandria"),
    re.compile(r"Alessandria (?P<deaths>\d+)"),
)
ASTI_RE = (
    re.compile(r"(?P<deaths>\d+)( ad)? Asti"),
    re.compile(r"Asti (?P<deaths>\d+)"),
)
BIELLA_RE = (
    re.compile(r"(?P<deaths>\d+)( a)? Biella"),
    re.compile(r"Biella (?P<deaths>\d+)"),
)
CUNEO_RE = (
    re.compile(r"(?P<deaths>\d+)( a)? Cuneo"),
    re.compile(r"Cuneo (?P<deaths>\d+)"),
)
NOVARA_RE = (
    re.compile(r"(?P<deaths>\d+)( a)? Novara"),
    re.compile(r"Novara (?P<deaths>\d+)"),
)
TORINO_RE = (
    re.compile(r"(?P<deaths>\d+)( a)? Torino"),
    re.compile(r"Torino (?P<deaths>\d+)"),
)
VERCELLI_RE = (
    re.compile(r"(?P<deaths>\d+)( a)? Vercelli"),
    re.compile(r"Vercelli (?P<deaths>\d+)"),
)
VCO_RE = (
    re.compile(r"(?P<deaths>\d+) (nel Verbano-Cusio-Ossola|VCO)"),
    re.compile(r"Verbano-Cusio-Ossola (?P<deaths>\d+)"),
)
FUORI_REGIONE_RE = (
    re.compile(r"(?P<deaths>\d+) residenti fuori regione"),
    re.compile(r"residenti fuori regione (?P<deaths>\d+)"),
)

PROVINCES_DEATHS_RE = (
  ('AL', ALESSANDRIA_RE),
  ('AT', ASTI_RE),
  ('BI', BIELLA_RE),
  ('CN', CUNEO_RE),
  ('NO', NOVARA_RE),
  ('TO', TORINO_RE),
  ('VC', VERCELLI_RE),
  ('VCO', VCO_RE),
  ('EXTRA', FUORI_REGIONE_RE),
)

def download_page():
    r = requests.get(PAGE)
    return r.text

def prepare_page(page):
    html = lxml.html.fromstring(page)
    content = html.cssselect(".field--name-field-corpo")[0]
    content_string = lxml.html.tostring(content)
    h = html2text.HTML2Text()
    # remove <strong> tags
    h.strong_mark = ""
    # don't wrap long lines
    h.body_width = 0
    text = h.handle(content_string.decode("utf-8"))
    return text

def parse_day_from_line(line):
    match = DATE_RE.match(line)
    if match:
        month = LOCALIZED_MONTH_TO_INT[match.group('month')]
        return date(2020, month, int(match.group('day')))
    return None

def parse_deaths_from_line(line):
    for death_re in DEATHS_RE:
        match = death_re.search(line)
        if match:
            tot_deaths = int(match.group('tot_deaths'))
            deaths_str = match.group('deaths')
            deaths = defaultdict(int)
            for province, province_res in PROVINCES_DEATHS_RE:
                for province_re in province_res:
                    match = province_re.search(deaths_str)
                    if match:
                        deaths[province] = int(match.group('deaths'))
            return tot_deaths, deaths
    return None

def parse_page(page):
    lines = page.split('\n')
    for line in lines:
        day = parse_day_from_line(line)
        if day:
            print(day)
            continue
        deaths = parse_deaths_from_line(line)
        if deaths:
            print(deaths)
            continue

if __name__ == '__main__':
    page = download_page()
    prepared = prepare_page(page)
    parse_page(prepared)
