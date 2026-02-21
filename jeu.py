import random

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
def generate_enemy():
  enemies = [
    Enemy("Goblin", 50, 8, 2, 40, 10),
    Enemy("Orc", 80, 12, 4, 60, 20),
    Enemy("Skeleton", 60, 10, 3, 50, 15)
  ]
  return random.choice(enemies)


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


# ===== MENU =====
def show_menu():
  print("\n=== MAIN MENU ===")
  print("1. Explore")
  print("2. Show Player Stats")
  print("3. Quit")


# ===== MAIN FUNCTION =====
def main():
  print("Welcome to the Ultimate Adventure Game 🗡️")

  player_name = input("Choose your name: ")
  player = Player(player_name)

  while True:
    if player.health <= 0:
      print("Game Over.")
      break

    show_menu()
    choice = input("What do you want to do? ")

    if choice == "1":
      enemy = generate_enemy()
      alive = combat(player, enemy)
      if not alive:
        break

    elif choice == "2":
      player.show_stats()

    elif choice == "3":
      print("Goodbye 👋")
      break

    else:
      print("Invalid choice.")


if __name__ == "__main__":
    main()
