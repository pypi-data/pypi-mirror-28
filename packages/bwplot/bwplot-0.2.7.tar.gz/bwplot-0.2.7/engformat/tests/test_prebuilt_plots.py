__author__ = 'maximmillen'

import numpy as np
import matplotlib.pyplot as plt
from bwplot import cbox

import engformat.plot as esfp


def test_basic_xy():
    x = np.linspace(0, 10, 50)
    y = x ** 2
    big_fig = plt.figure()
    sf = big_fig.add_subplot(111)
    sf.plot(x, y, label="test")
    esfp.xy(sf)


def test_pb_time_series():
    x = np.linspace(0, 10, 50)
    y = x ** 2
    big_fig = plt.figure()
    sf = big_fig.add_subplot(111)
    sf.plot(x, y, label="test")
    esfp.time_series(sf)


def test_pb_xy():
    A = plt.figure(figsize=(6, 4))
    P1 = A.add_subplot(111)
    y = np.random.normal(size=1000).cumsum()
    x = np.arange(1000)
    P1.plot(x, y, c=cbox(1), alpha=0.7, label='chur')
    P1.set_xlabel('Time $[s]$')
    esfp.xy(P1)


def test_pb_transfer_function():
    x = np.linspace(0, 10, 50)
    y = x ** 1.2
    big_fig = plt.figure()
    sp = big_fig.add_subplot(111)
    sp.plot(x, y, label="test")
    esfp.transfer_function(sp, ratio=True)
    lines = sp.get_lines()
    assert len(lines) == 2
    assert lines[0].get_zorder() == 102
    assert lines[1].get_zorder() == 50  # ratio line
    xlim = sp.get_xlim()
    ylim = sp.get_ylim()
    assert xlim[0] == 0.0
    assert xlim[1] == 10.5
    assert ylim[0] == 0.0



if __name__ == '__main__':
    test_pb_transfer_function()
    plt.show()
    # test_pb_timeseries()