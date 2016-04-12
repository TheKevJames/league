import os
import platform
import shutil


c_drive = 'C'
if platform.system() != 'Windows':
    c_drive = os.path.join(os.path.expanduser('~'), '.PlayOnLinux',
                           'wineprefix', 'LeagueOfLegends', 'drive_c')

config_dir = os.path.join(c_drive, 'Riot Games', 'League of Legends', 'Config')
champions_dir = os.path.join(config_dir, 'Champions')


def to_file(champ, role, item_set):
    champion_dir = os.path.join(champions_dir, champ.key, 'Recommended')

    try:
        shutil.rmtree(champion_dir)
    except OSError:
        pass

    try:
        os.makedirs(champion_dir)
    except OSError:
        pass

    item_set_file = os.path.join(champion_dir,
                                 '{}_{}.json'.format(champ.key, role.name))
    with open(item_set_file, 'w') as f:
        f.write(item_set)


def to_screen(_champ, _role, item_set):
    print(item_set)
