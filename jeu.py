import random
import json
import os
import time

# ===== CONSTANTS =====
SAVE_FILE = "savegame.json"

# ===== SHOP =====
SHOP_ITEMS = {
  "weapons": [
    {"name": "Iron Sword ⚔️",      "bonus_attack": 5,  "price": 50},
    {"name": "Steel Blade 🗡️",     "bonus_attack": 10, "price": 100},
    {"name": "Enchanted Staff 🪄",  "bonus_attack": 15, "price": 150},
    {"name": "Shadow Dagger 🌑",    "bonus_attack": 12, "price": 120},
    {"name": "Dragon Slayer 🐉",    "bonus_attack": 25, "price": 300},
  ],
  "armor": [
    {"name": "Leather Armor 🧥",   "bonus_defense": 3,  "price": 40},
    {"name": "Chain Mail ⛓️",      "bonus_defense": 6,  "price": 80},
    {"name": "Plate Armor 🛡️",     "bonus_defense": 10, "price": 150},
    {"name": "Shadow Cloak 🌑",    "bonus_defense": 7,  "price": 100},
    {"name": "Dragon Scale 🐲",    "bonus_defense": 15, "price": 280},
  ],
  "potions": [
    {"name": "Small Potion 🧪",    "heal": 30,  "price": 20},
    {"name": "Medium Potion 💊",   "heal": 60,  "price": 40},
    {"name": "Large Potion 🫙",    "heal": 100, "price": 70},
    {"name": "Elixir ✨",          "heal": 999, "price": 200},
  ],
  "special": [
    {"name": "Mana Crystal 💎",    "mana": 30,  "price": 35},
    {"name": "XP Scroll 📜",       "xp": 50,    "price": 60},
    {"name": "Lucky Charm 🍀",     "luck": 0.1, "price": 90},
  ]
}

# ===== COMBAT ZONES =====
ZONES = {
  "Forest 🌲": {
    "required_level": 1,
    "description": "A dark forest full of goblins and wolves.",
    "enemies": ["Goblin 👹", "Wolf 🐺", "Bandit 🦹"],
    "boss": "Forest Troll 👾",
  },
  "Desert 🏜️": {
    "required_level": 3,
    "description": "A scorching desert with deadly creatures.",
    "enemies": ["Scorpion 🦂", "Sand Wraith 👻", "Desert Bandit 🦹"],
    "boss": "Sand Wyrm 🐍",
  },
  "Volcano 🌋": {
    "required_level": 6,
    "description": "A dangerous volcano with fire monsters.",
    "enemies": ["Fire Imp 😈", "Lava Golem 🪨", "Phoenix Hawk 🦅"],
    "boss": "Dragon 🐉",
  },
  "Dungeon 🏰": {
    "required_level": 10,
    "description": "An ancient dungeon full of undead.",
    "enemies": ["Skeleton ☠️", "Zombie 🧟", "Dark Knight ⚫"],
    "boss": "Lich King 💀",
  },
}

# ===== QUESTS =====
QUESTS = [
  {
    "id": "q1",
    "name": "First Blood 🩸",
    "description": "Kill your first enemy.",
    "goal_kills": 1,
    "reward_xp": 30,
    "reward_gold": 20,
  },
  {
    "id": "q2",
    "name": "Goblin Slayer 👹",
    "description": "Kill 5 enemies.",
    "goal_kills": 5,
    "reward_xp": 80,
    "reward_gold": 50,
  },
  {
    "id": "q3",
    "name": "Veteran ⚔️",
    "description": "Kill 15 enemies.",
    "goal_kills": 15,
    "reward_xp": 200,
    "reward_gold": 120,
  },
  {
    "id": "q4",
    "name": "Hero 🏆",
    "description": "Reach level 5.",
    "goal_level": 5,
    "reward_xp": 300,
    "reward_gold": 200,
  },
  {
    "id": "q5",
    "name": "Legend 🌟",
    "description": "Reach level 10.",
    "goal_level": 10,
    "reward_xp": 500,
    "reward_gold": 400,
  },
]

