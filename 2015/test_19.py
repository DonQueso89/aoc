import day19


def test_19():
    assert day19.solve1(*day19.prep_data(open("testinput19").read())) == 4
    assert day19.solve1(*day19.prep_data(open("testinput19_1").read())) == 7
    assert day19.solve3(*day19.prep_data(open("testinput19p2_1").read())) == 3
    assert day19.solve3(*day19.prep_data(open("testinput19p2").read())) == 6
