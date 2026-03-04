import random
import json

# ===== CLASSE JOUEUR =====
class Joueur:
  def __init__(self, nom, classe):
    self.nom = nom
    self.classe = classe
    self.niveau = 1
    self.xp = 0
    self.or_ = 0
    self.potions = 2

    if classe == "Guerrier":
      self.sante_max = 120
      self.attaque = 18
      self.defense = 8
      self.mana = 0

    elif classe == "Mage":
      self.sante_max = 80
      self.attaque = 10
      self.defense = 3
      self.mana = 50

    elif classe == "Assassin":
      self.sante_max = 90
      self.attaque = 15
      self.defense = 4
      self.mana = 20

    self.sante = self.sante_max
    self.arme = {
      "nom": "Épée rouillée 🗡️",
      "bonus_attaque": 2
    }
    self.zone = "Forêt 🌲"

  # ----- AFFICHER LES STATS -----
  def afficher_stats(self):
    print("\n===== STATISTIQUES =====")
    print(f"Nom       : {self.nom}")
    print(f"Classe    : {self.classe}")
    print(f"Niveau    : {self.niveau}")
    print(f"XP        : {self.xp}/100")
    print(f"Santé     : {self.sante}/{self.sante_max}")
    print(f"Attaque   : {self.attaque}")
    print(f"Défense   : {self.defense}")
    print(f"Or        : {self.or_}")
    print(f"Potions   : {self.potions}")
    print(f"Arme      : {self.arme['nom']} (+{self.arme['bonus_attaque']} ATK)")
    print(f"Zone      : {self.zone}")
    if self.mana > 0:
      print(f"Mana      : {self.mana}")
    print("========================\n")

  # ----- SUBIR DES DÉGÂTS -----
  def subir_degats(self, degats):
    self.sante -= degats
    self.sante = max(0, self.sante)

  # ----- ATTAQUER UN ENNEMI -----
  def attaquer_ennemi(self, ennemi):
    critique = random.random() < 0.2
    attaque_totale = self.attaque + self.arme["bonus_attaque"]
    degats_base = random.randint(attaque_totale - 3, attaque_totale + 3)
    degats = degats_base - ennemi.defense

    if critique:
      degats *= 2
      print("💥 COUP CRITIQUE !")

    degats = max(0, degats)
    ennemi.subir_degats(degats)
    print(f"{self.nom} attaque {ennemi.nom} pour {degats} dégâts !")

  # ----- CAPACITÉ SPÉCIALE -----
  def capacite_speciale(self, ennemi):
    print("\n✨ CAPACITÉ SPÉCIALE ✨")

    if self.classe == "Guerrier":
      degats = (self.attaque + self.arme["bonus_attaque"]) * 2
      degats -= ennemi.defense
      degats = max(0, degats)
      ennemi.subir_degats(degats)
      print(f"💥 Coup Puissant ! {degats} dégâts infligés !")

      if random.random() < 0.25:
        print("⚡ L'ennemi est étourdi !")
        return "etourdissement"

    elif self.classe == "Mage":
      if self.mana >= 20:
        self.mana -= 20
        degats = random.randint(25, 35)
        ennemi.subir_degats(degats)
        print(f"🔥 Boule de Feu ! {degats} dégâts infligés !")
      else:
        print("❌ Pas assez de mana !")

    elif self.classe == "Assassin":
      degats = (self.attaque + self.arme["bonus_attaque"]) * 2
      ennemi.subir_degats(degats)
      print(f"🗡️ Attaque Furtive ! {degats} dégâts infligés !")

      if random.random() < 0.3:
        print("💨 Vous éviterez la prochaine attaque !")
        return "esquive"

    return None

  # ----- UTILISER UNE POTION -----
  def utiliser_potion(self):
    if self.potions > 0:
      soin = 30
      avant = self.sante
      self.sante = min(self.sante_max, self.sante + soin)
      soin_reel = self.sante - avant
      self.potions -= 1
      print(f"{self.nom} boit une potion et récupère {soin_reel} points de santé !")
    else:
      print("❌ Plus aucune potion !")

  # ----- GAGNER DE L'XP -----
  def gagner_xp(self, montant):
    self.xp += montant
    print(f"Vous gagnez {montant} XP !")

    while self.xp >= 100:
      self.xp -= 100
      self.monter_niveau()

  # ----- MONTER DE NIVEAU -----
  def monter_niveau(self):
    self.niveau += 1
    self.sante_max += 20
    self.attaque += 5
    self.defense += 2
    self.sante = self.sante_max
    print("🎉 NIVEAU SUPÉRIEUR !")
    print(f"Vous êtes maintenant niveau {self.niveau} !")