# ===== UI HELPERS =====
def clear_screen():
  os.system("cls" if os.name == "nt" else "clear")

def pause(msg="Press Enter to continue..."):
  input(f"\n  {msg}")

def divider():
  print("  " + "─" * 36)

def title(text):
  print("\n" + "="*40)
  print(f"  {text}")
  print("="*40)

def health_bar(current, maximum, length=20):
  filled = int((current / maximum) * length)
  bar = "█" * filled + "░" * (length - filled)
  return f"[{bar}] {current}/{maximum}"

# ===== ENEMY CLASS =====
class Enemy:
  def __init__(self, name, health, attack, defense, xp, gold):
    self.name       = name
    self.health     = health
    self.max_health = health
    self.attack     = attack
    self.defense    = defense
    self.xp         = xp
    self.gold       = gold

  def take_damage(self, damage):
    self.health = max(0, self.health - damage)

  def attack_player(self, player):
    damage = random.randint(self.attack - 3, self.attack + 3)
    damage = max(0, damage - player.defense)
    player.take_damage(damage)
    print(f"\n  {self.name} attacks {player.name} for {damage} damage!")

# ===== PLAYER CLASS =====
class Player:
  def __init__(self, name, player_class):
    self.name             = name
    self.player_class     = player_class
    self.level            = 1
    self.xp               = 0
    self.xp_to_next       = 100
    self.gold             = 0
    self.potions          = 2
    self.kills            = 0
    self.completed_quests = []
    self.luck             = 0.0

    if player_class == "Warrior":
      self.max_health = 120
      self.attack     = 18
      self.defense    = 8
      self.mana       = 0
    elif player_class == "Mage":
      self.max_health = 80
      self.attack     = 10
      self.defense    = 3
      self.mana       = 50
    elif player_class == "Assassin":
      self.max_health = 90
      self.attack     = 15
      self.defense    = 4
      self.mana       = 20
    else:
      self.max_health = 100
      self.attack     = 12
      self.defense    = 5
      self.mana       = 0

    # Common attributes for all classes
    self.health    = self.max_health
    self.zone      = "Forest 🌲"
    self.weapon    = {"name": "Rusty Sword 🗡️", "bonus_attack": 2}
    self.armor     = {"name": "Cloth Shirt 👕",  "bonus_defense": 0}
    self.inventory = []

  def show_stats(self):
    title(f"📊  STATS — {self.name}")
    print(f"  Class   : {self.player_class}")
    print(f"  Level   : {self.level}")
    print(f"  XP      : {self.xp}/{self.xp_to_next}")
    print(f"  Health  : {health_bar(self.health, self.max_health)}")
    print(f"  Attack  : {self.attack}")
    print(f"  Defense : {self.defense}")
    print(f"  Gold    : {self.gold} 💰")
    print(f"  Potions : {self.potions} 🧪")
    print(f"  Kills   : {self.kills}")
    print(f"  Weapon  : {self.weapon['name']} (+{self.weapon['bonus_attack']} ATK)")
    print(f"  Armor   : {self.armor['name']} (+{self.armor['bonus_defense']} DEF)")
    print(f"  Zone    : {self.zone}")
    if self.mana > 0:
      print(f"  Mana    : {self.mana} 💎")
    divider()

  def take_damage(self, damage):
    self.health = max(0, self.health - damage)

  def heal(self, amount):
    self.health = min(self.max_health, self.health + amount)

  def use_potion(self):
    if self.potions <= 0:
      print("  ❌ No potions left!")
      return
    self.heal(50)
    self.potions -= 1
    print(f"  🧪 Used a potion! ({self.health}/{self.max_health} HP) — {self.potions} left")

  def attack_enemy(self, enemy):
    # Critical hit chance based on luck
    crit_chance = 0.1 + self.luck
    is_crit     = random.random() < crit_chance

    damage = self.attack + self.weapon["bonus_attack"]
    damage = random.randint(int(damage * 0.8), int(damage * 1.2))
    damage = max(0, damage - enemy.defense)

    if is_crit:
      damage = int(damage * 1.5)
      print(f"\n  💥 CRITICAL HIT! {self.name} attacks {enemy.name} for {damage} damage!")
    else:
      print(f"\n  ⚔️  {self.name} attacks {enemy.name} for {damage} damage!")

    enemy.take_damage(damage)

  def special_ability(self, enemy):
    if self.player_class == "Warrior":
      damage = (self.attack + self.weapon["bonus_attack"]) * 2
      damage = max(0, damage - enemy.defense)
      enemy.take_damage(damage)
      print(f"  🗡️  POWER STRIKE! {self.name} hits {enemy.name} for {damage} damage!")

    elif self.player_class == "Mage":
      if self.mana < 20:
        print("  ❌ Not enough mana! (Need 20)")
        return
      damage = (self.attack + self.weapon["bonus_attack"]) + random.randint(15, 30)
      damage = max(0, damage - enemy.defense)
      enemy.take_damage(damage)
      self.mana -= 20
      print(f"  🪄  FIREBALL! {self.name} blasts {enemy.name} for {damage} damage! (Mana: {self.mana})")

    elif self.player_class == "Assassin":
      if self.mana < 10:
        print("  ❌ Not enough mana! (Need 10)")
        return
      damage = (self.attack + self.weapon["bonus_attack"]) + random.randint(10, 20)
      damage = max(0, damage - enemy.defense)
      enemy.take_damage(damage)
      self.mana -= 10
      print(f"  🌑  BACKSTAB! {self.name} stabs {enemy.name} for {damage} damage! (Mana: {self.mana})")

  def gain_xp(self, amount):
    self.xp += amount
    print(f"  ✨ +{amount} XP ({self.xp}/{self.xp_to_next})")
    while self.xp >= self.xp_to_next:
      self.xp -= self.xp_to_next
      self.level_up()

  def level_up(self):
    self.level      += 1
    self.xp_to_next  = int(self.xp_to_next * 1.5)
    self.max_health += 15
    self.health      = self.max_health
    self.attack     += 3
    self.defense    += 1
    if self.mana > 0:
      self.mana = min(100, self.mana + 10)
    print(f"\n  🎉 LEVEL UP! You are now Level {self.level}!")
    print(f"  ❤️  Max HP +15 | ⚔️  ATK +3 | 🛡️  DEF +1")

