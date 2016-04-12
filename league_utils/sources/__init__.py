import bs4
import requests

import league_utils.models as models


# TODO: merge with other sources
def champion_gg(champ):
    url = 'http://champion.gg/champion/{}'.format(champ.key)
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    champ.roles = [models.Role(x.text.strip())
                   for x in soup.select('.champion-profile ul li a h3')]

    for role in champ.roles:
        url = 'http://champion.gg/champion/{}/{}'.format(champ.key, role.name)
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        champ.builds[role] = [
            models.Item(x['src'].split('/')[-1].split('.')[0], x['tooltip'])
            for x in soup.select('.col-md-7 .build-wrapper a img')]
        champ.starts[role] = [
            models.Item(x['src'].split('/')[-1].split('.')[0], x['tooltip'])
            for x in soup.select('.col-md-5 .build-wrapper a img')]
