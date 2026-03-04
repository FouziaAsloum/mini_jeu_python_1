import random
import json

# ===== PLAYER CLASS =====
class Player:
  def __init__(self, name, player_class):
    self.name = name
    self.player_class = player_class

    # Stats de base
    self.level = 1
    self.xp = 0
    self.gold = 0
    self.potions = 2

    # Stats selon la classe
    if player_class == "Guerrier":
      self.max_health = 120
      self.attack = 18
      self.defense = 8
      self.mana = 0

    elif player_class == "Mage":
      self.max_health = 80
      self.attack = 10
      self.defense = 3
      self.mana = 50

    elif player_class == "Assassin":
      self.max_health = 90
      self.attack = 15
      self.defense = 4
      self.mana = 20

    self.health = self.max_health
    
    self.weapon = {
    "name": "Épée rouillée 🗡️",
    "attack_bonus": 2
    }
    
    self.zone = "Forêt 🌲"


  def show_stats(self):
    print("\n===== PLAYER STATS =====")
    print(f"Name: {self.name}")
    print(f"Class: {self.player_class}")
    print(f"Level: {self.level}")
    print(f"XP: {self.xp}/100")
    print(f"Health: {self.health}/{self.max_health}")
    print(f"Attack: {self.attack}")
    print(f"Defense: {self.defense}")
    print(f"Gold: {self.gold}")
    print(f"Potions: {self.potions}")
    if self.mana > 0:
     print(f"Mana: {self.mana}")
    print("========================\n")


# ----- TAKE DAMAGE -----
  def take_damage(self, damage):
    self.health -= damage
    self.health = max(0, self.health)


# ----- ATTACK ENEMY -----
  def attack_enemy(self, enemy):
    crit = random.random() < 0.2  # 20% chance critique
    total_attack = self.attack + self.weapon["attack_bonus"]
    base_damage = random.randint(total_attack - 3, total_attack + 3)
    damage = base_damage - enemy.defense

    if crit:
        damage *= 2
        print("💥 CRITICAL HIT!")

    damage = max(0, damage)
    enemy.take_damage(damage)
    
    print(f"{self.name} attacks {enemy.name} for {damage} damage!")
    
    
# ----- SPECIAL ABILITY -----
  def special_ability(self, enemy):
    print("\n✨ SPECIAL ABILITY ✨")

    # ===== warrior =====
    if self.player_class == "Guerrier":
      damage = (self.attack + self.weapon["attack_bonus"]) * 2
      damage -= enemy.defense
      damage = max(0, damage)

      enemy.take_damage(damage)
      print(f"💥 Coup Puissant ! {damage} damage dealt!")

      if random.random() < 0.25:
        print("⚡ L'ennemi est étourdi !")
        return "stun"

    # ===== wizard =====
    elif self.player_class == "Mage":
      if self.mana >= 20:
        self.mana -= 20
        damage = random.randint(25, 35)
        enemy.take_damage(damage)
        print(f"🔥 Boule de Feu ! {damage} damage dealt!")
      else:
        print("❌ Pas assez de mana !")

    # ===== murderer =====
    elif self.player_class == "Assassin":
      damage = (self.attack + self.weapon["attack_bonus"]) * 2
      enemy.take_damage(damage)
      print(f"🗡 Attaque Furtive ! {damage} damage dealt!")

      if random.random() < 0.3:
        print("💨 Vous évitez la prochaine attaque !")
        return "dodge"

    return None
 


# ----- USE POTION -----
  def use_potion(self):
    if self.potions > 0:
      heal = 30
      before = self.health
      self.health = min(self.max_health, self.health + heal)
      actual_heal = self.health - before
      self.potions -= 1
      print(f"{self.name} drinks a potion and heals {actual_heal} HP!")
    
    else:
      print("No potions left!")

  def gain_xp(self, amount):
    self.xp += amount
    print(f"You gained {amount} XP!")

    while self.xp >= 100:
      self.xp -= 100
      self.level_up()

  def level_up(self):
    self.level += 1
    self.max_health += 20
    self.attack += 5
    self.defense += 2
    self.health = self.max_health
    print("🎉 LEVEL UP!")
    print(f"You are now level {self.level}!")


# ==============================
#            ENEMY
# ==============================

