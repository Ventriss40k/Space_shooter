import math

x1 = 0
y1 = 0
x2 = 5
y2 = 10

angle = math.atan2(y2 - y1, x2 - x1)

print("Angle between ({}, {}) and ({}, {}): {:.2f} degrees".format(x1, y1, x2, y2, math.degrees(angle)))
