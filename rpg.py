from random import randint

class Attack:
  def __init__(self,name,damage,crit,miss):
    self.name = name
    self.damage = damage
    self.crit = crit
    self.miss = miss

  def calculate_damage(self):
    r = randint(0,100)
    if r < self.crit:
      return self.damage * 2
    r = randint(0,100)
    if r < self.miss:
      return 0

    return self.damage

class Item :
  def __init__(self,name):
    self.name = name

  def use(self, Entity):
    print("Vous utilisez :", self.name)

class Potion(Item) :
  def __init__(self,name,effect,power):
    super().__init__(name)
    self.effect = effect
    self.power = power

  def use(self, player):
    if self.effect == "Soin":
      player.hp += self.power
    elif self.effect == "Def":
      player.Def += self.power

class Weapon(Item) :
  def __init__(self,name,atk):
    super().__init__(name)
    self.atk = atk

  def use(self,player):
    player.atks.append(self.atk)

class Entity():
  def __init__(self,name, atks, Def, hp ):
    self.name = name
    self.atks = atks
    self.Def = Def
    self.hp = hp

  def attack(self):
    pass

class Location:
  def __init__(self, name):
    self.name = name
    self.monsters = []
    self.items = []

  def add_monster(self, monster):
    self.monsters.append(monster)

  def add_item(self, item):
    self.items.append(item)

class Forest(Location):
  def __init__(self):
    super().__init__("Forêt")
    self.add_monster(monster("Loup", [Attack("Morsure", 1, 1, 1)], 1, 10, None))

class Castle(Location):
  def __init__(self):
    super().__init__("Château")
    self.add_monster(monster("Garde", [Attack("Coup d'épée", 5, 5, 5)], 5, 20, None))
    self.add_item(Weapon("Épée", Attack("Coup d'épée", 5, 20, 0)))

class House(Location):
  def __init__(self):
    super().__init__("Maison")
    self.add_item(Potion("Potion de vie puissante", "Soin", 25))
    self.add_item(Potion("Potion de vie puissante", "Soin", 25))
    self.add_item(Potion("Potion de défense", "Def", 10))
    self.add_item(Weapon("Dague", Attack("Coup de dague", 3, 10, 0)))

class PlayerRPG(Entity):
  def __init__(self,Role):
    if Role == "Warrior":
      super().__init__(Role,[Attack("Epee",1,5,5),Attack("Hache",20,20,40)],5,20)
      self.inventory = [Potion("Potion de vie","Soin",15)]
    elif Role == "Mage":
      super().__init__(Role,[Attack("Boule de feu",40,5,30),Attack("Eclair",20,20,40)],3,15)
      self.inventory =[Potion("Potion de Soin","Soin",20),Weapon("Baton",Attack("Boule de feu",5,20,0)),Potion("Potion de Defense","Defense",10),Potion("Potion de Defense","Defense",10)]

  def use_inventory(self):
    self.open_inventory()
    choose = int(input())
    p = self.inventory[choose]
    p.use(self)
    self.inventory.remove(p)

  def attack(self):
    for element in self.atks:
      print(element.name)
    choose = int(input())
    return self.atks[choose].calculate_damage()

  def open_inventory (self):
    for item in self.inventory:
      print(item.name)

  def move(self, new_location):
    self.location = new_location
    print(f"Vous vous déplacez vers {new_location.name}.")

class monster(Entity) :
  def __init__(self, name, atks, Def, hp, loot):
    super().__init__(name,atks,Def,hp)
    self.loot = loot

  def attack(self):
    r = randint(0,len(self.atks)-1)
    atk = self.atks[r]
    return atk.calculate_damage()

def Fight(Player,Monster):
  while Player.hp > 0 and Monster.hp > 0:
    print(f"Le monstre a {Monster.hp} points de vie.")
    choose = input("Atk or item")
    if choose == "Atk":
      Monster.hp -= Player.attack()
    elif len(Player.inventory) > 0:
      Player.use_inventory()

    Player.hp -= Monster.attack()

  #Réinitialise la vie du monstre après le combat
  if Monster.hp <= 0:
    print(f"Le {Monster.name} est mort.")
    Monster.hp = 25

def jeu(Player):
  forest = Forest()
  castle = Castle()
  house = House()
  locations = [forest, castle, house]

  while Player.hp > 0:
    location_index = randint(0, len(locations) - 1)
    location = locations[location_index]
    Player.move(location)
    if location.monsters:
      monster_index = randint(0, len(location.monsters) - 1)
      monster = location.monsters[monster_index]
      print(f"Un {monster.name} vous attaque !")
      Fight(Player, monster)
    elif location.items:
      item_index = randint(0, len(location.items) - 1)
      item = location.items[item_index]
      Player.inventory.append(item)
      print(f"Vous avez trouvé {item.name} et l'avez ajouté à votre inventaire.")
    if Player.hp > 0:
      print("Vous avez survécu à cette zone. Le jeu continue...")
    else:
      print("Vous êtes mort. Vous avez perdu.")

Pl = PlayerRPG("Warrior")

jeu(Pl)