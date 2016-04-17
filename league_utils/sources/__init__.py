import bs4
import requests

import league_utils.common as common
import league_utils.models as models


def champion_gg(champ):
    def parse_id(src):
        return int(src.split('/')[-1].split('.')[0])

    BUILD = '.col-md-7 .build-wrapper a img'
    ROLES = '.champion-profile ul li a h3'
    STARTS = '.col-md-5 .build-wrapper a img'

    url = 'http://champion.gg/champion/{}'.format(champ.key)
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    champ.roles = common.dedup(
        champ.roles + [models.Role(x.text.strip())
                       for x in soup.select(ROLES)])

    for role in champ.roles:
        url = 'http://champion.gg/champion/{}/{}'.format(champ.key, role.name)
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')

        champ.builds[role] += [
            models.Item(parse_id(x['src']), x['tooltip'])
            for x in soup.select(BUILD)]
        champ.starts[role] += [
            models.Item(parse_id(x['src']), x['tooltip'])
            for x in soup.select(STARTS)]
