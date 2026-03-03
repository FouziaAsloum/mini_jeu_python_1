import random
import json

# ===== PLAYER CLASS =====
class Player:
  def __init__(self, name):
    self.name = name
    self.health = 100
    self.max_health = 100
    self.attack = 15
    self.defense = 5
    self.gold = 0
    self.level = 1
    self.xp = 0
    self.potions = 2

  def show_stats(self):
    print("\n===== PLAYER STATS =====")
    print(f"Name: {self.name}")
    print(f"Level: {self.level}")
    print(f"XP: {self.xp}/100")
    print(f"Health: {self.health}/{self.max_health}")
    print(f"Attack: {self.attack}")
    print(f"Defense: {self.defense}")
    print(f"Gold: {self.gold}")
    print(f"Potions: {self.potions}")
    print("========================\n")


# ----- TAKE DAMAGE -----
  def take_damage(self, damage):
    self.health -= damage
    self.health = max(0, self.health)


# ----- ATTACK ENEMY -----
  def attack_enemy(self, enemy):
    crit = random.random() < 0.2  # 20% chance critique
    base_damage = random.randint(self.attack - 3, self.attack + 3)
    damage = base_damage - enemy.defense

    if crit:
        damage *= 2
        print("💥 CRITICAL HIT!")

    damage = max(0, damage)
    enemy.take_damage(damage)
    
    print(f"{self.name} attacks {enemy.name} for {damage} damage!")


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

  enemy_types = [
    {"name": "Goblin 👹", "base_health": 50, "base_attack": 8, "base_defense": 2},
    {"name": "Orc 💪", "base_health": 80, "base_attack": 12, "base_defense": 4},
    {"name": "Skeleton 💀", "base_health": 60, "base_attack": 10, "base_defense": 3}
    ]

  enemy_choice = random.choice(enemy_types)

  health = enemy_choice["base_health"] + level * 10
  attack = enemy_choice["base_attack"] + level * 2
  defense = enemy_choice["base_defense"] + level
  xp_reward = 30 + level * 10
  gold_reward = 15 + level * 5

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

  while enemy.health > 0 and player.health > 0:
    print(f"\n{player.name}: {player.health} HP")
    print(f"{enemy.name}: {enemy.health} HP")

    action = input("1.Attack  2.Use Potion : ")

    if action == "1":
      player.attack_enemy(enemy)
    elif action == "2":
      player.use_potion()
    else:
      print("Invalid action.")
      continue

    if enemy.health > 0:
        enemy.attack_player(player)

  if player.health > 0:
    print(f"\n✅ {enemy.name} defeated!")
    player.gold += enemy.gold_reward
    player.gain_xp(enemy.xp_reward)
    print(f"You gained {enemy.gold_reward} gold!")
  else:
    print("\n💀 You were defeated...")
    return False

  return True


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
    "potions": player.potions
    }

  with open("save.json", "w") as file:
    json.dump(data, file, indent=4)

  print("💾 Game saved successfully!")
  
  
# ===== LOAD GAME ===== 
def load_game():
  try:
    with open("save.json", "r") as file:
      data = json.load(file)

      player = Player(data["name"])
      player.level = data["level"]
      player.xp = data["xp"]
      player.health = data["health"]
      player.max_health = data["max_health"]
      player.attack = data["attack"]
      player.defense = data["defense"]
      player.gold = data["gold"]
      player.potions = data["potions"]

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
  print("3. Shop")
  print("4. Save Game")
  print("5. Load Game")
  print("6. Quit")





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
      player = Player(player_name)
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
        enemy = generate_boss(player)
      else:
        enemy = generate_enemy(player)
        
      alive = combat(player, enemy)
      if not alive:
        break

    elif choice == "2":
      player.show_stats()

    elif choice == "3":
      shop(player)

    elif choice == "4":
      save_game(player)

    elif choice == "5":
      loaded = load_game()
      if loaded:
          player = loaded

    elif choice == "6":
      print("Goodbye 👋")
      break

    else:
      print("Invalid choice.")



if __name__ == "__main__":
    main()