# ===== ENEMY GENERATION =====
ENEMY_TEMPLATES = {
  "Goblin 👹":         {"health": 40,  "attack": 10, "defense": 2,  "xp": 20, "gold": 10},
  "Wolf 🐺":           {"health": 50,  "attack": 12, "defense": 3,  "xp": 25, "gold": 8},
  "Bandit 🦹":         {"health": 60,  "attack": 14, "defense": 4,  "xp": 30, "gold": 20},
  "Scorpion 🦂":       {"health": 65,  "attack": 16, "defense": 5,  "xp": 35, "gold": 15},
  "Sand Wraith 👻":    {"health": 55,  "attack": 18, "defense": 3,  "xp": 40, "gold": 18},
  "Desert Bandit 🦹":  {"health": 75,  "attack": 17, "defense": 6,  "xp": 38, "gold": 25},
  "Fire Imp 😈":       {"health": 70,  "attack": 20, "defense": 5,  "xp": 45, "gold": 20},
  "Lava Golem 🪨":     {"health": 100, "attack": 22, "defense": 10, "xp": 60, "gold": 30},
  "Phoenix Hawk 🦅":   {"health": 80,  "attack": 24, "defense": 7,  "xp": 55, "gold": 28},
  "Skeleton ☠️":       {"health": 90,  "attack": 25, "defense": 8,  "xp": 65, "gold": 35},
  "Zombie 🧟":         {"health": 110, "attack": 20, "defense": 9,  "xp": 60, "gold": 30},
  "Dark Knight ⚫":    {"health": 120, "attack": 28, "defense": 12, "xp": 80, "gold": 50},
}

