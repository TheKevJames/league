from .experiment import GoldItemsSupport


def run(experiment):
    if experiment == 'gold.items.support':
        return GoldItemsSupport().render()

    raise Exception("No experiment named '{}'".format(experiment))
