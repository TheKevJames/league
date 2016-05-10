"""usage:
league-utils isg [--champ=<champ>] [--write | --no-write]
league-utils -h | --help

options:
    isg                    Use the item set generator
    --champ=<champ>        Get info for only this champion.
    --write --no-write     Write to file or print to screen.
    -v --version           Show the version.
    -h --help              Show this screen.
"""
import sys

import docopt

import league_utils.api as api
import league_utils.models as models
import league_utils.isg as isg
import league_utils.isg.encode as encode  # pylint: disable=W0611
import league_utils.isg.groups as groups  # pylint: disable=W0611
import league_utils.output as output
import league_utils.sources as sources


def run():
    args = docopt.docopt(__doc__, version='0.2.6', argv=sys.argv[1:])

    if args['isg']:
        name = None
        if args['--champ']:
            name = args['--champ'].lower()

        champs = api.get_champ(name)
        items = groups.all_()
        for c in sorted(champs, key=lambda x: x['name']):
            champ = models.Champion(c['id'], c['key'], c['name'])
            sources.champion_gg(champ)
            for role in champ.roles:
                item_set = isg.item_set(champ, role, items)
                if args['--write']:
                    # TODO: concurrent:
                    # with concurrent.futures.ProcessPoolExecutor() as exec:
                    #     results = exec.map(main, isg.get_all_champions())
                    # for result in results:
                    #     print('\033[92mok:\033[00m', result.name)
                    data_set = isg.encode.item_set(*item_set)
                    output.to_file(champ, role, data_set)
                    continue

                output.to_screen(champ, role, item_set)

            if args['--write']:
                print('\033[92mok:\033[00m', champ.name)
