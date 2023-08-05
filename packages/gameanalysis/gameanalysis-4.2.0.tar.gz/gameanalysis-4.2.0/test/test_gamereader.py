import functools
import json
import pytest

import numpy as np

from gameanalysis import agggen
from gameanalysis import gambit
from gameanalysis import gamegen
from gameanalysis import gamereader
from gameanalysis import learning
from gameanalysis import matgame
from gameanalysis import rsgame
from test import testutils


@functools.lru_cache()
def egame():
    return rsgame.emptygame([3, 4], [4, 3])


@functools.lru_cache()
def game():
    return gamegen.add_profiles(egame(), 0.5)


def sgame():
    return gamegen.add_noise(game(), 1, 3)


def agg():
    return agggen.normal_aggfn([3, 4], [4, 3], 10)


def mat():
    return matgame.matgame(np.random.random((4, 3, 2, 3)))


@functools.lru_cache()
def rbf():
    return learning.rbfgame_train(game())


def point():
    return learning.point(rbf())


def sample():
    return learning.sample(rbf())


def neighbor():
    return learning.neighbor(rbf())


@testutils.warnings_filter(UserWarning)
@pytest.mark.parametrize('game', [
    egame, game, sgame, agg, mat, rbf, point, sample, neighbor, 'gambit'])
def test_automatic_deserialization(game):
    """Test that we can serialize and deserialize arbitrary games"""
    if game == 'gambit':
        game = mat()
        string = gambit.dumps(game)
    else:
        game = game()
        string = json.dumps(game.to_json())
    copy = gamereader.loads(string)
    assert game == copy


def test_parse_fail():
    with pytest.raises(AssertionError):
        gamereader.loads('')


@testutils.warnings_filter(DeprecationWarning)
def test_deprecation():
    gamereader.read(egame().to_json())
