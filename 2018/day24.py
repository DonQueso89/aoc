#!/usr/bin/env python
import argparse
import re
from collections import namedtuple

parser = argparse.ArgumentParser(description='Solve day 24')
parser.add_argument("infile", type=str)


IMMUNE_SYSTEM = 0
INFECTION = 1


class Group:
    def __init__(self, side, units, hp, attack_power, attack_type, initiative, weaknesses, immunities):
        self.side = side
        self.units = units
        self.hp = hp
        self.attack_power = attack_power
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def __str__(self):
        return f'<{self.side} units: {self.units} hp: {self.hp} weaknesses: {self.weaknesses} immunities: {self.immunities}>'

    def __repr__(self):
        return f'<{self.side} units: {self.units} hp: {self.hp} weaknesses: {self.weaknesses} immunities: {self.immunities}>'


def prep_data(data):
    groups = []
    data = data.splitlines()
    side = IMMUNE_SYSTEM
    for line in data[1:]:
        if not line:
            continue
        if 'Infection' in line:
            side = INFECTION
            continue
        n_units, hp, ap, initiative = [int(x) for x in re.findall('\d+', line)]
        at = re.match(r'.* ([a-z]+) damage .*', line).groups()[0]
        weaknesses = re.match(r'.*weak to ([a-z, ]+).*', line)
        if weaknesses:
            weaknesses = weaknesses.groups()[0]

        immunities = re.match(r'.*immune to ([a-z, ]+).*', line)
        if immunities:
            immunities = immunities.groups()[0]
        groups.append(
            Group(
                side,
                n_units,
                hp,
                ap,
                at,
                initiative,
                weaknesses if weaknesses else '',
                immunities if immunities else '',
            )
        )
    return groups


def damage(attacker, defender):
    """
    default = effective power
    weak = effective power * 2
    immune = effective power * 0
    """
    effective_power = attacker.units * attacker.attack_power
    if attacker.attack_type in defender.weaknesses:
        return effective_power * 2
    if attacker.attack_type in defender.immunities:
        return 0
    return effective_power


def solve(groups):
    immune_system = set([x for x in groups if x.side == IMMUNE_SYSTEM])
    infection = set([x for x in groups if x.side == INFECTION])
    while True:
        attack_map = {}
        # target selection: decreasing order of effective power / initiative
        groups = sorted(
            groups,
            key=lambda k: (-k.units * k.attack_power, -k.initiative)
        )
        for attacker in groups:
            # choose target of max(damage_dealt, effective_power, initiative)
            defending = immune_system if attacker.side == INFECTION else infection
            try:
                defender = sorted(
                    defending,
                    key=lambda k: (
                        damage(attacker, k),
                        k.units * k.attack_power,
                        k.initiative)
                )[-1]
                if damage(attacker, defender) == 0:
                    continue
                attack_map[attacker] = defender
                defending -= set([defender])
            except IndexError:
                continue

        for attacker in sorted(groups, key=lambda k: -k.initiative):
            target = attack_map.get(attacker)
            if target:
                target.units = max(target.units - (damage(attacker, target) // target.hp), 0)

        groups = [x for x in groups if x.units > 0]
        immune_system = set([x for x in groups if x.side == IMMUNE_SYSTEM])
        infection = set([x for x in groups if x.side == INFECTION])

        if not immune_system or not infection:
            return groups
    return 0


def solve2(data):
    boost = 1
    while True:
        groups = prep_data(data)
        for g in groups:
            if g.side == IMMUNE_SYSTEM:
                g.attack_power += boost
        result = solve(groups)
        if result[0].side == IMMUNE_SYSTEM:
            return sum([x.units for x in result])
        boost += 1


if __name__ == '__main__':
    args = parser.parse_args()
    data = open(args.infile).read()
    _data = prep_data(data)
    print("Part 1: {:d}".format(sum([x.units for x in solve(_data)])))
    print("Part 2: {:d}".format(solve2(data)))
