# class Location:
#     def __init__(self, name, options):
#         self.name = name
#         self.options = options

from random import randint

class Site:
    def __init__(self, name, structures=[], enemies=[], can_plant_bomb=False):
        self.name = name
        self.enemies = enemies
        self.can_be_surveyed_count = 2
        self.structures = structures
        self.structures_been_surveyed = False
        self.enemies_been_surveyed = False
        self.can_plant_bomb = can_plant_bomb

    def survey_structures(self):
        structure_names = ""
        for structure in self.structures:
            structure_names += structure.name + ", "
        structure_names = structure_names.rstrip(", ")
        print(f"Structures in sight: {structure_names}")

        #Player sees the structures around him
        player.structures_in_sight = self.structures

        while True:
            try:
                structure_chosen = input("""
Pick a structure to hide behind by entering the name of the structure to be chosen (enter "None" to select nothing): """
                                         ).upper()

                #player didn't choose any
                if structure_chosen == "NONE":
                    print(f"You didn't select any structures to hide behind")
                    break
                #if the player did choose something
                for structure in self.structures:
                    if structure.name == structure_chosen:
                        player.structure_selected = structure
                        break
                else:
                    raise ValueError
            except ValueError:
                print("Enter a valid input. You can only choose one of the structures listed")
            else:
                break

        for structure in self.structures:
            if structure.name == structure_chosen:
                player.structure_selected = structure
                print(f"You've selected {player.structure_selected.name}. It provides the protection of "
                      f"{player.structure_selected.protection * 100}%")
                break

    def survey_enemies(self):
        #the order is riflers-heavy_inf-snipers
        for enemy_group in self.enemies:
            print(f"There are {len(enemy_group)} {enemy_group[0].__class__.__name__}s")

        for enemy_group in self.enemies:
            for enemy in enemy_group:
                enemy.print_essential_info()

        #player spots the enemies
        in_sight_enemies = []
        for enemy_group in self.enemies:
            in_sight_enemies.extend(enemy_group)
        player.enemies_in_sight = in_sight_enemies

class Player:
    def __init__(self):
        self.alive = True
        self.current_site = None
        self.in_combat = False
        self.rounds_won = 0
        self.structure_selected = None
        self.structures_in_sight = []
        self.enemies_in_sight = []
        self.enemy_selected = None
        self.weapon_selected = None
        self.is_random_firing = False

    # functions related to the Phases
    def carry_out_reconnaissance(self):
        while True:
            try:
                choice = eval(input(f"Choose one of the options: \n1. Look for structures to utilize"
                                    f"\n2. Get information on enemies' composition"
                                    ))
                if choice == 1:
                    self.current_site.survey_structures()
                elif choice == 2:
                    self.current_site.survey_enemies()
                else:
                    raise ValueError
            except SyntaxError:
                print("Enter a valid number. Only the numbers 1 and 2 are valid inputs")
            except ValueError:
                print("Enter a valid number. Only the numbers 1 and 2 are valid inputs")
            else:
                player.in_combat = True
                break

    def carry_out_combat(self):
        #show the enemies that can be attacked
        if len(player.enemies_in_sight) > 0:
            self.show_enemies_in_sight()
            self.pick_enemy_to_attack()
        else:
            print("You have no enemies in sight as of now")
            #random firing
            while True:
                do_random_firing = input("Would you carry out random-firing? Accuracy will be somewhat dropped (Y/N)").upper()
                if do_random_firing == "Y":
                    self.is_random_firing = True
                    self.pick_weapon()
                    self.random_fire()
                    break
                elif do_random_firing == "N":
                    break
                else:
                    print("The input can only be either Y or N. Enter a valid input: ")

        #determine number of bullets to be fired
        if player.enemy_selected is not None:
            self.pick_weapon()
            bullets_fired_count = self.pick_bullets()
            if isinstance(player.weapon_selected, Gun):
                self.attack_with_gun(bullets_fired_count)


    def show_enemies_in_sight(self):
        for enemy in player.enemies_in_sight:
            print(enemy.name)

    def pick_enemy_to_attack(self):
        while True:
            try:
                enemy_selected = input("Pick an enemy to attack by entering his name (ignore this stage by entering "
                                       "None: ")
                if enemy_selected == "None":
                    break

                for enemy in player.enemies_in_sight:
                    if enemy.name == enemy_selected:
                        enemy.print_essential_info()
                        player.enemy_selected = enemy
                        break
                else:
                    raise ValueError
            except ValueError:
                print("Enter a valid input. Match one of the names shown below or enter None")
                self.show_enemies_in_sight()
            else:
                break


    def pick_weapon(self):
        inventory.show_inventory()

        loop = True
        while loop:
            weapon_picked = input("Choose a weapon to use by entering its classfication (i.e. primary-weapon, utility: ")
            for key, value in vars(inventory).items():
                if weapon_picked == key:
                    player.weapon_selected = value
                    loop = False
            if player.weapon_selected is None:
                print("Enter a valid input")


    def pick_bullets(self):
        if player.weapon_selected is not "utility":
            while True:
                try:
                    bullets_count = eval(input("How many bullets will you fire?"))
                    if isinstance(bullets_count, int) and 0 < bullets_count <= player.weapon_selected.bullet_count:
                        return bullets_count
                        break
                    else:
                        raise ValueError
                except SyntaxError:
                    print(f"enter a number bigger than 0 and smaller than or equal to {player.weapon_selected.bullet_count}")
                except ValueError:
                    print(f"enter a number bigger than 0 and smaller than or equal to {player.weapon_selected.bullet_count}")

    def attack_with_gun(self, bullets_fired):
        weapon = player.weapon_selected
        damage_dealt = calculate_damage_by_player(weapon.damage, weapon.accuracy, bullets_fired)
        player.enemy_selected.health -= damage_dealt
        player.weapon_selected.bullet_count -= bullets_fired

        if player.enemy_selected.health <= 0:
            print(f"Bang!!! You have killed {player.enemy_selected.name}")
            player.enemy_selected.is_alive = False
            player.enemy_selected = None
        else:
            print(f"You have inflicted {damage_dealt} amount of damage on {player.enemy_selected.name}")
            player.enemy_selected = None

    def random_fire(self):
        for enemy in player.current_site.enemies:
            if enemy.is_alive:
                weapon = player.weapon_selected
                bullets_fired = randint(0, weapon.bullet_count)
                weapon.bullet_count -= bullets_fired
                total_damage = calculate_damage_by_player(weapon.damage, weapon.accuracy, bullets_fired)
                enemy.health -= total_damage

                if enemy.health > 0:
                    print(f"{enemy.name} has taken {total_damage} amount of damage\nhe has {enemy.health} health remaining")
                else:
                    print(f"{enemy.name} is killed and has taken {total_damage} amount of damage")

        print(f"You have {player.weapon_selected.bullet_count} bullets remaining for {player.weapon_selected.name}")

    def move_to_next_site(self):
        pass

