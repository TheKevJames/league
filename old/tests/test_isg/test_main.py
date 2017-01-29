import pytest

import league_utils.isg as isg
import league_utils.models as models
import league_utils.sources as sources


@pytest.mark.skip(reason='CI needs a real token')
def test_no_duplicate_items():
    champ = models.Champion(133, name='Quinn')
    sources.champion_gg(champ)

    for role in champ.roles:
        set_ = isg.item_set(champ, role)
        items = [item for block in set_[3] for item in block[1]]
        assert len(items) == len(set(items))