class Enemy:
  def __init__(self, name, health, attack, defense, xp_reward, gold_reward):
    self.name = name
    self.health = health
    self.attack = attack
    self.defense = defense
    self.xp_reward = xp_reward
    self.gold_reward = gold_reward
    
  def take_damage(self, damage):
    self.health -= damage
    self.health = max(0, self.health)

  def attack_player(self, player):
    base_damage = random.randint(self.attack - 2, self.attack + 2)
    damage = base_damage - player.defense
    damage = max(0, damage)
    
    player.take_damage(damage)
    print(f"{self.name} attacks {player.name} for {damage} damage!")


# ===== ENEMY GENERATOR =====
def generate_enemy(player):
  level = player.level
  zone = player.zone  # ✅ On récupère la zone actuelle

  enemy_types = [
    {"name": "Goblin 👹", "base_health": 50, "base_attack": 8, "base_defense": 2},
    {"name": "Orc 💪", "base_health": 80, "base_attack": 12, "base_defense": 4},
    {"name": "Skeleton 💀", "base_health": 60, "base_attack": 10, "base_defense": 3}
    ]

  enemy_choice = random.choice(enemy_types)

# ✅ Multiplicateur selon la zone
  if zone == "Forêt 🌲":
    multiplier = 1
  elif zone == "Donjon 🏰":
    multiplier = 1.5
  else:
    multiplier = 2

# ✅ Calcul des stats avec scaling zone + level
  health = int((enemy_choice["base_health"] + level * 10) * multiplier)
  attack = int((enemy_choice["base_attack"] + level * 2) * multiplier)
  defense = int((enemy_choice["base_defense"] + level) * multiplier)

  xp_reward = int((30 + level * 10) * multiplier)
  gold_reward = int((15 + level * 5) * multiplier)

  return Enemy(
    enemy_choice["name"],
    health,
    attack,
    defense,
    xp_reward,
    gold_reward
  )

  
  
# ===== BOSS GENERATOR =====
def generate_boss():
  return Enemy("Dragon 🐉", 200, 20, 8, 150, 100)


# ===== COMBAT SYSTEM =====
def combat(player, enemy):
  print(f"\n⚔️ A wild {enemy.name} appears!")

  dodge_next = False  # Pour l'assassin

  while enemy.health > 0 and player.health > 0:
    print(f"\n{player.name}: {player.health} HP")
    print(f"{enemy.name}: {enemy.health} HP")

    print("1. Attack")
    print("2. Use Potion")
    print("3. Special Ability")

    action = input("Choose action: ")

    if action == "1":
      player.attack_enemy(enemy)

    elif action == "2":
      player.use_potion()

    elif action == "3":
      effect = player.special_ability(enemy)

      if effect == "stun":
        continue  # L’ennemi ne joue pas

      if effect == "dodge":
        dodge_next = True

    else:
      print("Invalid action.")
      continue

    # ----- TOUR ENNEMI -----
    if enemy.health > 0:

      if dodge_next:
        print("💨 Vous esquivez l'attaque ennemie !")
        dodge_next = False
      else:
        enemy.attack_player(player)

  # ----- FIN DU COMBAT -----
  if player.health > 0:
    print(f"\n✅ {enemy.name} defeated!")
    player.gold += enemy.gold_reward
    player.gain_xp(enemy.xp_reward)
    print(f"You gained {enemy.gold_reward} gold!")
  else:
    print("\n💀 You were defeated...")
    return False

  return True


# ===== CHANGE ZONE  =====
def change_zone(player):
  zones = {
    "1": "Forêt 🌲",
    "2": "Donjon 🏰",
    "3": "Montagne ⛰️"
  }

  print("\n🗺️ Choisis une zone :")
  for key, value in zones.items():
    print(f"{key}. {value}")

  choice = input("Zone : ")

  if choice in zones:
    player.zone = zones[choice]
    print(f"\n✅ Tu es maintenant dans : {player.zone}")


# ===== SHOP =====
def shop(player):
  while True:
    print("\n🏪 Welcome to the Shop!")
    print("1. Buy Potion (20 gold)")
    print("2. Increase Attack (+3) (50 gold)")
    print("3. Increase Defense (+2) (50 gold)")
    print("4. Exit Shop")

    choice = input("What do you want to buy? ")

    if choice == "1":
      if player.gold >= 20:
        player.gold -= 20
        player.potions += 1
        print("You bought a potion! 🧪")
      else:
        print("Not enough gold!")

    elif choice == "2":
      if player.gold >= 50:
        player.gold -= 50
        player.attack += 3
        print("Attack increased! 🗡️")
      else:
        print("Not enough gold!")

    elif choice == "3":
      if player.gold >= 50:
        player.gold -= 50
        player.defense += 2
        print("Defense increased! 🛡️")
      else:
        print("Not enough gold!")

    elif choice == "4":
      break

    else:
      print("Invalid choice.")
      
  