BOSS_TEMPLATES = {
  "Forest Troll 👾": {"health": 180, "attack": 22, "defense": 8,  "xp": 120, "gold": 80},
  "Sand Wyrm 🐍":    {"health": 220, "attack": 28, "defense": 10, "xp": 160, "gold": 100},
  "Dragon 🐉":       {"health": 300, "attack": 35, "defense": 15, "xp": 250, "gold": 200},
  "Lich King 💀":    {"health": 400, "attack": 40, "defense": 18, "xp": 400, "gold": 350},
}

def scale_enemy(template, player_level):
  t     = template.copy()
  bonus = (player_level - 1) * 0.1
  t["health"]  = int(t["health"]  * (1 + bonus))
  t["attack"]  = int(t["attack"]  * (1 + bonus))
  t["defense"] = int(t["defense"] * (1 + bonus))
  t["xp"]      = int(t["xp"]      * (1 + bonus))
  t["gold"]    = int(t["gold"]    * (1 + bonus))
  return t

def generate_zone_enemy(player):
  zone_data = ZONES[player.zone]
  name      = random.choice(zone_data["enemies"])
  t         = scale_enemy(ENEMY_TEMPLATES[name], player.level)
  return Enemy(name, t["health"], t["attack"], t["defense"], t["xp"], t["gold"])

def generate_zone_boss(player):
  zone_data = ZONES[player.zone]
  name      = zone_data["boss"]
  t         = scale_enemy(BOSS_TEMPLATES[name], player.level)
  return Enemy(name, t["health"], t["attack"], t["defense"], t["xp"], t["gold"])

# ===== QUEST SYSTEM =====
def check_quests(player):
  for quest in QUESTS:
    if quest["id"] in player.completed_quests:
      continue

    completed = False
    if "goal_kills" in quest and player.kills >= quest["goal_kills"]:
      completed = True
    if "goal_level" in quest and player.level >= quest["goal_level"]:
      completed = True

    if completed:
      player.completed_quests.append(quest["id"])
      player.xp   += quest["reward_xp"]
      player.gold += quest["reward_gold"]
      print(f"\n  🏆 QUEST COMPLETE: {quest['name']}")
      print(f"  Reward: +{quest['reward_xp']} XP, +{quest['reward_gold']} Gold")

def show_quests(player):
  title("📋  QUESTS")
  for quest in QUESTS:
    status = "✅" if quest["id"] in player.completed_quests else "🔲"
    print(f"  {status} {quest['name']}")
    print(f"     {quest['description']}")
    print(f"     Reward: {quest['reward_xp']} XP + {quest['reward_gold']} Gold")
    divider()

# ===== INVENTORY =====
def show_inventory(player):
  while True:
    title(f"🎒  INVENTORY — {player.name}")
    print(f"  🗡️  Equipped weapon : {player.weapon['name']} (+{player.weapon['bonus_attack']} ATK)")
    print(f"  🛡️  Equipped armor  : {player.armor['name']} (+{player.armor['bonus_defense']} DEF)")
    print(f"  🧪  Potions         : {player.potions}")
    if player.mana > 0:
      print(f"  💎  Mana            : {player.mana}/100")
    divider()

    weapons = [i for i in player.inventory if "bonus_attack"  in i]
    armors  = [i for i in player.inventory if "bonus_defense" in i]

    if not weapons and not armors:
      print("  📭 No items in inventory.")
      print("     (Potions and special items are used automatically)")
    else:
      if weapons:
        print("  ⚔️  WEAPONS:")
        for i, item in enumerate(weapons, 1):
          equipped = " ◄ EQUIPPED" if item["name"] == player.weapon["name"] else ""
          print(f"    {i}. {item['name']} (+{item['bonus_attack']} ATK){equipped}")
        divider()

      if armors:
        offset = len(weapons)
        print("  🛡️  ARMOR:")
        for i, item in enumerate(armors, 1):
          equipped = " ◄ EQUIPPED" if item["name"] == player.armor["name"] else ""
          print(f"    {i + offset}. {item['name']} (+{item['bonus_defense']} DEF){equipped}")
        divider()

    print("  Enter a number to equip an item")
    print("  0. 🚪  Back")
    divider()

    choice = input("  Choice: ").strip()

    if choice == "0":
      break

    if not choice.isdigit():
      print("  ❌ Invalid choice.")
      continue

    idx            = int(choice) - 1
    all_equippable = weapons + armors

    if idx < 0 or idx >= len(all_equippable):
      print("  ❌ Invalid choice.")
      continue

    item = all_equippable[idx]

    if "bonus_attack" in item:
      player.weapon = {"name": item["name"], "bonus_attack": item["bonus_attack"]}
      print(f"  ✅ {item['name']} equipped!")
    elif "bonus_defense" in item:
      player.armor = {"name": item["name"], "bonus_defense": item["bonus_defense"]}
      print(f"  ✅ {item['name']} equipped!")

    pause()

