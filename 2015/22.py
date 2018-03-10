from copy import deepcopy 

"""

Objects: 
- Weapons 
- Warriors
- Spell 

Damage is at least 1 
Start mana = 500, no maximum
Effects that are already active can not be started
Effects can be started on the same turn that another one ends
First player at or below 0 hp loses

Day 1:
Least amount of mana spent and still win 
Day 2:
Extract 1 hp of player at start of each player turn.


"""
class Spell:
    def __init__(self, cost, timer, damage, mana_increase, heal, armor_increase, name, instant):
        self.cost = cost
        self.timer = timer
        self.damage = damage 
        self.mana_increase = mana_increase
        self.heal = heal
        self.armor_increase = armor_increase
        self.name = name
        self.is_active = False
        self.initial_timer = timer
        self.instant = instant
    
    def decrease_timer(self):
        self.timer -= 1
    
    def set_active(self, bool):
        self.is_active = bool
    
    def reset(self):
        self.timer = self.initial_timer
        self.is_active = False
    
    def display_stats(self):
        return "%s\nTimer: %s\nIs active: %s" % (self.name, self.timer, self.is_active)

# Boss has fixed damage, player uses spells with mana. 
class Warrior:
    def __init__(self, mana, hp, damage, armor):
        self.hp = hp 
        self.mana = mana
        self.damage = damage
        self.armor = armor
        self.mana_spent = 0
    
    def display_stats(self):
        return "hp: %d\nmana: %d\ndamage: %d\narmor: %d\n" % (self.hp, self.mana, self.damage, self.armor)
    
    def is_dead(self):
        return self.hp <= 0

"""
Base cases: 
- Boss is dead (append to mana_spent)
- Player is dead (do nothing)

Recursive case:
- Both players are still alive

Three objects are passed in the recursive call:
- Player (Warrior) 
- Boss (Warrior)
- Effects (Containing Spell objects)

- also: the next spell is passed if it is possible in the current state

"""

def turn(player, boss, effects, next_spell):
        
        print "PLAYER STATS"
        print player.display_stats()
        print "BOSS STATS"
        print boss.display_stats()
        for spell in effects.values():
            print spell.display_stats()
        
        # Cast next_spell. Execute if instant.
        spell = effects[next_spell]
        if spell.instant:
            boss.hp -= spell.damage
            player.hp += spell.heal
            player.mana -= spell.cost
            player.mana_spent += spell.cost
        else:
            spell.set_active(True)
            player.mana -= spell.cost
            player.mana_spent += spell.cost
            player.armor += spell.armor_increase

        # Check if boss is dead 
        if boss.is_dead():
            mana_spent.append(player.mana_spent)
            return True 

        # ---------------------------- BOSS TURN -------------------------- #
        # Apply effects 
        for effect in effects.values():
            if effect.is_active:
                player.mana += effect.mana_increase
                boss.hp -= effect.damage
                effect.decrease_timer()

        # Check if boss is dead 
        if boss.is_dead():
            mana_spent.append(player.mana_spent)
            return True

        # Clean up spells
        for effect in effects.values():
            if effect.timer == 0 and effect.is_active:
                effect.reset()
                player.armor -= effect.armor_increase

        # Boss attack 
        if player.armor - boss.damage >= 0:
            player.hp -= 1
        else:
            player.hp += (player.armor - boss.damage)

        # Check if player is dead 
        if player.is_dead():
            return False
            
        # ---------------------------- PLAYER TURN -------------------------- #
        
        player.hp -= 1
        if player.is_dead():
            return False
        
        # Apply effects
        for effect in effects.values():
            if effect.is_active:
                player.mana += effect.mana_increase
                boss.hp -= effect.damage
                effect.decrease_timer()
        
        
        # Check if boss is dead 
        if boss.is_dead():
            mana_spent.append(player.mana_spent)
            return True 
        
        # Clean up spells
        for effect in effects.values():
            if effect.timer == 0 and effect.is_active:
                effect.reset()
                player.armor -= effect.armor_increase
        
        for s in effects:
            if player.mana - effects[s].cost >= 0 and not (player.mana_spent >= min(mana_spent) or effects[s].is_active):
                # Recursive call(s) for all possible spells
                turn(deepcopy(player), deepcopy(boss), deepcopy(effects), s)
        # No spells possible: player loses.





# Instantiate Warriors. HP of player is decreased by 1 for the first turn on Day 2
player = Warrior(500, 49, 0, 0)
boss = Warrior(0, 51, 9, 0)

# Instantiate Spells. 0 timer means instant damage.
spell_dict = {"Magic missile": Spell(53, 0 , 4,  0, 0, 0, "Magic missile", True), 
              "Drain": Spell(73, 0, 2, 0, 2, 0, "Drain", True), 
              "Shield": Spell(113, 6, 0, 0, 0, 7, "Shield", False), 
              "Poison": Spell(173, 6, 3, 0, 0, 0, "Poison", False), 
              "Recharge": Spell(229, 5, 0, 101, 0, 0, "Recharge", False)};

# For day 1, initial minimum can be set to 1000.
mana_spent = [1500]

for spell in spell_dict:
    turn(deepcopy(player), deepcopy(boss), deepcopy(spell_dict), spell)

print "Least amount of mana spent: ", min(mana_spent)

