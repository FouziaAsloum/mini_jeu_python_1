# === Mini Adventure Game ===

# ===== PLAYER CLASS =====
class Player:
  def __init__(self, name):
    self.name = name
    self.health = 100
    self.attack = 15
    self.defense = 5
    self.gold = 0

  def show_stats(self):
    print("\n===== PLAYER STATS =====")
    print(f"Name: {self.name}")
    print(f"Health: {self.health}")
    print(f"Attack: {self.attack}")
    print(f"Defense: {self.defense}")
    print(f"Gold: {self.gold}")
    print("========================\n")

  def attack_enemy(self, enemy):
    damage = self.attack - enemy.defense
    if damage < 0:
        damage = 0
    enemy.health -= damage
    print(f"{self.name} attacks {enemy.name}!")
    print(f"{enemy.name} loses {damage} health points.")


# ===== ENEMY CLASS =====
class Enemy:
  def __init__(self, name, health, attack, defense):
    self.name = name
    self.health = health
    self.attack = attack
    self.defense = defense

  def show_stats(self):
    print("\n===== ENEMY =====")
    print(f"Name: {self.name}")
    print(f"Health: {self.health}")
    print(f"Attack: {self.attack}")
    print(f"Defense: {self.defense}")
    print("=================\n")


# ===== MENU =====
def show_menu():
  print("\n=== MAIN MENU ===")
  print("1. Explore")
  print("2. Show Player Stats")
  print("3. Quit")


# ===== MAIN FUNCTION =====
def main():
  print("Welcome to the Adventure Game 🗡️")

  player_name = input("Choose your name: ")
  player = Player(player_name)

  while True:
    show_menu()
    choice = input("What do you want to do? ")

    if choice == "1":
      print("\nYou go exploring...")
      enemy = Enemy("Goblin", 50, 8, 2)
      enemy.show_stats()

      player.attack_enemy(enemy)

      if enemy.health <= 0:
        print("The goblin has been defeated!")
        player.gold += 10
        print("You gained 10 gold!")
      else:
        print(f"Enemy remaining health: {enemy.health}")

    elif choice == "2":
      player.show_stats()

    elif choice == "3":
      print("Goodbye 👋")
      break

    else:
      print("Invalid choice.")

if __name__ == "__main__":
  main()

