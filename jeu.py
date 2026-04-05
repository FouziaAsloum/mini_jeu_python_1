import os
import random
import time
import json

# ===== SHOP ITEMS =====
SHOP_ITEMS = {
  "weapons": [
    {"name": "Iron Sword ⚔️", "bonus_attack": 5, "price": 50},
    {"name": "Steel Blade 🗡️", "bonus_attack": 10, "price": 100},
    {"name": "Enchanted Staff 🪄", "bonus_attack": 15, "price": 150},
    {"name": "Shadow Dagger 🌑", "bonus_attack": 12, "price": 120},
    {"name": "Dragon Slayer 🐉", "bonus_attack": 25, "price": 300},
  ],
  "armor": [
    {"name": "Leather Armor 🧥", "bonus_defense": 3, "price": 40},
    {"name": "Chain Mail ⛓️", "bonus_defense": 6, "price": 80},
    {"name": "Plate Armor 🛡️", "bonus_defense": 10, "price": 150},
    {"name": "Shadow Cloak 🌑", "bonus_defense": 7, "price": 100},
    {"name": "Dragon Scale 🐲", "bonus_defense": 15, "price": 280},
  ],
  "potions": [
    {"name": "Small Potion 🧪", "heal": 30, "price": 20},
    {"name": "Medium Potion 💊", "heal": 60, "price": 40},
    {"name": "Large Potion 🫙", "heal": 100, "price": 70},
    {"name": "Elixir ✨", "heal": 999, "price": 200},
  ],
  "special": [
    {"name": "Mana Crystal 💎", "mana": 30, "price": 35},
    {"name": "XP Scroll 📜", "xp": 50, "price": 60},
    {"name": "Lucky Charm 🍀", "luck": 0.1, "price": 90},
  ]
}

