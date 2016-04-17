import bs4
import requests

import league_utils.common as common
import league_utils.models as models


def champion_gg(champ):
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
            models.Item(x['src'].split('/')[-1].split('.')[0], x['tooltip'])
            for x in soup.select(BUILD)]
        champ.starts[role] += [
            models.Item(x['src'].split('/')[-1].split('.')[0], x['tooltip'])
            for x in soup.select(STARTS)]


def lolflavor(champ):
    # TODO: these builds are inserted into the page after load
    url = 'http://www.lolflavor.com/champions/{}/'.format(champ.key)  # pylint: disable=W0612


def metalol(champ):
    # TODO: these builds are not role-specific
    url = 'http://www.metalol.net/champions/{}'.format(champ.name)  # pylint: disable=W0612


def probuilds(champ):
    # TODO: these builds are not role-specific
    url = 'http://probuilds.net/champions/details/{}'.format(champ.key)  # pylint: disable=W0612
