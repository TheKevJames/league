# Bard

## Bonus
0 CHIMES: +30 damage on-hit. Meeps respawn every 10 seconds.
5 CHIMES: Meeps now apply a 25% slow for 1 second.
10 CHIMES: +25 more damage on-hit. (55)
15 CHIMES: Meeps stock limit is increased to 2.
20 CHIMES: +25 more damage on-hit. (80)
25 CHIMES: Meeps now strike through target in an AoE cone.
30 CHIMES: +30 more damage on-hit. (110)
35 CHIMES: Respawn time is reduced to 9 seconds.
40 CHIMES: +30 more damage on-hit. (140)
45 CHIMES: Slow increased to 45%.
50 CHIMES: +35 more damage on-hit. (175)
55 CHIMES: Meeps stock limit is increased to 3.
60 CHIMES: +35 more damage on-hit. (210)
65 CHIMES: Width of AoE cone is increased.
70 CHIMES: +35 more damage on-hit. (245)
75 CHIMES: Respawn time is reduced to 8 seconds.
80 CHIMES: +35 more damage on-hit. (280)
85 CHIMES: Slow increased to 60%.
90 CHIMES: +35 more damage on-hit. (315)
95 CHIMES: Meeps stock limit is increased to 4.
100 CHIMES: +30 more damage on-hit. (345)
105 CHIMES: Respawn time is reduced to 7 seconds.
110 CHIMES: +30 more damage on-hit. (375)
115 CHIMES: Slow increased to 70%
120 CHIMES: +25 more damage on-hit. (400)
125 CHIMES: Respawn time is reduced to 6 seconds.
130 CHIMES: +25 more damage on-hit. (425)
135 CHIMES: Slow increased to 75%.
140 CHIMES: +20 more damage on-hit. (445)
145 CHIMES: Slow increased to 80%.
150 CHIMES: +20 more damage on-hit. (465)
EVERY 5 ADDITIONAL CHIMES: +20 more damage on-hit.

## Totals
0: +30 dmg; 1meep/10s
5: +30 dmg +25% slow; 1meep/10s
10: +55 dmg +25% slow; 1meep/10s
15: +55 dmg +25% slow; 1meep/5s
20: +80 dmg +25% slow; 1meep/5s
25: +80 dmg +25% slow in cone; 1meep/5s
30: +110 dmg +25% slow in cone; 1meep/5s
35: +110 dmg +25% slow in cone; 1meep/4.5s
40: +140 dmg +25% slow in cone; 1meep/4.5s
45: +140 dmg +45% slow in cone; 1meep/4.5s
50: +175 dmg +45% slow in cone; 1meep/4.5s
55: +175 dmg +45% slow in cone; 1meep/3s
60: +210 dmg +45% slow in cone; 1meep/3s
65: +210 dmg +45% slow in big cone; 1meep/3s
70: +245 dmg +45% slow in big cone; 1meep/3s
75: +245 dmg +45% slow in big cone; 1meep/2.66s
80: +280 dmg +45% slow in big cone; 1meep/2.66s
85: +280 dmg +60% slow in big cone; 1meep/2.66s
90: +315 dmg +60% slow in big cone; 1meep/2.66s
95: +315 dmg +60% slow in big cone; 1meep/2s
100: +345 dmg +60% slow in big cone; 1meep/2s
105: +345 dmg +60% slow in big cone; 1meep/1.75s
110: +375 dmg +60% slow in big cone; 1meep/1.75s
115: +375 dmg +70% slow in big cone; 1meep/1.75s
120: +400 dmg +70% slow in big cone; 1meep/1.75s
125: +400 dmg +70% slow in big cone; 1meep/1.5s
130: +425 dmg +70% slow in big cone; 1meep/1.5s
135: +425 dmg +75% slow in big cone; 1meep/1.5s
140: +445 dmg +75% slow in big cone; 1meep/1.5s
145: +445 dmg +80% slow in big cone; 1meep/1.5s
150: +465 dmg +85% slow in big cone; 1meep/1.5s
155: +485 dmg +85% slow in big cone; 1meep/1.5s
160: +505 dmg +85% slow in big cone; 1meep/1.5s
165: +525 dmg +85% slow in big cone; 1meep/1.5s
170: +545 dmg +85% slow in big cone; 1meep/1.5s

```python
dps = [
    (0, 30/10),
    (5, 30/10),
    (10, 55/10),
    (15, 55/5),
    (20, 80/5),
    (25, 80/5),
    (30, 110/5),
    (35, 110/4.5),
    (40, 140/4.5),
    (45, 140/4.5),
    (50, 175/4.5),
    (55, 175/3),
    (60, 210/3),
    (65, 210/3),
    (70, 245/3),
    (75, 245/2.66),
    (80, 280/2.66),
    (85, 280/2.66),
    (90, 315/2.66),
    (95, 315/2),
    (100, 345/2),
    (105, 345/1.75),
    (110, 375/1.75),
    (115, 375/1.75),
    (120, 400/1.75),
    (125, 400/1.5),
    (130, 425/1.5),
    (135, 425/1.5),
    (140, 445/1.5),
    (145, 445/1.5),
    (150, 465/1.5),
    (155, 485/1.5),
    (160, 505/1.5),
    (165, 525/1.5),
    (170, 545/1.5),
    (175, 565/1.5),
    (180, 585/1.5),
]

x, y = zip(*dps)
y_deriv = [1] + [y[i] / y[i-1] for i in range(1, len(y))]

import matplotlib.pyplot as plot
plot.clf()
plot.plot(x, y_deriv)

plot.title('Bard DPS per Chimes')
plot.xlabel('Chimes')
plot.ylabel('DPS')
plot.grid(True)
plot.savefig('bard.png')
plot.show()
```
