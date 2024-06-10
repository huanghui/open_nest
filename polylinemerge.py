from shapely.ops import linemerge
from shapely.ops import polygonize
lines = [
    ((0, 0), (1, 1)),
    ((0, 0), (0, 1)),
    ((0, 1), (1, 1)),
    ((1, 1), (1, 0)),
    ((1, 0), (0, 0))
    ]
print(list(polygonize(lines)))
linemerge(lines)
#<shapely.geometry.multilinestring.MultiLineString object at 0x...>
print(list(linemerge(lines)))