# ===== WEAPON SHOP =====     
def weapon_shop(player):
  weapons = [
    {"name": "Épée en fer ⚔️", "attack_bonus": 5, "price": 50},
    {"name": "Grande hache 🪓", "attack_bonus": 8, "price": 100},
    {"name": "Lame légendaire 🔥", "attack_bonus": 15, "price": 250}
  ]

  print("\n🛒 Boutique d'armes :")
  for i, weapon in enumerate(weapons):
    print(f"{i+1}. {weapon['name']} (+{weapon['attack_bonus']} ATK) - {weapon['price']} or")

  choice = input("Choisis une arme (ou 0 pour quitter) : ")

  if choice.isdigit():
    choice = int(choice)

    if choice == 0:
      return

    if 1 <= choice <= len(weapons):
      selected = weapons[choice - 1]

      if player.gold >= selected["price"]:
          player.gold -= selected["price"]
          player.weapon = {
            "name": selected["name"],
            "attack_bonus": selected["attack_bonus"]
           }
          print(f"\n✅ Tu as équipé {selected['name']} !")
      else:
          print("❌ Pas assez d'or.")


# ===== SAVE GAME PLAYER =====     
def save_game(player):
  data = {
    "name": player.name,
    "level": player.level,
    "xp": player.xp,
    "health": player.health,
    "max_health": player.max_health,
    "attack": player.attack,
    "defense": player.defense,
    "gold": player.gold,
    "potions": player.potions,
    "zone": player.zone,
    "weapon": player.weapon,
    "player_class": player.player_class
    }

  with open("save.json", "w") as file:
    json.dump(data, file, indent=4)

  print("💾 Game saved successfully!")
  
  
# ===== LOAD GAME ===== 
def load_game():
  try:
    with open("save.json", "r") as file:
      data = json.load(file)

      player = Player(
        data["name"],
        data.get("player_class", "Guerrier")
        )
      player.level = data["level"]
      player.xp = data["xp"]
      player.health = data["health"]
      player.max_health = data["max_health"]
      player.attack = data["attack"]
      player.defense = data["defense"]
      player.gold = data["gold"]
      player.potions = data["potions"]
      player.zone = data["zone"]
      player.weapon = data["weapon"]


      print("✅ Game loaded successfully!")
      return player

  except FileNotFoundError:
    print("⚠️ No save file found.")
    return None
  
  except json.JSONDecodeError:
    print("⚠️ Save file corrupted.")
    return None




# ===== MENU =====
def show_menu():
  print("\n=== MAIN MENU ===")
  print("1. Explore")
  print("2. Show Player Stats")
  print("3. Changer de zone")
  print("4. Shop")
  print("5. Boutique d'armes")
  print("6. Save Game")
  print("7. Load Game")
  print("8. Quit")





# ===== MAIN FUNCTION =====
def main():
  print("Welcome to the Ultimate Adventure Game 🗡️")

  player = None

  while player is None:
    print("1. New Game")
    print("2. Load Game")
    start_choice = input("Choose an option: ")

    if start_choice == "1":
      player_name = input("Choose your name: ")
      print("\nChoose your class:")
      print("1. Guerrier")
      print("2. Mage")
      print("3. Assassin")

      class_choice = input("Class: ")

      if class_choice == "1":
        player_class = "Guerrier"
      elif class_choice == "2":
        player_class = "Mage"
      elif class_choice == "3":
        player_class = "Assassin"
      else:
        print("Invalid choice, Guerrier selected by default.")
        player_class = "Guerrier"

      player = Player(player_name, player_class)
    
    elif start_choice == "2":
      player = load_game()
    else:
      print("Invalid choice.")

  while True:
    if player.health <= 0:
      print("Game Over.")
      break

    show_menu()
    choice = input("What do you want to do? ")

    if choice == "1":
      if random.random() < 0.2:   # 20% chance
        enemy = generate_boss()
      else:
        enemy = generate_enemy(player)
        
      alive = combat(player, enemy)
      if not alive:
        break

    elif choice == "2":
      player.show_stats()
      
    elif choice == "3":
      change_zone(player)

    elif choice == "4":
      shop(player)
      
    elif choice == "5":
      weapon_shop(player)

    elif choice == "6":
      save_game(player)

    elif choice == "7":
      loaded = load_game()
      if loaded:
        player = loaded

    elif choice == "8":
      print("Goodbye 👋")
      break

    else:
      print("Invalid choice.")



if __name__ == "__main__":
    main()
