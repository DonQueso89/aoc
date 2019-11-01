from day20 import clipped_range


def test__clipped_range():
    blocked = [
        (5, 10),
        (7, 12),
        (3, 6),
    ]
    assert clipped_range(1, 4, blocked) == (1, 2)
    assert clipped_range(2, 4, blocked) == (2, 3)
    
    blocked = [
        (20, 30),
        (4, 10),
        (7, 19),
    ]
    assert clipped_range(1, 4, blocked) == (1, 2)