class Enemy:
    def __init__(self, weapon, gun_type="rifle", armor_type="light-armored", distance=3):
        global enemy_count

        self.is_alive = True
        self.health = 100
        self.name = "Enemy " + str(enemy_count)
        self.weapon = weapon
        self.gun_type = gun_type
        self.armor_type = armor_type
        self.distance_from_player = distance

        enemy_count += 1

    def print_essential_info(self):
        enemy_info = vars(self)
        # del enemy_info[self.weapon]

        print(self.name)
        for key, value in enemy_info.items():
            print(f"{key}: {value}")

        print("\n")


class Rifler(Enemy):
    def __init__(self, standard_distance):
        Enemy.__init__(self, Gun("Default Enemy Gun"))
        self.distance_from_player = standard_distance


class Troll(Enemy):
    def __init__(self, standard_distance):
        Enemy.__init__(self, Gun("Default Enemy Gun"))
        #Heavy infantries are in front of riflers
        self.distance_from_player = standard_distance - 1


class Sniper(Enemy):
    def __init__(self, standard_distance):
        Enemy.__init__(self, Gun("Default Enemy Gun"))
        #snipers are behind riflers
        self.distance_from_player = standard_distance + 2


class Gun:
    def __init__(self, name, capacity=30, damage=10, accuracy=0.2, is_shotgun=False):
        self.name = name
        self.capacity = capacity
        self.bullet_count = self.capacity
        self.damage = damage
        self.accuracy = accuracy
        self.is_shotgun = is_shotgun


class Utility:
    def __init__(self, damage, accuracy_drop):
        self.damage = damage
        self.accuracy_drop = accuracy_drop

    def deal_damage_molotov(self):
        #incendiary bomb-- recursion
        pass

class Inventory:
    def __init__(self, primary_weapon=Gun("Default Rifle"), secondary_weapon=Gun("Defualt Pistol"), utility=[]):
        self.primary_weapon = primary_weapon
        self.secondary_weapon = secondary_weapon
        self.utility = utility

    def show_inventory(self):
        inventory = vars(self)
        for value, key in inventory.items():
            print("{value}: {key}".format(value=value, key=key))


class Structures:
    def __init__(self, name="structure", protection=0.3, sniping_protection=0.1):
        self.name = name
        self.protection = protection
        self.sniping_protection = sniping_protection


# global variables
player = Player()
inventory = Inventory()
enemy_count = 1

