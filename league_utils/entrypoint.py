"""usage:
league-utils datascience <name>
league-utils info (--champ=<champ> | --item=<item>)
league-utils isg [--champ=<champ>] [--write | --no-write] [--path=/path/to/lol]
league-utils -h | --help

options:
datascience         Run a data science experiment
info                Show API info on object.
isg                 Use the item set generator
<name>              Data science experiment to run.
--champ=<champ>     Get info for only this champion.
--item=<item>       Get info for only this item.
--write --no-write  Write to file or print to screen.
--path=<path>       Override the path to your LoL installation.
                    By default, this is:
                    "C:\\Program Files\\Riot Games\\League of Legends"
-v --version        Show the version.
-h --help           Show this screen.
"""
import sys

import docopt

import league_utils.api as api
import league_utils.data_science as data_science
import league_utils.models as models
import league_utils.isg as isg
import league_utils.isg.encode as encode  # pylint: disable=W0611
import league_utils.isg.groups as groups  # pylint: disable=W0611
import league_utils.output as output
import league_utils.sources as sources


def run():
    args = docopt.docopt(__doc__, version='0.3.2', argv=sys.argv[1:])

    if args['datascience']:
        return data_science.run(args['<name>'])

    if args['info']:
        if args['--champ']:
            name = args['--champ'].lower()
            champ = api.get_champ(name)[0]
            champ = models.Champion(champ['id'], champ['key'], champ['name'])
            champ.dump()
        elif args['--item']:
            name = args['--item'].lower()
            item = api.get_item(name)[0]
            item = models.Item(item['id'], item['name'])
            item.dump()

        return

    if args['isg']:
        if args['--write']:
            path = args['--path']
            if not path:
                path = output.get_base_dir()

            print('> writing item sets to {}'.format(path))
            champ_dir = output.build_path(path)

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
                    output.to_file(champ_dir, champ, role, data_set)
                    continue

                output.to_screen(champ, role, item_set)

            if args['--write']:
                print('\033[92mok:\033[00m', champ.name)
