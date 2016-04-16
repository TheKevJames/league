import os
import platform


def get_base_dir(system):
    if system == 'Windows':
        return os.path.join('C:', 'Riot Games', 'League of Legends')
    elif system == 'Linux':
        return os.path.join(os.path.expanduser('~'), '.PlayOnLinux',
                            'wineprefix', 'LeagueOfLegends', 'drive_c',
                            'Riot Games', 'League of Legends')
    elif system.startswith('CYGWIN_NT'):
        return os.path.join(os.sep, 'cygdrive', 'c', 'Riot Games',
                            'League of Legends')
    elif system == 'Darwin':
        return os.path.join(os.sep, 'Applications', 'League of Legends.app',
                            'Contents', 'LOL')
    else:
        raise Exception('Platform "{}" not supported.'.format(system))


config_dir = os.path.join(get_base_dir(platform.system()), 'Config')
champions_dir = os.path.join(config_dir, 'Champions')


def to_file(champ, role, item_set):
    champion_dir = os.path.join(champions_dir, champ.key, 'Recommended')

    try:
        os.makedirs(champion_dir)
    except OSError:
        pass

    item_set_file = os.path.join(champion_dir,
                                 '{}_{}.json'.format(champ.key, role.name))
    with open(item_set_file, 'w') as f:
        f.write(item_set)


def to_screen(_champ, _role, item_set):
    print('- {} ({})'.format(item_set[0], item_set[1]))
    for block in item_set[3]:
        print('  - {}:'.format(block[0]))
        for item in block[1]:
            print('    - {}'.format(item.name))
