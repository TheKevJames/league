LeagueUtils
===========

LeagueUtils is a set of utilities for interacting with League of Legends data.
Currently, it contains the League ISG (Item Set Generator) and an API for item
gold efficiency.

|version| |build| |coverage| |codacy| |landscape| |requirements|

ISG
---

The Item Set Generator is designed to build recommended pages for every
champion in every viable role. It does this by pulling date from Riot's API and
from some third party sites, determining which build paths work best, and
updating your League config with the results.

Usage
~~~~~

The most common use case is to run

::

    league-utils-isg

to install the item sets for every champion. The item sets will be installed
beside the default Riot recommended pages, but if you have manually downloaded
item sets into your config directory before, these may be overwritten. Make
sure any such files have unique names before running this script! (eg. anything
other than :code:`${CHAMPION}_${ROLE}.json`).

You can also run something like

::

    league-utils-isg --champ Rumble

to load info on only one champion.

Gold Efficiency
---------------

The Gold Efficiency project automatically calculates the efficiency of all
items by looking at the vallue of the stats they provide. This is a common form
of `theory crafting`_.

These stats are calculated in real-time, and thus will always be up-to-date
when a new patch is released.

When using this data, keep in mind that some aspects of items such as unique
abilities will not be taken into account in determining the worth of an item.
The ignored stats or abilities will be returned in the result.

Usage
~~~~~

For now, this is available only as a REST API. You can access the results for
any item by ID. For example, to get efficiency data on Overlord's Bloodmail,
run

::

    curl https://league.thekev.in/item/3084/efficiency

Setup
-----

Install from PyPI
~~~~~~~~~~~~~~~~~

Simply run

::

    pip3 install league-utils

Install from Source
~~~~~~~~~~~~~~~~~~~

After cloning this repo or downloading and un{zip,tar}ing the `most recent
zipfile or tarball`_.

::

    python3 setup.py install

Run without installing
~~~~~~~~~~~~~~~~~~~~~~

This project can also be run without installation. After cloning this repo or
downloading and un{zip,tar}ing the `most recent zipfile or tarball`_, run

::

    pip3 install -r requirements.txt

and use the `league-utils.py` script in the root of this folder. Working in a
`virtualenv`_ is recommended!

Note that when using this method, the sub-project must be provided as an
argument. For example:

::

    league-utils-isg [options]  # becomes: ./league-utils.py isg [options]

From a binary
~~~~~~~~~~~~~

Pre-compiled binaries are provided for some Operating Systems. If yours is
supported, you can grab the binary for the `latest release`_ and just run that
without installing anything. Note that using this method does not allow you to
easily update your installation.

If you use a binary to run :code:`league-utils`, make sure you use the
:code:`league-utils.py` syntax described above.

Running Your Own Server
=======================

So you want to run your own API server, eh? Well, there's a convenient docker
file you can use for that, but it does require just a bit of setup.

You'll need to get yourself API keys for both Riot's API and champion.gg's.
Once you do, simply export them to your shell and use docker-compose to run the
server. Roughly speaking, you'll want to:

::

    export CHAMPIONGG_TOKEN=foo-asdfasdfasdf
    export LEAGUE_TOKEN=bar-fdsafdsafdsa
    git clone git@github.com:thekevjames/league.git
    cd league
    docker-compose build
    docker-compose up

You may also be interested in using the `official docker image`_. If you are,
the following might make your life easier:

::

    curl https://raw.githubusercontent.com/TheKevJames/league/master/docker-compose.yml > docker-compose.yml
    curl https://raw.githubusercontent.com/TheKevJames/league/master/docker-compose.override.yml > docker-compose.override.yml
    docker-compose pull
    docker-compose up -d

If you're looking for something a bit more production-ready, you can also deploy
this project to a Docker Swarm cluster. In that case, you'll need to configure
Docker secrets and deploy this to a stack:

::

    echo "my-championgg-token" | docker secret create championgg_token -
    echo "my-riot-token" | docker secret create riot_token -
    echo "my-sentry-dsn" | docker secret create sentry_dsn_league -

    curl https://raw.githubusercontent.com/TheKevJames/league/master/docker-compose.yml > league.yml
    docker stack deploy -c league.yml thekevjames

    # to force an update to the latest build
    docker service update --force thekevjames_league_utils_api

Release Procedure
=================

I love automating the shit out of things, but I'm still not done. CI takes care
of a huge number of things in this repo, but it doesn't yet do everything. This
section is meant to remind me of the parts I have to do manually and thus need
to get around to automating.

::

    # OLD_TAG=$(git tag --sort=version:refname | tail -n1)
    find ./ -type f -exec sed -i "s/OLD_TAG/NEW_TAG/g" *.py {} \;  # OSX: -i ''
    clog -C CHANGELOG.md -F --setversion NEW_TAG
    git commit -am 'chore(release): release new version'
    git tag NEW_TAG
    git push

At some point, I may consider integrating an "unreleased" changelog:

::

    clog -C CHANGELOG.md -F --setversion unreleased

Disclaimer
==========

This project probably won't make your computer explode, make your girlfriend
leave you, or get you fired from your job, but I make no guarantees that
blindly following its advice won't drop your ELO. You've been warned.

.. |build| image:: https://img.shields.io/circleci/project/TheKevJames/league.svg
    :target: https://circleci.com/gh/TheKevJames/league
.. |codacy| image:: https://img.shields.io/codacy/a8f370e55fc94d72b92b2b6615ce165b.svg
    :target: https://www.codacy.com/app/KevinJames/league
.. |downloads| image:: https://img.shields.io/pypi/dm/league-utils.svg
    :target: https://pypi.python.org/pypi/league-utils
.. |landscape| image:: https://landscape.io/github/TheKevJames/league/master/landscape.svg?style=flat
    :target: https://landscape.io/github/TheKevJames/league/master
.. |requirements| image:: https://pyup.io/repos/github/TheKevJames/league/shield.svg
    :target: https://pyup.io/repos/github/TheKevJames/league/
.. |version| image:: https://img.shields.io/pypi/v/league-utils.svg
    :target: https://pypi.python.org/pypi/league-utils

.. _`latest release`: https://github.com/thekevjames/league/releases/latest
.. _`most recent zipfile or tarball`: https://github.com/thekevjames/league/releases/latest
.. _`official docker image`: https://hub.docker.com/r/thekevjames/league-utils-api/
.. _`theory crafting`: http://leagueoflegends.wikia.com/wiki/Gold_efficiency
.. _`virtualenv`: virtualenvwrapper.readthedocs.org
