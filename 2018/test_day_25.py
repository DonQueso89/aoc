import day25
import pytest


@pytest.mark.parametrize("infile,output", [
    ("testinput25", 8),
    ("testinput25_1", 4),
    ("testinput25_2", 3),
    ("testinput25_3", 2),
])
def test__solve(infile, output):
    assert day25.solve(day25.prep_input(infile)) == output