debug = True
should_loop_phases = True


def instantiate_enemies(riflers_count, heavy_inf_count, snipers_count, standard_distance=3):
    enemies = []

    riflers = [Rifler(standard_distance=standard_distance) for i in range(riflers_count)]
    heavy_inf = [Troll(standard_distance=standard_distance) for i in range(heavy_inf_count)]
    snipers = [Sniper(standard_distance=standard_distance) for i in range(snipers_count)]

    enemies.extend(riflers)
    enemies.extend(heavy_inf)
    enemies.extend(snipers)

    return enemies


def start_game():
    # James is going to make a text file for introduction
    print("Welcome to Counter Strike: Text Offensive")
    print("Your decisions will decide the result of the rounds and decide whether you live or die.")
    print("Be mindful of the equipment you bring into battle, It will decide the outcomes in some situations.")
    print("May the odds be ever in your favor.")
    dramaticpause = input("     Press 'Enter' to Start")


def buy_function():
    print("")
    print("Opening Buy Menu.....")

    def select_primary():
        print("----------------------------------------------------------------------------------")
        print("                        Primary Weapon Menu           ")
        print("----------------------------------------------------------------------------------")
        print("(1)  AK-47  //  Rifle          //  30 Rounds // Range: Medium")
        print("(2)  SG-553 //  Scoped Rifle  //  30 Rounds // Range: Medium - Long")
        print("(3)  UMP-45 //  SMG          //  25 Rounds // Range: Close")
        print("(4)  AWP    //  Sniper      //  10 Rounds // Range: Long")
        print("(5)  None")
        print("     Refer to User Manual for detailed weapon descriptions.")
        print("")

        while True:
            try:
                primaryselect = eval(input("Please select a Primary Weapon (1 - 5): "))

                if primaryselect == 1:
                    primaryweapon = "AK-47"
                    break
                elif primaryselect == 2:
                    primaryweapon = "SG-553"
                    break
                elif primaryselect == 3:
                    primaryweapon = "UMP-45"
                    break
                elif primaryselect == 4:
                    primaryweapon = "AWP"
                    break
                elif primaryselect == 5:
                    primaryweapon = "None"
                    break
                else:
                    print("Try Again, Select (1 - 5)")
            except SyntaxError:
                print("Try Again, Select (1 - 5)")
            except NameError:
                print("Try Again, Select (1 - 5)")
        return primaryweapon

    def select_secondary():
        print("----------------------------------------------------------------------------------")
        print("                        Secondary Weapon Menu           ")
        print("----------------------------------------------------------------------------------")
        print("(1)  Glock        //  Sidearm           //  20 Rounds // Range: Close")
        print("(2)  P250         //  Sidearm          //  13 Rounds // Range: Medium")
        print("(3)  Desert Eagle //  Hand Cannon     //  7 Rounds  // Range: Medium - Long")
        print("(4)  CZ-75 Auto   //  Machine Pistol //  13 Rounds // Range: Close")
        print("     Refer to User Manual for detailed weapon descriptions.")
        print("")

        while True:
            try:
                secondaryselect = eval(input("Please select a Secondary Weapon (1 - 4): "))

                if secondaryselect == 1:
                    secondaryweapon = "Glock"
                    break
                elif secondaryselect == 2:
                    secondaryweapon = "P250"
                    break
                elif secondaryselect == 3:
                    secondaryweapon = "Desert Eagle"
                    break
                elif secondaryselect == 4:
                    secondaryweapon = "CZ-75 Auto"
                    break
                else:
                    print("Try Again, Select (1 - 4)")
            except SyntaxError:
                print("Try Again, Select (1 - 4)")
            except NameError:
                print("Try Again, Select (1 - 4)")

        return secondaryweapon

    def utility_select():
        utilitylist = []
        print("")
        print("----------------------------------------------------------------------------------")
        print("                                Utility Menu                                      ")
        print("     Utility is very useful to help aim duels and other combat situations go in your favor.  ")
        print("     You can carry up to 4 grenades")
        print("----------------------------------------------------------------------------------")
        print("(1)  Flashbang      || Grenade that blinds enemies for a short period of time.")
        print("(2)  Smoke Grenade  || Grenade that covers an area in smoke for a period of time.")
        print("(3)  Molotov        || Grenade that covers the ground in fire for a short period of time.")
        print("(4)  HE Grenade     || Grenade that damages enemies within blast radius")
        print("(5)  Exit Utility Menu")
        print("")

        count = 4
        while count > 0:
            print(count, "inventory slots remaining.")
            utilityselect = eval(input("Please select your Utility: "))
            print("")

            if utilityselect == 1:
                utilitylist.append("Flashbang")
                count -= 1
            elif utilityselect == 2:
                utilitylist.append("Smoke Grenade")
                count -= 1
            elif utilityselect == 3:
                utilitylist.append("Molotov")
                count -= 1
            elif utilityselect == 4:
                utilitylist.append("HE Grenade")
                count -= 1
            elif utilityselect == 5:
                count -= 4
        return utilitylist

    primaryweapon = select_primary()
    secondaryweapon = select_secondary()
    utility = utility_select()
    playerinventory = Inventory(primaryweapon, secondaryweapon, utility)
    print("Buy phase complete.... round starting")
    print("----------------------------------------------------------------------------------")
    return playerinventory