# ===== SHOP =====
def show_shop(player):
  while True:
    title("🏪  SHOP")
    print(f"  💰 Your Gold: {player.gold}")
    divider()
    print("  1. 🗡️  Weapons")
    print("  2. 🛡️  Armor")
    print("  3. 🧪  Potions")
    print("  4. ✨  Special Items")
    print("  5. 🚪  Leave Shop")
    divider()

    choice = input("  Choice: ").strip()

    if choice == "1":
      buy_item(player, "weapons")
    elif choice == "2":
      buy_item(player, "armor")
    elif choice == "3":
      buy_item(player, "potions")
    elif choice == "4":
      buy_item(player, "special")
    elif choice == "5":
      break
    else:
      print("  ❌ Invalid choice.")

def buy_item(player, category):
  items = SHOP_ITEMS[category]
  title(f"🏪  {category.upper()}")
  print(f"  💰 Gold: {player.gold}")
  divider()

  for i, item in enumerate(items, 1):
    if "bonus_attack"  in item: stat = f"+{item['bonus_attack']} ATK"
    elif "bonus_defense" in item: stat = f"+{item['bonus_defense']} DEF"
    elif "heal"  in item:         stat = f"+{item['heal']} HP"
    elif "mana"  in item:         stat = f"+{item['mana']} MP"
    elif "xp"    in item:         stat = f"+{item['xp']} XP"
    elif "luck"  in item:         stat = f"+{item['luck']} Luck"
    else:                         stat = ""
    print(f"  {i}. {item['name']} ({stat}) — {item['price']} gold")

  divider()
  print("  0. Back")
  choice = input("  Buy: ").strip()

  if choice == "0":
    return

  if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
    print("  ❌ Invalid choice.")
    return

  item = items[int(choice) - 1]

  if player.gold < item["price"]:
    print(f"  ❌ Not enough gold! (Need {item['price']})")
    return

  player.gold -= item["price"]

  if "bonus_attack" in item:
    player.weapon = {"name": item["name"], "bonus_attack": item["bonus_attack"]}
    print(f"  ✅ Equipped {item['name']}!")

  elif "bonus_defense" in item:
    player.armor      = {"name": item["name"], "bonus_defense": item["bonus_defense"]}
    player.defense    = player.defense - getattr(player, "_armor_bonus", 0) + item["bonus_defense"]
    player._armor_bonus = item["bonus_defense"]
    print(f"  ✅ Equipped {item['name']}!")

  elif "heal" in item:
    player.potions += 1
    print(f"  ✅ Bought a potion! ({player.potions} total)")

  elif "mana" in item:
    player.mana = min(100, player.mana + item["mana"])
    print(f"  ✅ Mana restored! ({player.mana}/100)")

  elif "xp" in item:
    player.gain_xp(item["xp"])

  elif "luck" in item:
    player.luck += item["luck"]
    print(f"  ✅ Lucky Charm equipped! (Luck: {player.luck:.1f})")

# ===== ZONE SYSTEM =====
def show_zones(player):
  title("🗺️  ZONES")
  zone_names = list(ZONES.keys())

  for i, (zone_name, data) in enumerate(ZONES.items(), 1):
    locked  = player.level < data["required_level"]
    status  = "🔒" if locked else "✅"
    current = " ◄ CURRENT" if zone_name == player.zone else ""
    print(f"  {i}. {status} {zone_name}{current}")
    print(f"     {data['description']}")
    print(f"     Required Level: {data['required_level']}")
    divider()

  print("  0. Back")
  choice = input("  Travel to: ").strip()

  if choice == "0":
    return

  if not choice.isdigit() or not (1 <= int(choice) <= len(zone_names)):
    print("  ❌ Invalid choice.")
    return

  chosen = zone_names[int(choice) - 1]
  req    = ZONES[chosen]["required_level"]

  if player.level < req:
    print(f"  🔒 You need Level {req} to enter {chosen}!")
    return

  player.zone = chosen
  print(f"  🗺️  You traveled to {chosen}!")