# ===== CLASSE ENNEMI =====
class Ennemi:
  def __init__(self, nom, sante, attaque, defense, recompense_xp, recompense_or):
    self.nom = nom
    self.sante = sante
    self.attaque = attaque
    self.defense = defense
    self.recompense_xp = recompense_xp
    self.recompense_or = recompense_or

  def subir_degats(self, degats):
    self.sante -= degats
    self.sante = max(0, self.sante)

  def attaquer_joueur(self, joueur):
    degats_base = random.randint(self.attaque - 2, self.attaque + 2)
    degats = degats_base - joueur.defense
    degats = max(0, degats)
    joueur.subir_degats(degats)
    print(f"{self.nom} attaque {joueur.nom} pour {degats} dégâts !")


# ===== GÉNÉRATEUR D'ENNEMIS =====
def generer_ennemi(joueur):
  niveau = joueur.niveau
  zone = joueur.zone

  types_ennemis = [
    {"nom": "Gobelin 👹",   "sante_base": 50, "attaque_base": 8,  "defense_base": 2},
    {"nom": "Orc 💪",       "sante_base": 80, "attaque_base": 12, "defense_base": 4},
    {"nom": "Squelette 💀", "sante_base": 60, "attaque_base": 10, "defense_base": 3}
  ]

  choix = random.choice(types_ennemis)

  if zone == "Forêt 🌲":
    multiplicateur = 1
  elif zone == "Donjon 🏰":
    multiplicateur = 1.5
  else:
    multiplicateur = 2

  sante   = int((choix["sante_base"]   + niveau * 10) * multiplicateur)
  attaque = int((choix["attaque_base"] + niveau * 2)  * multiplicateur)
  defense = int((choix["defense_base"] + niveau)      * multiplicateur)

  recompense_xp = int((30 + niveau * 10) * multiplicateur)
  recompense_or = int((15 + niveau * 5)  * multiplicateur)

  return Ennemi(choix["nom"], sante, attaque, defense, recompense_xp, recompense_or)


# ===== GÉNÉRATEUR DE BOSS =====
def generer_boss():
  return Ennemi("Dragon 🐉", 200, 20, 8, 150, 100)


# ===== SYSTÈME DE COMBAT =====
def combat(joueur, ennemi):
  print(f"\n⚔️ Un {ennemi.nom} apparaît !")

  esquive_prochaine = False

  while ennemi.sante > 0 and joueur.sante > 0:
    print(f"\n❤️  Votre santé    : {joueur.sante}/{joueur.sante_max}")
    print(f"👹 Santé ennemi  : {ennemi.sante}")
    print("1. Attaquer")
    print("2. Utiliser une potion")
    print("3. Capacité spéciale")

    action = input("Action : ")
    etourdissement = False
    effet = None

    if action == "1":
      joueur.attaquer_ennemi(ennemi)

    elif action == "2":
      joueur.utiliser_potion()

    elif action == "3":
      effet = joueur.capacite_speciale(ennemi)

      if effet == "etourdissement":
        etourdissement = True

      elif effet == "esquive":
        esquive_prochaine = True

    else:
      print("❌ Action invalide.")
      continue

    # ----- TOUR DE L'ENNEMI -----
    if ennemi.sante > 0:
      if etourdissement:
        print("⚡ L'ennemi est étourdi et ne peut pas attaquer !")
      elif esquive_prochaine:
        print("💨 Vous esquivez l'attaque ennemie !")
        esquive_prochaine = False
      else:
        ennemi.attaquer_joueur(joueur)

  # ----- FIN DU COMBAT -----
  if joueur.sante > 0:
    print(f"\n✅ {ennemi.nom} vaincu !")
    joueur.or_ += ennemi.recompense_or
    joueur.gagner_xp(ennemi.recompense_xp)
    print(f"Vous gagnez {ennemi.recompense_or} pièces d'or !")
    return True
  else:
    print("\n💀 Vous avez été vaincu...")
    return False