# ===== COMBAT ZONES =====
ZONES = {
  "Village 🏘️": {
    "required_level": 1,
    "description": "A safe haven to shop, rest and take quests.",
    "enemies": [],
    "boss": None,
  },
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

RANDOM_EVENTS = [
  {"name": "💰 Treasure Chest", "weight": 15},
  {"name": "🧙 Mysterious Merchant", "weight": 10},
  {"name": "⚗️ Magic Fountain", "weight": 12},
  {"name": "🪤 Trap", "weight": 13},
  {"name": "📦 Supply Crate", "weight": 15},
  {"name": "🌟 Blessing", "weight": 12},
  {"name": "👻 Ambush", "weight": 10},
  {"name": "⚔️ Normal Combat", "weight": 50},
]

# ===== UI HELPERS =====
def clear_screen():
  os.system("cls" if os.name == "nt" else "clear")

def pause(msg="Press Enter to continue..."):
  input(f"\n  {msg}")

def divider():
  print("  " + "─" * 36)

def title(text):
  clear_screen()
  print("  " + " " * 15 + text + " " * 15)
  print("  " + "─" * 36)

def health_bar(current, maximum, length=20):
  filled = int((current / maximum) * length)
  bar = "█" * filled + "░" * (length - filled)
  return f"[{bar}] {current}/{maximum}"

# ===== PLAYER CLASS =====
class Player:
  def __init__(self, name, player_class):
    self.name = name
    self.player_class = player_class
    self.level = 1
    self.xp = 0
    self.xp_to_next = 100
    self.gold = 0
    self.potions = 2
    self.kills = 0
    self.completed_quests = []
    self.luck = 0.0
    self.reputation = 0

    if player_class == "Warrior":
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
    else:
      self.max_health = 100
      self.attack = 12
      self.defense = 5
      self.mana = 0

    self.health = self.max_health
    self.zone = "Village 🏘️"
    self.weapon = {"name": "Rusty Sword 🗡️", "bonus_attack": 2}
    self.armor = {"name": "Cloth Shirt 👕", "bonus_defense": 0}
    self.inventory = []
    self.status_effects = {}
    self._armor_bonus = 0

  def take_damage(self, damage):
    self.health = max(0, self.health - damage)
    if self.health <= 0:
      print(f"  💀 {self.name} has fallen!")

  def gain_xp(self, amount):
    self.xp += amount
    print(f"  ✨ +{amount} XP!")
    if self.xp >= self.xp_to_next:
      self.level_up()

  def level_up(self):
    self.level += 1
    self.xp -= self.xp_to_next
    self.xp_to_next = int(self.xp_to_next * 1.5)
    self.max_health += 10
    self.health = self.max_health
    self.attack += 2
    self.defense += 1
    if self.mana > 0:
      self.mana = min(100, self.mana + 10)
    print(f"\n  🎉 LEVEL UP! You are now level {self.level}!")
    print(f"  ❤️  Max HP +10 | ⚔️  ATK +2 | 🛡️  DEF +1")

  def use_potion(self):
    if self.potions > 0:
      heal = 50
      self.health = min(self.max_health, self.health + heal)
      self.potions -= 1
      print(f"  🧪 Used a potion! +{heal} HP ({self.health}/{self.max_health})")
    else:
      print("  ❌ No potions left!")

  def special_ability(self, enemy):
    rage_mult = 1.5 if "rage" in self.status_effects else 1.0

    if self.player_class == "Warrior":
      damage = (self.attack + self.weapon["bonus_attack"]) * 2
      damage = max(0, damage - enemy.defense)
      damage = int(damage * rage_mult)
      if rage_mult > 1:
        print("  😡 Rage boost!")
      enemy.take_damage(damage)
      print(f"  🗡️  POWER STRIKE! {self.name} hits {enemy.name} for {damage} damage!")

    elif self.player_class == "Mage":
      if self.mana >= 10:
        damage = (self.attack + self.weapon["bonus_attack"]) * 3
        damage = max(0, damage - enemy.defense)
        self.mana -= 10
        print(f"  🔮  FIREBALL! {self.name} hits {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)
      else:
        print("  ❌ Not enough mana!")

    elif self.player_class == "Assassin":
      if random.random() < 0.3:
        damage = int((self.attack + self.weapon["bonus_attack"]) * 1.5)
        damage = max(0, damage - enemy.defense)
        print(f"  🗡️  CRITICAL STRIKE! {self.name} hits {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)
      else:
        print("  ❌ Missed!")

  def show_stats(self):
    title(f"📊  STATS — {self.name}")
    print(f"  Level     : {self.level}")
    print(f"  XP        : {self.xp}/{self.xp_to_next}")
    print(f"  Health    : {self.health}/{self.max_health}")
    print(f"  Attack    : {self.attack}")
    print(f"  Defense   : {self.defense}")
    if self.mana > 0:
      print(f"  Mana      : {self.mana}/100")
    print(f"  Gold      : {self.gold}")
    print(f"  Potions   : {self.potions}")
    print(f"  Kills     : {self.kills}")
    print(f"  Reputation: {self.reputation} ({get_reputation_title(self.reputation)})")
    divider()

# ===== ENEMY CLASS =====
class Enemy:
  def __init__(self, name, health, attack, defense, xp, gold):
    self.name = name
    self.max_health = health
    self.health = health
    self.attack = attack
    self.defense = defense
    self.xp = xp
    self.gold = gold
    self.status_effects = {}

  def take_damage(self, damage):
    self.health = max(0, self.health - damage)
    if self.health <= 0:
      print(f"  💀 {self.name} has been defeated!")

  def attack_player(self, player):
    damage = self.attack
    damage = random.randint(int(damage * 0.8), int(damage * 1.2))
    damage = max(0, damage - player.defense)
    player.take_damage(damage)

# ===== ENEMY GENERATION =====
ENEMY_TEMPLATES = {
  "Goblin 👹": {"health": 40, "attack": 10, "defense": 2, "xp": 20, "gold": 10},
  "Wolf 🐺": {"health": 50, "attack": 12, "defense": 3, "xp": 25, "gold": 8},
  "Bandit 🦹": {"health": 60, "attack": 14, "defense": 4, "xp": 30, "gold": 20},
  "Scorpion 🦂": {"health": 65, "attack": 16, "defense": 5, "xp": 35, "gold": 15},
  "Sand Wraith 👻": {"health": 55, "attack": 18, "defense": 3, "xp": 40, "gold": 18},
  "Desert Bandit 🦹": {"health": 75, "attack": 17, "defense": 6, "xp": 38, "gold": 25},
  "Fire Imp 😈": {"health": 70, "attack": 20, "defense": 5, "xp": 45, "gold": 20},
  "Lava Golem 🪨": {"health": 100, "attack": 22, "defense": 10, "xp": 60, "gold": 30},
  "Phoenix Hawk 🦅": {"health": 80, "attack": 24, "defense": 7, "xp": 55, "gold": 28},
  "Skeleton ☠️": {"health": 90, "attack": 25, "defense": 8, "xp": 65, "gold": 35},
  "Zombie 🧟": {"health": 110, "attack": 20, "defense": 9, "xp": 60, "gold": 30},
  "Dark Knight ⚫": {"health": 120, "attack": 28, "defense": 12, "xp": 80, "gold": 50},
}

BOSS_TEMPLATES = {
  "Forest Troll 👾": {"health": 180, "attack": 22, "defense": 8, "xp": 120, "gold": 80},
  "Sand Wyrm 🐍": {"health": 220, "attack": 28, "defense": 10, "xp": 160, "gold": 100},
  "Dragon 🐉": {"health": 300, "attack": 35, "defense": 15, "xp": 250, "gold": 200},
  "Lich King 💀": {"health": 400, "attack": 40, "defense": 18, "xp": 400, "gold": 350},
}

def scale_enemy(template, player_level):
  multiplier = 1 + (player_level - 1) * 0.1
  return {
    "health": int(template["health"] * multiplier),
    "attack": int(template["attack"] * multiplier),
    "defense": int(template["defense"] * multiplier),
    "xp": int(template["xp"] * multiplier),
    "gold": int(template["gold"] * multiplier),
  }

def generate_zone_enemy(player):
  zone_data = ZONES[player.zone]
  enemies_list = zone_data["enemies"]
  if not enemies_list:
    enemies_list = list(ENEMY_TEMPLATES.keys())
  enemy_name = random.choice(enemies_list)
  t = scale_enemy(ENEMY_TEMPLATES[enemy_name], player.level)
  return Enemy(enemy_name, t["health"], t["attack"], t["defense"], t["xp"], t["gold"])

# ===== COMBAT =====
def combat(player, enemy, is_boss=False):
  title(f"⚔️  COMBAT — {player.name} vs {enemy.name}")
  enemy_dialogue(enemy)

  while player.health > 0 and enemy.health > 0:
    # Status effects
    apply_status_effects(player)
    apply_status_effects(enemy)

    if player.health <= 0:
      break

    # Show health bars
    divider()
    print(f"  {player.name}: {health_bar(player.health, player.max_health)}")
    print(f"  {enemy.name}: {health_bar(enemy.health, enemy.max_health)}")
    divider()

    # Player turn (skip if frozen or stunned)
    if "freeze" in player.status_effects or "stun" in player.status_effects:
      print(f"  ❄️  {player.name} can't move!")
    else:
      print("  1. ⚔️  Attack")
      print("  2. 🌟  Special Ability")
      print("  3. 🧪  Use Potion")
      print("  4. 🏃  Flee")
      divider()
      action = input("  Action: ").strip()

      if action == "1":
        damage = player.attack + player.weapon["bonus_attack"]
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        damage = max(0, damage - enemy.defense)
        if "rage" in player.status_effects:
          damage = int(damage * 1.5)
          print("  😡 Rage boost!")
        enemy.take_damage(damage)
        print(f"  ⚔️  {player.name} hits {enemy.name} for {damage} damage!")
        # Random status on attack
        apply_status(enemy, "poison", 3, 0.1)

      elif action == "2":
        player.special_ability(enemy)

      elif action == "3":
        player.use_potion()

      elif action == "4":
        if random.random() < 0.4:
          print("  🏃 You successfully fled!")
          return "flee"
        else:
          print("  ❌ Couldn't escape!")

      else:
        print("  ❌ Invalid action!")

    if enemy.health <= 0:
      break

    # Enemy turn
    if "freeze" in enemy.status_effects or "stun" in enemy.status_effects:
      print(f"  ❄️  {enemy.name} can't move!")
    else:
      enemy.attack_player(player)
      dmg_dealt = enemy.attack - player.defense
      print(f"  💢 {enemy.name} attacks {player.name}!")
      # Random status from enemy
      apply_status(player, "poison", 2, 0.08)

    pause()

  if player.health > 0:
    print(f"\n  ✅ {enemy.name} defeated!")
    player.kills += 1
    player.gain_xp(enemy.xp)
    player.gold += enemy.gold
    print(f"  💰 +{enemy.gold} gold!")
    if is_boss:
      change_reputation(player, 10, "Defeated a boss")
    check_quests(player)
    player.status_effects = {}
    return "win"
  else:
    print("\n  💀 You were defeated...")
    player.status_effects = {}
    return "lose"

# ===== STATUS EFFECTS =====
def apply_status_effects(entity):
  effects_to_remove = []
  for effect, turns in entity.status_effects.items():
    if effect == "poison":
      dmg = 5
      entity.health -= dmg
      print(f"  ☠️  {entity.name} takes {dmg} poison damage!")
    elif effect == "burn":
      dmg = 8
      entity.health -= dmg
      print(f"  🔥 {entity.name} takes {dmg} burn damage!")
    elif effect == "freeze":
      print(f"  🧊 {entity.name} is frozen!")
    elif effect == "stun":
      print(f"  ⚡ {entity.name} is stunned!")
    elif effect == "rage":
      print(f"  😡 {entity.name} is enraged! (+50% damage)")
    elif effect == "shield":
      print(f"  🛡️  {entity.name} is shielded!")

    entity.status_effects[effect] -= 1
    if entity.status_effects[effect] <= 0:
      effects_to_remove.append(effect)

  for effect in effects_to_remove:
    del entity.status_effects[effect]
    print(f"  ✨ {effect.capitalize()} effect wore off!")

def apply_status(target, effect, turns, chance=0.3):
  if random.random() < chance:
    target.status_effects[effect] = turns
    icons = {
      "poison": "☠️",
      "burn": "🔥",
      "freeze": "🧊",
      "stun": "⚡",
      "rage": "😡",
      "shield": "🛡️"
    }
    icon = icons.get(effect, "🔮")
    print(f"  {icon} {target.name} is now {effect}ed for {turns} turns!")

# ===== QUEST SYSTEM =====
def check_quests(player):
  for quest in QUESTS:
    if quest["id"] in player.completed_quests:
      continue
    if "goal_kills" in quest and player.kills >= quest["goal_kills"]:
      complete_quest(player, quest)
    elif "goal_level" in quest and player.level >= quest["goal_level"]:
      complete_quest(player, quest)

def complete_quest(player, quest):
  player.completed_quests.append(quest["id"])
  player.gain_xp(quest["reward_xp"])
  player.gold += quest["reward_gold"]
  print(f"\n  🎉 QUEST COMPLETED: {quest['name']}!")
  print(f"  ✨ +{quest['reward_xp']} XP")
  print(f"  💰 +{quest['reward_gold']} gold")

# ===== RANDOM EVENTS =====
def random_event(player):
  event = weighted_random(RANDOM_EVENTS)
  event_name = event["name"]

  if event_name == "💰 Treasure Chest":
    title("💰 TREASURE CHEST")
    gold = random.randint(30, 100)
    player.gold += gold
    print(f"  You found a treasure chest!")
    print(f"  💰 +{gold} gold!")

  elif event_name == "🧙 Mysterious Merchant":
    title("🧙 MYSTERIOUS MERCHANT")
    print("  A mysterious merchant offers you a rare item...")
    item = random.choice(SHOP_ITEMS["special"])
    print(f"  🎁 You received {item['name']}!")
    player.inventory.append(item)

  elif event_name == "⚗️ Magic Fountain":
    title("⚗️ MAGIC FOUNTAIN")
    heal_amount = random.randint(20, 50)
    player.health = min(player.max_health, player.health + heal_amount)
    print(f"  You find a glowing fountain...")
    print(f"  You drink from it and feel restored!")
    print(f"  +{heal_amount} HP ❤️  ({player.health}/{player.max_health})")

  elif event_name == "🪤 Trap":
    title("🪤 TRAP!")
    damage = random.randint(10, 30)
    player.health = max(1, player.health - damage)
    print(f"  You step on a hidden trap!")
    print(f"  -{damage} HP 💢  ({player.health}/{player.max_health})")

  elif event_name == "📦 Supply Crate":
    title("📦 SUPPLY CRATE")
    potion = random.choice(SHOP_ITEMS["potions"])
    player.inventory.append(potion)
    print(f"  You find an abandoned crate!")
    print(f"  +1 {potion['name']} added to inventory 🎒")

  elif event_name == "🌟 Blessing":
    title("🌟 BLESSING")
    xp_gain = random.randint(20, 60)
    player.gain_xp(xp_gain)
    print(f"  A divine light surrounds you...")
    print(f"  +{xp_gain} XP ✨")

  elif event_name == "👻 Ambush":
    title("👻 AMBUSH!")
    print("  You've been ambushed by multiple enemies!\n")
    time.sleep(1)
    for i in range(2):
      if player.health <= 0:
        break
      enemy_name = random.choice(list(ENEMY_TEMPLATES.keys()))
      t = scale_enemy(ENEMY_TEMPLATES[enemy_name], player.level)
      enemy = Enemy(enemy_name, t["health"], t["attack"], t["defense"], t["xp"], t["gold"])
      print(f"\n  ⚔️  Enemy {i+1}: {enemy.name} appears!")
      time.sleep(0.8)
      combat(player, enemy)

  else:
    enemy = generate_zone_enemy(player)
    combat(player, enemy)

  divider()
  pause()

def weighted_random(items):
  total_weight = sum(item["weight"] for item in items)
  rand_val = random.uniform(0, total_weight)
  weight_sum = 0
  for item in items:
    weight_sum += item["weight"]
    if rand_val <= weight_sum:
      return item
  return items[-1]

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

    weapons = [i for i in player.inventory if "bonus_attack" in i]
    armors = [i for i in player.inventory if "bonus_defense" in i]

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

    idx = int(choice) - 1
    all_equippable = weapons + armors

    if idx < 0 or idx >= len(all_equippable):
      print("  ❌ Invalid choice.")
      continue

    item = all_equippable[idx]

    if "bonus_attack" in item:
      player.weapon = {"name": item["name"], "bonus_attack": item["bonus_attack"]}
      print(f"  ✅ Equipped {item['name']}!")
    elif "bonus_defense" in item:
      player.armor = {"name": item["name"], "bonus_defense": item["bonus_defense"]}
      player.defense = player.defense - player._armor_bonus + item["bonus_defense"]
      player._armor_bonus = item["bonus_defense"]
      print(f"  ✅ Equipped {item['name']}!")

    pause()

# ===== SHOP =====
def show_shop(player):
  while True:
    title("🏪  SHOP")
    print(f"  💰 Gold: {player.gold}")
    rep_title = get_reputation_title(player.reputation)
    print(f"  🏅 Reputation: {rep_title} ({player.reputation}/100)")
    divider()

    all_items = []
    categories = ["weapons", "armor", "potions", "special"]
    cat_labels = {"weapons": "⚔️  WEAPONS", "armor": "🛡️  ARMOR", "potions": "🧪  POTIONS", "special": "🌟  SPECIAL"}

    idx = 1
    for cat in categories:
      print(f"  {cat_labels[cat]}:")
      for item in SHOP_ITEMS[cat]:
        final_price = get_shop_price(player, item["price"])
        if final_price is None:
          print(f"    {idx}. {item['name']} — REFUSED")
        else:
          print(f"    {idx}. {item['name']} — {final_price}g")
        all_items.append((item, cat))
        idx += 1
      divider()

    print("  0. 🚪  Back")
    divider()

    choice = input("  Buy: ").strip()

    if choice == "0":
      break

    if not choice.isdigit():
      print("  ❌ Invalid choice.")
      continue

    item_idx = int(choice) - 1
    if item_idx < 0 or item_idx >= len(all_items):
      print("  ❌ Invalid choice.")
      continue

    item, cat = all_items[item_idx]
    final_price = get_shop_price(player, item["price"])

    if final_price is None:
      print("  ❌ The shopkeeper refuses to sell to you!")
      pause()
      continue

    if player.gold < final_price:
      print("  ❌ Not enough gold!")
      pause()
      continue

    print(f"  You bought {item['name']} for {final_price} gold!")
    player.gold -= final_price

    if "bonus_attack" in item:
      player.weapon = {"name": item["name"], "bonus_attack": item["bonus_attack"]}
      print(f"  ✅ Equipped {item['name']}!")
    elif "bonus_defense" in item:
      player.armor = {"name": item["name"], "bonus_defense": item["bonus_defense"]}
      player.defense = player.defense - player._armor_bonus + item["bonus_defense"]
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
      print(f"  ✅ Lucky Charm! (Luck: {player.luck:.1f})")

    pause()

def get_shop_price(player, base_price):
  rep = player.reputation
  if rep >= 51:
    return int(base_price * 0.8)
  elif rep >= 11:
    return int(base_price * 0.9)
  elif rep <= -51:
    return None
  elif rep <= -11:
    return int(base_price * 1.1)
  else:
    return base_price

# ===== ZONES =====
def show_zones(player):
  while True:
    title("🗺️  ZONES")
    print(f"  Current Zone: {player.zone}")
    print(f"  Level: {player.level}")
    divider()

    for i, (zone_name, zone_data) in enumerate(ZONES.items(), 1):
      if player.level >= zone_data["required_level"]:
        print(f"  {i}. {zone_name} - {zone_data['description']}")
      else:
        print(f"  {i}. {zone_name} - {zone_data['description']} (Requires level {zone_data['required_level']})")

    print("  0. 🚪  Back")
    divider()

    choice = input("  Zone: ").strip()

    if choice == "0":
      break

    if not choice.isdigit():
      print("  ❌ Invalid choice!")
      continue

    idx = int(choice) - 1
    if idx < 0 or idx >= len(ZONES):
      print("  ❌ Invalid choice!")
      continue

    chosen = list(ZONES.keys())[idx]
    if player.level >= ZONES[chosen]["required_level"]:
      player.zone = chosen
      print(f"  🗺️  You traveled to {chosen}!")
    else:
      print(f"  ❌ You need to be level {ZONES[chosen]['required_level']} to enter {chosen}!")

    pause()

# ===== DIALOGUES =====
def npc_dialogue(player, location):
  dialogues = {
    "village": [
      "🧓 Old Man: 'Be careful out there, the forest is dangerous...'",
      "👧 Girl: 'I heard there's treasure hidden in the dungeon!'",
      "💂 Guard: 'Stay out of trouble, adventurer.'",
    ],
    "forest": [
      "🧝 Elf: 'The deeper you go, the darker it gets...'",
      "🍄 Mushroom Fairy: 'Lost? Follow the glowing mushrooms!'",
      "🪓 Woodcutter: 'I saw something huge move between the trees last night.'",
    ],
    "desert": [
      "🧙 Mystic: 'The sands hide many secrets... and dangers.'",
      "🐫 Merchant: 'Water is more valuable than gold out here.'",
    ],
    "volcano": [
      "🔥 Fire Spirit: 'The lava flows with a will of its own...'",
      "🌋 Geologist: 'This volcano is unusually active...'",
    ],
    "dungeon": [
      "💀 Ghost: 'Turn back... while you still can...'",
      "⛓️ Prisoner: 'Please, get me out of here!'",
      "🧙 Old Wizard: 'The boss ahead is weak to magic, remember that.'",
    ],
  }

  rep = player.reputation
  if rep >= 100:
    print("\n  ✨ Everyone bows as you walk by...")
  elif rep <= -50:
    print("\n  😨 People step away as you approach...")

  if location in dialogues:
    line = random.choice(dialogues[location])
    print(f"\n{line}")
  else:
    print("\n🧍 Stranger: 'I have nothing to say to you.'")

def enemy_dialogue(enemy):
  dialogues = {
    "Goblin": "  👺 Goblin: \"Hehehe... you look tasty!\"",
    "Wolf": "  🐺 Wolf: \"Growl!\"",
    "Bandit": "  🦹 Bandit: \"Hand over your gold!\"",
    "Scorpion": "  🦂 Scorpion: \"Hisssss...\"",
    "Sand": "  👻 Sand Wraith: \"Your soul will be mine...\"",
    "Desert": "  🦹 Desert Bandit: \"This is my territory!\"",
    "Fire": "  😈 Fire Imp: \"Burn, mortal!\"",
    "Lava": "  🪨 Lava Golem: \"Crush...\"",
    "Phoenix": "  🦅 Phoenix Hawk: \"Screech!\"",
    "Skeleton": "  💀 Skeleton: \"YOHOHOHO\"",
    "Zombie": "  🧟 Zombie: \"Brains...\"",
    "Dark": "  🗡️ Dark Knight: \"Your soul belongs to me.\"",
    "Forest": "  👾 Forest Troll: \"Me smash!\"",
    "Sand Wyrm": "  🐍 Sand Wyrm: \"Hissss...\"",
    "Dragon": "  🐉 Dragon: \"You dare challenge me?!\"",
    "Lich": "  💀 Lich King: \"Your soul will serve me forever...\"",
  }

  name = enemy.name.split(" ")[0]
  line = dialogues.get(name, f"  ⚔️  {enemy.name}: \"Prepare to fight!\"")
  print(f"\n{line}")
  pause("  Press Enter to begin combat...")

# ===== REPUTATION =====
def change_reputation(player, amount, reason=""):
  player.reputation = max(-100, min(100, player.reputation + amount))
  if amount > 0:
    print(f"  📈 Reputation +{amount} ({reason})")
  else:
    print(f"  📉 Reputation {amount} ({reason})")
  print(f"  → {get_reputation_title(player.reputation)} ({player.reputation}/100)")

def get_reputation_title(rep):
  if rep >= 51:
    return "Legend"
  elif rep >= 11:
    return "Hero"
  elif rep <= -51:
    return "Villain"
  elif rep <= -11:
    return "Outlaw"
  else:
    return "Adventurer"

# ===== QUESTS =====
def show_quests(player):
  title("📜  QUESTS")
  print(f"  Completed: {len(player.completed_quests)}/{len(QUESTS)}")
  divider()

  for quest in QUESTS:
    status = "✅ Completed" if quest["id"] in player.completed_quests else "❌ Not started"
    print(f"  {status} {quest['name']}")
    print(f"    {quest['description']}")
    if "goal_kills" in quest:
      print(f"    Progress: {player.kills}/{quest['goal_kills']} kills")
    elif "goal_level" in quest:
      print(f"    Progress: {player.level}/{quest['goal_level']} level")
    divider()

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

def load_game(slot):
  try:
    with open(slot, "r") as f:
      data = json.load(f)
    player = Player(data["name"], data["player_class"])
    player.__dict__.update(data)
    print(f"  ✅ Game loaded from {slot}!")
    return player
  except FileNotFoundError:
    print(f"  ❌ No save found in {slot}.")
    return None
  except Exception as e:
    print(f"  ❌ Error loading: {e}")
    return None

# ===== PLAYER CREATION =====
def create_player(player_number=1):
  title(f"🧑  CREATE PLAYER {player_number}")
  name = input("  Enter your name: ").strip()
  if not name:
    name = f"Hero{player_number}"

  divider()
  print("  Choose your class:")
  print("  1. ⚔️  Warrior  — High HP & defense")
  print("  2. 🔮  Mage     — High damage & mana")
  print("  3. 🗡️  Assassin — Fast & critical hits")
  print("  4. 🏹  Ranger   — Balanced stats")
  divider()

  classes = {"1": "Warrior", "2": "Mage", "3": "Assassin", "4": "Ranger"}
  choice = input("  Class: ").strip()
  player_class = classes.get(choice, "Ranger")

  player = Player(name, player_class)
  player.gold = 50
  print(f"\n  ✅ {name} the {player_class} created!")
  pause()
  return player

def setup_player(player_number=1):
  title(f"👤  PLAYER {player_number} SETUP")
  print("  1. 🆕  New Game")
  print("  2. 💾  Load Game")
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

# ===== MAIN MENU =====
def show_menu(player):
  title(f"🏡  VILLAGE — {player.name} (Lvl {player.level})")
  print(f"  HP  : {player.health}/{player.max_health}")
  print(f"  Gold: {player.gold}")
  print(f"  Zone: {player.zone}")
  divider()
  print("  1. 🗺️  Travel to a new zone")
  print("  2. 📊  View stats")
  print("  3. 🎒  Inventory")
  print("  4. 🏪  Shop")
  print("  5. 📜  Quests")
  print("  6. 💾  Save Game")
  print("  7. 🚪  Quit")
  divider()

# ===== SINGLE PLAYER LOOP =====
def single_player_loop(player):
  print("\n📍 You arrive in the village...")
  npc_dialogue(player, "village")
  pause()

  while True:
    show_menu(player)
    choice = input("  Action: ").strip()

    if choice == "1":
      show_zones(player)
      if player.zone != "Village 🏘️":
        random_event(player)
        player.zone = "Village 🏘️"

    elif choice == "2":
      player.show_stats()
      pause()

    elif choice == "3":
      show_inventory(player)

    elif choice == "4":
      show_shop(player)

    elif choice == "5":
      show_quests(player)
      pause()

    elif choice == "6":
      save_game(player)
      pause()

    elif choice == "7":
      print("  👋 Goodbye!")
      break

    else:
      print("  ❌ Invalid choice.")

# ===== MULTIPLAYER =====
def show_menu_multi():
  title("🏡  VILLAGE — MULTIPLAYER")
  print("  1. 🗺️  Travel to a new zone")
  print("  2. 📊  View stats")
  print("  3. 🎒  Inventory")
  print("  4. 🏪  Shop")
  print("  5. 📜  Quests")
  print("  6. 💾  Save Game")
  print("  7. 🤼  PvP Duel")
  print("  8. 🚪  Quit")
  divider()

def pvp_duel(player1, player2):
  title(f"🤼  PVP — {player1.name} vs {player2.name}")
  p1 = player1
  p2 = player2

  while p1.health > 0 and p2.health > 0:
    divider()
    print(f"  {p1.name}: {health_bar(p1.health, p1.max_health)}")
    print(f"  {p2.name}: {health_bar(p2.health, p2.max_health)}")
    divider()

    for attacker, defender in [(p1, p2), (p2, p1)]:
      if attacker.health <= 0 or defender.health <= 0:
        break
      print(f"\n  {attacker.name}'s turn!")
      print("  1. ⚔️  Attack")
      print("  2. 🌟  Special")
      print("  3. 🧪  Potion")
      action = input("  Action: ").strip()

      if action == "1":
        damage = attacker.attack + attacker.weapon["bonus_attack"]
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        damage = max(0, damage - defender.defense)
        defender.take_damage(damage)
        print(f"  ⚔️  {attacker.name} hits {defender.name} for {damage} damage!")
      elif action == "2":
        attacker.special_ability(defender)
      elif action == "3":
        attacker.use_potion()
      pause()

  if p1.health > 0:
    print(f"\n  🏆 {p1.name} wins the duel!")
    change_reputation(p1, 5, "Won a duel")
  else:
    print(f"\n  🏆 {p2.name} wins the duel!")
    change_reputation(p2, 5, "Won a duel")
  pause()

def multi_player_loop(player1, player2):
  print("\n📍 You arrive in the village...")
  npc_dialogue(player1, "village")

  while True:
    show_menu_multi()
    choice = input("  Action: ").strip()

    if choice == "1":
      show_zones(player1)
      if player1.zone != "Village 🏘️":
        random_event(player1)
        player1.zone = "Village 🏘️"

    elif choice == "2":
      player1.show_stats()
      player2.show_stats()
      pause()

    elif choice == "3":
      show_inventory(player1)

    elif choice == "4":
      show_shop(player1)

    elif choice == "5":
      show_quests(player1)
      pause()

    elif choice == "6":
      save_game(player1)
      save_game(player2)
      pause()

    elif choice == "7":
      pvp_duel(player1, player2)

    elif choice == "8":
      print("  👋 Goodbye!")
      break

    else:
      print("  ❌ Invalid choice.")

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