# ===== COMBAT =====
def combat(player, enemy, is_boss=False):
  clear_screen()
  label = "👾  BOSS FIGHT" if is_boss else "⚔️   COMBAT"
  title(label)
  print(f"  {player.name} vs {enemy.name}")
  divider()
  time.sleep(1)

  while player.health > 0 and enemy.health > 0:
    print(f"\n  {player.name} : {health_bar(player.health, player.max_health)}")
    print(f"  {enemy.name}  : {health_bar(enemy.health, enemy.max_health)}")
    divider()
    print("  1. ⚔️  Attack")
    print("  2. ✨  Special Ability")
    print("  3. 🧪  Use Potion")
    print("  4. 🏃  Run Away")
    divider()

    choice = input("  Action: ").strip()

    if choice == "1":
      player.attack_enemy(enemy)
    elif choice == "2":
      player.special_ability(enemy)
    elif choice == "3":
      player.use_potion()
    elif choice == "4":
      if random.random() < 0.5:
        print("  🏃 You ran away successfully!")
        return "flee"
      else:
        print("  ❌ Couldn't escape!")
    else:
      print("  ❌ Invalid choice.")
      continue

    if enemy.health > 0:
      enemy.attack_player(player)

  if player.health > 0:
    print(f"\n  ✅ {enemy.name} defeated!")
    player.kills += 1
    player.gain_xp(enemy.xp)
    player.gold += enemy.gold
    print(f"  💰 +{enemy.gold} gold!")
    check_quests(player)
    return "win"
  else:
    print("\n  💀 You were defeated...")
    return "lose"

# ===== PvP COMBAT =====
def pvp_combat(player1, player2):
  clear_screen()
  title("🥊  PvP BATTLE")
  print(f"  {player1.name} ({player1.player_class}) vs {player2.name} ({player2.player_class})")
  divider()
  time.sleep(1)

  players = [player1, player2]
  turn    = 0

  while player1.health > 0 and player2.health > 0:
    attacker = players[turn % 2]
    defender = players[(turn + 1) % 2]

    print(f"\n  {player1.name} : {health_bar(player1.health, player1.max_health)}")
    print(f"  {player2.name} : {health_bar(player2.health, player2.max_health)}")
    divider()
    print(f"  🎮 {attacker.name}'s turn!")
    print("  1. ⚔️  Attack")
    print("  2. ✨  Special Ability")
    print("  3. 🧪  Use Potion")
    divider()

    choice = input("  Action: ").strip()

    if choice == "1":
      attacker.attack_enemy(defender)
    elif choice == "2":
      attacker.special_ability(defender)
    elif choice == "3":
      attacker.use_potion()
    else:
      print("  ❌ Invalid choice.")
      continue

    turn += 1

  winner = player1 if player1.health > 0 else player2
  loser  = player2 if player1.health > 0 else player1
  print(f"\n  🏆 {winner.name} wins the duel!")
  print(f"  💀 {loser.name} was defeated!")

