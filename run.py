#!/usr/bin/env python3
import concurrent.futures
import os
import platform
import shutil

import league


base_dir = None
if platform.system() == 'Windows':
    base_dir = 'C'
else:
    base_dir = os.path.join(os.path.expanduser('~'), '.PlayOnLinux',
                            'wineprefix', 'LeagueOfLegends', 'drive_c')

base_dir = os.path.join(base_dir, 'Riot Games', 'League of Legends', 'Config',
                        'Champions')


def main(champ):
    d = os.path.join(base_dir, champ.key, 'Recommended')

    try:
        shutil.rmtree(d)
    except OSError:
        pass

    try:
        os.makedirs(d)
    except OSError:
        pass

    champ.sets(d)
    return champ


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(main, league.get_all_champions())

    for result in results:
        print('\033[92mok:\033[00m {}'.format(result.name))
