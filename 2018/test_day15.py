import pytest
import day15


@pytest.mark.parametrize("infile,output", [
    ("testinput15_1", 36334),
    ("testinput15_2", 39514),
    ("testinput15_3", 27755),
    ("testinput15_4", 28944),
    ("testinput15_5", 18740),
    ("testinput15_6", 27730),
])
def test__testinputs(infile, output):
    r = day15.solve(day15.prep_grid(infile))
    assert r[0] * r[1] == output

class A:
    pass
@pytest.mark.parametrize("infile,output", [
    ("testinput15_2", 31284),
    ("testinput15_3", 3478),
    ("testinput15_4", 6474),
])
def test__testinputs2(infile, output):
    a = A()
    a.infile = infile
    r = day15.solve2(a)
    assert r[0] * r[1] == output