# ===== CO-OP COMBAT =====
def coop_combat(player1, player2, enemy, is_boss=False):
  clear_screen()
  label = "👾  BOSS FIGHT (CO-OP)" if is_boss else "⚔️   CO-OP COMBAT"
  title(label)
  print(f"  {player1.name} & {player2.name} vs {enemy.name}")
  divider()
  time.sleep(1)

  players = [player1, player2]
  turn    = 0

  while (player1.health > 0 or player2.health > 0) and enemy.health > 0:
    active  = players[turn % 2]
    partner = players[(turn + 1) % 2]

    if active.health <= 0:
      turn += 1
      continue

    print(f"\n  {player1.name} : {health_bar(player1.health, player1.max_health)}")
    print(f"  {player2.name} : {health_bar(player2.health, player2.max_health)}")
    print(f"  {enemy.name}   : {health_bar(enemy.health, enemy.max_health)}")
    divider()
    print(f"  🎮 {active.name}'s turn!")
    print("  1. ⚔️  Attack")
    print("  2. ✨  Special Ability")
    print("  3. 🧪  Use Potion")
    print(f"  4. 💊  Heal {partner.name}")
    divider()

    choice = input("  Action: ").strip()

    if choice == "1":
      active.attack_enemy(enemy)
    elif choice == "2":
      active.special_ability(enemy)
    elif choice == "3":
      active.use_potion()
    elif choice == "4":
      if active.potions <= 0:
        print("  ❌ No potions left!")
        continue
      partner.heal(50)
      active.potions -= 1
      print(f"  💊 {active.name} healed {partner.name} for 50 HP! ({partner.health}/{partner.max_health})")
    else:
      print("  ❌ Invalid choice.")
      continue

    if enemy.health > 0:
      target = random.choice([p for p in players if p.health > 0])
      enemy.attack_player(target)

    turn += 1

  if enemy.health <= 0:
    print(f"\n  ✅ {enemy.name} defeated!")
    xp_each   = enemy.xp   // 2
    gold_each = enemy.gold // 2
    for p in players:
      p.kills += 1
      p.gain_xp(xp_each)
      p.gold += gold_each
      check_quests(p)
    print(f"  💰 Each player gets {gold_each} gold!")
    return "win"
  else:
    print("\n  💀 Both players were defeated...")
    return "lose"

# ===== SAVE / LOAD =====
def choose_save_slot(action="save"):
  title(f"💾  {action.upper()} — CHOOSE SLOT")
  print("  1. Slot 1")
  print("  2. Slot 2")
  print("  3. Slot 3")
  print("  0. Cancel")
  divider()
  choice = input("  Slot: ").strip()
  if choice in ("1", "2", "3"):
    return f"save_player_{choice}.json"
  return None