# ===== CHANGER DE ZONE =====
def changer_zone(joueur):
  zones = {
    "1": "Forêt 🌲",
    "2": "Donjon 🏰",
    "3": "Montagne ⛰️"
  }

  print("\n🗺️ Choisissez une zone :")
  for cle, valeur in zones.items():
    print(f"{cle}. {valeur}")

  choix = input("Zone : ")

  if choix in zones:
    joueur.zone = zones[choix]
    print(f"\n✅ Vous êtes maintenant dans : {joueur.zone}")
  else:
    print("❌ Choix invalide.")


# ===== BOUTIQUE =====
def boutique(joueur):
  while True:
    print("\n🏪 Bienvenue dans la boutique !")
    print(f"Or disponible : {joueur.or_} 💰")
    print("1. Acheter une potion (20 or)")
    print("2. Augmenter l'attaque (+3) (50 or)")
    print("3. Augmenter la défense (+2) (50 or)")
    print("4. Quitter la boutique")

    choix = input("Que voulez-vous acheter ? ")

    if choix == "1":
      if joueur.or_ >= 20:
        joueur.or_ -= 20
        joueur.potions += 1
        print("✅ Vous avez acheté une potion ! 🧪")
      else:
        print("❌ Pas assez d'or !")

    elif choix == "2":
      if joueur.or_ >= 50:
        joueur.or_ -= 50
        joueur.attaque += 3
        print("✅ Attaque augmentée ! 🗡️")
      else:
        print("❌ Pas assez d'or !")

    elif choix == "3":
      if joueur.or_ >= 50:
        joueur.or_ -= 50
        joueur.defense += 2
        print("✅ Défense augmentée ! 🛡️")
      else:
        print("❌ Pas assez d'or !")

    elif choix == "4":
      break

    else:
      print("❌ Choix invalide.")


# ===== BOUTIQUE D'ARMES =====
def boutique_armes(joueur):
  armes = [
    {"nom": "Épée en fer ⚔️",    "bonus_attaque": 5,  "prix": 50},
    {"nom": "Grande hache 🪓",    "bonus_attaque": 8,  "prix": 100},
    {"nom": "Lame légendaire 🔥", "bonus_attaque": 15, "prix": 250}
  ]

  print("\n🛒 Boutique d'armes :")
  print(f"Or disponible : {joueur.or_} 💰")
  for i, arme in enumerate(armes):
    print(f"{i+1}. {arme['nom']} (+{arme['bonus_attaque']} ATK) - {arme['prix']} or")

  choix = input("Choisissez une arme (ou 0 pour quitter) : ")

  if choix.isdigit():
    choix = int(choix)

    if choix == 0:
      return

    if 1 <= choix <= len(armes):
      selection = armes[choix - 1]

      if joueur.or_ >= selection["prix"]:
        joueur.or_ -= selection["prix"]
        joueur.arme = {
          "nom": selection["nom"],
          "bonus_attaque": selection["bonus_attaque"]
        }
        print(f"\n✅ Vous avez équipé {selection['nom']} !")
      else:
        print("❌ Pas assez d'or.")
    else:
      print("❌ Choix invalide.")


