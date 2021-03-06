"""
Test module for transformations.
"""
from geojson import Feature, LineString, Point

from turfpy.transformation import bbox_clip, bezie_spline, circle, intersect, union


def test_circle():
    center = Feature(geometry=Point((-75.343, 39.984)))
    cc = circle(center, radius=5, steps=10)
    cc = cc["geometry"]
    assert cc.type == "Polygon"
    assert len(cc.coordinates[0]) == 11
    assert cc.coordinates == [
        [
            [-75.343, 40.028966],
            [-75.377513, 40.020373],
            [-75.398824, 39.997882],
            [-75.398802, 39.970091],
            [-75.377476, 39.947617],
            [-75.343, 39.939034],
            [-75.308524, 39.947617],
            [-75.287198, 39.970091],
            [-75.287176, 39.997882],
            [-75.308487, 40.020373],
            [-75.343, 40.028966],
        ]
    ]


def test_bbox_clip():
    f = Feature(
        geometry={
            "coordinates": [[[2, 2], [8, 4], [12, 8], [3, 7], [2, 2]]],
            "type": "Polygon",
        }
    )
    bbox = [0, 0, 10, 10]
    clip = bbox_clip(f, bbox)
    clip = clip["geometry"]
    assert clip.type == "Polygon"
    assert len(clip.coordinates[0]) == 6
    assert clip.coordinates == [
        [[10.0, 6.0], [8.0, 4.0], [2.0, 2.0], [3.0, 7.0], [10.0, 7.777778], [10.0, 6.0]]
    ]


def test_intersection():
    f = Feature(
        geometry={
            "coordinates": [
                [
                    [-122.801742, 45.48565],
                    [-122.801742, 45.60491],
                    [-122.584762, 45.60491],
                    [-122.584762, 45.48565],
                    [-122.801742, 45.48565],
                ]
            ],
            "type": "Polygon",
        }
    )
    b = Feature(
        geometry={
            "coordinates": [
                [
                    [-122.520217, 45.535693],
                    [-122.64038, 45.553967],
                    [-122.720031, 45.526554],
                    [-122.669906, 45.507309],
                    [-122.723464, 45.446643],
                    [-122.532577, 45.408574],
                    [-122.487258, 45.477466],
                    [-122.520217, 45.535693],
                ]
            ],
            "type": "Polygon",
        }
    )
    inter = intersect(f, b)
    inter = inter["geometry"]
    assert inter.type == "Polygon"
    assert len(inter.coordinates[0]) == 7
    assert inter.coordinates == [
        [
            [-122.584762, 45.545509],
            [-122.584762, 45.48565],
            [-122.689027, 45.48565],
            [-122.669906, 45.507309],
            [-122.720031, 45.526554],
            [-122.64038, 45.553967],
            [-122.584762, 45.545509],
        ]
    ]


def test_bezie_spline():
    ls = LineString(
        [
            (-76.091308, 18.427501),
            (-76.695556, 18.729501),
            (-76.552734, 19.40443),
            (-74.61914, 19.134789),
            (-73.652343, 20.07657),
            (-73.157958, 20.210656),
        ]
    )

    f = Feature(geometry=ls)

    bf = bezie_spline(f)
    bf = bf["geometry"]
    assert bf.type == "LineString"
    assert len(bf.coordinates) == 500


def test_union():
    p1 = Feature(
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [-82.574787, 35.594087],
                    [-82.574787, 35.615581],
                    [-82.545261, 35.615581],
                    [-82.545261, 35.594087],
                    [-82.574787, 35.594087],
                ]
            ],
        }
    )

    p2 = Feature(
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [-82.560024, 35.585153],
                    [-82.560024, 35.602602],
                    [-82.52964, 35.602602],
                    [-82.52964, 35.585153],
                    [-82.560024, 35.585153],
                ]
            ],
        }
    )
    result = union([p1, p2])
    assert dict(result) == {
        "type": "Feature",
        "geometry": {
            "coordinates": [
                [
                    [-82.560024, 35.585153],
                    [-82.560024, 35.594087],
                    [-82.574787, 35.594087],
                    [-82.574787, 35.615581],
                    [-82.545261, 35.615581],
                    [-82.545261, 35.602602],
                    [-82.52964, 35.602602],
                    [-82.52964, 35.585153],
                    [-82.560024, 35.585153],
                ]
            ],
            "type": "Polygon",
        },
        "properties": {},
    }