def save_game(player):
  slot = choose_save_slot("save")
  if not slot:
    return
  data = player.__dict__.copy()
  with open(slot, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
  print(f"  💾 Game saved to {slot}!")

def load_game(slot=None):
  if not slot:
    slot = choose_save_slot("load")
  if not slot:
    return None
  try:
    with open(slot, "r") as f:
      data = json.load(f)
    player = Player(data["name"], data["player_class"])
    player.__dict__.update(data)
    print(f"  ✅ Game loaded from {slot}!")
    return player
  except FileNotFoundError:
    print("  ⚠️  No save file found in this slot.")
    return None
  except json.JSONDecodeError:
    print("  ⚠️  Save file corrupted.")
    return None

# ===== MENUS =====
def show_menu_single():
  title("📜  MENU")
  print("  1. ⚔️  Explore")
  print("  2. 📊  Stats")
  print("  3. 🎒  Inventory")
  print("  4. 🏪  Shop")
  print("  5. 🗺️  Change Zone")
  print("  6. 📋  Quests")
  print("  7. 💾  Save")
  print("  8. 🚪  Quit")
  divider()

def show_menu_multi():
  title("📜  MULTIPLAYER MENU")
  print("  1.  ⚔️  Explore Together (Co-op)")
  print("  2.  🥊  PvP Duel")
  print("  3.  📊  Show Stats")
  print("  4.  🎒  Inventory P1")
  print("  5.  🎒  Inventory P2")
  print("  6.  🏪  Shop (Player 1)")
  print("  7.  🏪  Shop (Player 2)")
  print("  8.  🗺️  Change Zone")
  print("  9.  📋  Quests")
  print("  10. 💾  Save Both")
  print("  11. 🚪  Quit")
  divider()

# ===== GAME LOOPS =====
def single_player_loop(player):
  while player.health > 0:
    show_menu_single()
    choice = input("  Action: ").strip()

    if choice == "1":
      is_boss = random.random() < 0.2
      enemy   = generate_zone_boss(player) if is_boss else generate_zone_enemy(player)
      print(f"  📍 Zone: {player.zone}")
      result  = combat(player, enemy, is_boss=is_boss)
      if result == "lose":
        title("💀  GAME OVER")
        print("  Your adventure ends here...")
        divider()
        break

    elif choice == "2":
      player.show_stats()
      pause()

    elif choice == "3":
      show_inventory(player)

    elif choice == "4":
      show_shop(player)

    elif choice == "5":
      show_zones(player)

    elif choice == "6":
      show_quests(player)
      pause()

    elif choice == "7":
      save_game(player)
      pause()

    elif choice == "8":
      print("  👋 Goodbye!")
      break

    else:
      print("  ❌ Invalid choice.")

def multi_player_loop(player1, player2):
  while True:
    show_menu_multi()
    choice = input("  Action: ").strip()

    if choice == "1":
      is_boss = random.random() < 0.2
      enemy   = generate_zone_boss(player1) if is_boss else generate_zone_enemy(player1)
      print(f"  📍 Zone: {player1.zone}")
      result  = coop_combat(player1, player2, enemy, is_boss=is_boss)
      if result == "lose":
        title("💀  GAME OVER")
        print("  Both adventurers have fallen...")
        divider()
        break

    elif choice == "2":
      pvp_combat(player1, player2)

    elif choice == "3":
      player1.show_stats()
      player2.show_stats()
      pause()

    elif choice == "4":
      show_inventory(player1)

    elif choice == "5":
      show_inventory(player2)

    elif choice == "6":
      show_shop(player1)

    elif choice == "7":
      show_shop(player2)

    elif choice == "8":
      show_zones(player1)
      player2.zone = player1.zone

    elif choice == "9":
      show_quests(player1)
      show_quests(player2)
      pause()

    elif choice == "10":
      save_game(player1)
      save_game(player2)

    elif choice == "11":
      print("  👋 Goodbye!")
      break

    else:
      print("  ❌ Invalid choice.")

# ===== CHARACTER CREATION =====
def create_player(player_number=1):
  title(f"🧑  CREATE CHARACTER — PLAYER {player_number}")
  name = input("  Enter your name: ").strip()
  if not name:
    name = f"Hero{player_number}"

  print("\n  Choose your class:")
  print("  1. ⚔️  Warrior  — High HP & Defense")
  print("  2. 🪄  Mage     — High Magic Damage")
  print("  3. 🌑  Assassin — High Speed & Crits")
  divider()

  c       = input("  Class: ").strip()
  classes = {"1": "Warrior", "2": "Mage", "3": "Assassin"}
  cls     = classes.get(c, "Warrior")

  player = Player(name, cls)
  print(f"\n  ✅ {name} the {cls} created!")
  return player

def setup_player(player_number=1):
  title(f"👤  PLAYER {player_number} SETUP")
  print("  1. 🆕  New Character")
  print("  2. 📂  Load Character")
  divider()

  choice = input("  Choice: ").strip()

  if choice == "2":
    slot = choose_save_slot("load")
    if slot:
      player = load_game(slot)
      if player:
        return player
    print("  ⚠️  Switching to new character creation.")

  return create_player(player_number)

# ===== MAIN =====
def main():
  clear_screen()
  title("⚔️   WELCOME TO ULTIMATE ADVENTURE   ⚔️")
  print("  A text-based RPG with multiplayer support.")
  divider()
  print("  1. 🧑  Single Player")
  print("  2. 👥  Multiplayer (Local Co-op / PvP)")
  divider()

  mode = input("  Mode: ").strip()

  if mode == "2":
    clear_screen()
    title("👥  MULTIPLAYER SETUP")
    print("  Player 1 will set up first, then Player 2.\n")
    pause("Player 1, press Enter when ready...")
    player1 = setup_player(1)

    clear_screen()
    pause("Player 2, press Enter when ready...")
    player2 = setup_player(2)

    multi_player_loop(player1, player2)

  else:
    player = setup_player(1)
    single_player_loop(player)

if __name__ == "__main__":
  main()