# ===== SAUVEGARDER LA PARTIE =====
def sauvegarder(joueur):
  donnees = {
    "nom": joueur.nom,
    "classe": joueur.classe,
    "niveau": joueur.niveau,
    "xp": joueur.xp,
    "sante": joueur.sante,
    "sante_max": joueur.sante_max,
    "attaque": joueur.attaque,
    "defense": joueur.defense,
    "or": joueur.or_,
    "potions": joueur.potions,
    "zone": joueur.zone,
    "arme": joueur.arme,
    "mana": joueur.mana
  }

  with open("sauvegarde.json", "w") as fichier:
    json.dump(donnees, fichier, indent=4, ensure_ascii=False)

  print("💾 Partie sauvegardée avec succès !")


# ===== CHARGER LA PARTIE =====
def charger_partie():
  try:
    with open("sauvegarde.json", "r") as fichier:
      donnees = json.load(fichier)

    joueur = Joueur(donnees["nom"], donnees.get("classe", "Guerrier"))
    joueur.niveau    = donnees["niveau"]
    joueur.xp        = donnees["xp"]
    joueur.sante     = donnees["sante"]
    joueur.sante_max = donnees["sante_max"]
    joueur.attaque   = donnees["attaque"]
    joueur.defense   = donnees["defense"]
    joueur.or_       = donnees["or"]
    joueur.potions   = donnees["potions"]
    joueur.zone      = donnees["zone"]
    joueur.arme      = donnees["arme"]
    joueur.mana      = donnees["mana"]

    print("✅ Partie chargée avec succès !")
    return joueur

  except FileNotFoundError:
    print("⚠️ Aucune sauvegarde trouvée.")
    return None

  except json.JSONDecodeError:
    print("⚠️ Fichier de sauvegarde corrompu.")
    return None


# ===== MENU PRINCIPAL =====
def afficher_menu():
  print("\n=== MENU PRINCIPAL ===")
  print("1. Explorer")
  print("2. Statistiques du joueur")
  print("3. Changer de zone")
  print("4. Boutique")
  print("5. Boutique d'armes")
  print("6. Sauvegarder")
  print("7. Charger une sauvegarde")
  print("8. Quitter")


# ===== FONCTION PRINCIPALE =====
def main():
  print("Bienvenue dans l'Aventure Ultime 🗡️")

  joueur = None

  while joueur is None:
    print("\n1. Nouvelle partie")
    print("2. Charger une partie")
    choix_depart = input("Choisissez une option : ")

    if choix_depart == "1":
      nom_joueur = input("Choisissez votre nom : ")
      print("\nChoisissez votre classe :")
      print("1. Guerrier")
      print("2. Mage")
      print("3. Assassin")

      choix_classe = input("Classe : ")

      if choix_classe == "1":
        classe = "Guerrier"
      elif choix_classe == "2":
        classe = "Mage"
      elif choix_classe == "3":
        classe = "Assassin"
      else:
        print("⚠️ Choix invalide, Guerrier sélectionné par défaut.")
        classe = "Guerrier"

      joueur = Joueur(nom_joueur, classe)

    elif choix_depart == "2":
      joueur = charger_partie()

    else:
      print("❌ Choix invalide.")

  while True:
    if joueur.sante <= 0:
      print("\n💀 Game Over.")
      break

    afficher_menu()
    choix = input("Que voulez-vous faire ? ")

    if choix == "1":
      if random.random() < 0.2:
        ennemi = generer_boss()
      else:
        ennemi = generer_ennemi(joueur)

      en_vie = combat(joueur, ennemi)
      if not en_vie:
        break

    elif choix == "2":
      joueur.afficher_stats()

    elif choix == "3":
      changer_zone(joueur)

    elif choix == "4":
      boutique(joueur)

    elif choix == "5":
      boutique_armes(joueur)

    elif choix == "6":
      sauvegarder(joueur)

    elif choix == "7":
      charge = charger_partie()
      if charge:
        joueur = charge

    elif choix == "8":
      print("Au revoir 👋")
      break

    else:
      print("❌ Choix invalide.")


if __name__ == "__main__":
  main()
