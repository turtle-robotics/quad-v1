import atexit
from time import time
from matplotlib import pyplot
from matplotlib.widgets import Button, Slider
from numpy import array, cos, pi, sin

from quad import l_lower as ll
from quad import l_shoulder as ls
from quad import l_upper as lu
from quad import pos_to_angles
from quad import r_foot as rf
from quad import w_chassis as wc
from quad import l_chassis as lc
from quad import walk_positions

leg_offsets = array([
    # LF, RF, LB, RB
    array([lc/2, wc/2, 0]).T,
    array([lc/2, wc/2, 0]).T,
    array([-lc/2, wc/2, 0]).T,
    array([-lc/2, wc/2, 0]).T
]).T
inversion = array([
    # LF, RF, LB, RB
    array([1, -1, 1]).T,
    array([1, 1, 1]).T,
    array([1, -1, 1]).T,
    array([1, 1, 1]).T
]).T


def update(v, t):
    p = walk_positions(v, t)
    [alpha, beta, gamma] = pos_to_angles(p).T
    s = array([0*alpha, ls*cos(alpha), ls*sin(alpha)])
    u = array([lu*cos(beta), lu*sin(beta)*cos(alpha+pi/2),
               lu*sin(beta)*sin(alpha+pi/2)])
    l = array([p[:, 0], p[:, 1], p[:, 2]-rf])
    pl = array([leg_offsets*inversion, (s+leg_offsets)*inversion,
                (s+u+leg_offsets)*inversion, (l+leg_offsets)*inversion])

    return pl


pl = update(array([0, 0]), 0)

pyplot.ion()
ax = pyplot.axes(projection="3d")
ax.axis("equal")
ax.set(xlim=(-.75*lc, .75*lc),
       ylim=(-.75*lc, .75*lc), zlim=(-.75*lc, .75*lc))
leg_lines = []
foot_dots = []
for leg in pl.T:
    leg_lines += [ax.plot(leg[0], leg[1], leg[2])[0]]
    # foot_dots += [ax.scatter(leg[0, -1], leg[1, -1], leg[2, -1], s=75)]
ax.view_init(elev=-150, azim=-45, roll=0)


atexit.register(pyplot.close)

while True:
    t = time()
    v = array([0.1, 0])
    pl = update(v, t)
    for leg, leg_line in zip(pl.T, leg_lines):
        leg_line.set_data_3d(leg[0], leg[1], leg[2])
        # foot_dot._offsets3d = (leg[0, -1], leg[1, -1], leg[2, -1])
    pyplot.draw()
    pyplot.pause(0.05)