def find_index_of_elem(elem, a_list):
    for index, item in enumerate(a_list):
        if elem == item:
            return index

    return None


def calculate_damage_by_player(weapon_damage, accuracy, bullets_fired):
    accuracy_percentage = accuracy * 100
    bullets_hit = 0
    if player.is_random_firing:
        accuracy_percentage = accuracy_percentage * 0.8

    for i in range(bullets_fired):
        if randint(1, 100) < accuracy_percentage:
            print(f"Bang!!! Someone is hit")
            bullets_hit += 1
        else:
            print(f"Bullet didn't land on anything!")

    return weapon_damage * bullets_hit


def main():
    ###create instances###
    rock = Structures(name="ROCK", protection=0.6, sniping_protection=0.2)
    pillar = Structures(name="PILLAR", protection=0, sniping_protection=0.7)

    ###guns##

    #rifles
    AK47 = Gun(name="AK-47", capacity=30, damage=27, accuracy=0.8, is_shotgun=False)
    SG553 = Gun(name="SG-553", capacity=30, damage=30, accuracy=0.7, is_shotgun=False)
    UMP45 = Gun(name="UMP-45", capacity=25, damage=22, accuracy=0.9, is_shotgun=False)

    #sniper rfles#
    AWP = Gun(name="AWP", capacity=10, damage=112, accuracy=0.95, is_shotgun=False)

    #shot-guns
    sawed_off = Gun(name="Sawed Off", capacity=7, damage=24, accuracy=0.5, is_shotgun=True)

    #pistols
    Glock_18 = Gun(name="Glock-18", capacity=20, damage=13, accuracy=0.7, is_shotgun=False)
    P250 = Gun(name="P250", capacity=13, damage=24, accuracy=0.6, is_shotgun=False)
    CZ75_auto = Gun(name="CZ-75 Auto", capacity=12, damage=23, accuracy=0.5, is_shotgun=False)
    Desert_Eagle = Gun(name="Desert Eagle", capacity=7, damage=58, accuracy=.75, is_shotgun=False)

    #Utility

    # sites
    enemies_t_spawn = instantiate_enemies(riflers_count=2, heavy_inf_count=1, snipers_count=1, standard_distance=3)
    t_spawn = Site(name="T Spawn", structures=[rock, pillar], enemies=enemies_t_spawn)
    outside_long = Site(name="Outside Long")
    a_long = Site(name="A Long")
    a_site = Site(name="A Site")
    top_mid = Site(name="Top-Mid")
    bottom_mid = Site(name="Bottom-Mid")
    tunnels = Site(name="Tunnels")
    b_site = Site(name="B Site")

    map = [outside_long, tunnels]
    outside_long = [a_long, top_mid]
    tunnels = [b_site, bottom_mid]
    a_long = [a_site]
    top_mid = [bottom_mid]
    bottom_mid = [b_site, a_site]

    # Initial phase
    # start_Game()
    # buy_Function()

    """
    the recurring phases of the game: reconnaissance, combat, moving, enemies' turn
    
    reconnaissance: Every time the player enters a new site, he can survey the area to get useful information, such as
    the number of enemies and their types, so he can plan ahead accordingly
    
    Combat: Literally, a combat between the player and enemies. They take turns shooting and moving around. Player has
    to make decisions as to how many bullets to fire or whether to move out of position or not
    
    Moving: When the combat is over, the player may proceed to other connected sites
    
    Enemies turn: when the player's turn is over, enemies take action
    """

    # player starting pos initialization
    player.current_site = t_spawn
    inventory.primary_weapon = AK47

    # for loop for a total of 7 rounds
    while player.rounds_won < 4:
        # phases
        while should_loop_phases:
            if player.current_site.can_be_surveyed_count > 0:
                player.carry_out_reconnaissance()
                player.current_site.can_be_surveyed_count -= 1

            if player.in_combat:
                player.carry_out_combat()
                #enemy turn

            if not player.in_combat:
                player.move_to_next_site()

            # the breaks below are temporary
            break
        break

    input()
main()
