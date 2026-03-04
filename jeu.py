import random
import json


# ===== CLASSE ENNEMI =====
class Ennemi:
  def __init__(self, nom, sante, attaque, defense, xp, or_):
    self.nom = nom
    self.sante = sante
    self.sante_max = sante
    self.attaque = attaque
    self.defense = defense
    self.xp = xp
    self.or_ = or_

  def subir_degats(self, degats):
    self.sante -= degats
    self.sante = max(0, self.sante)

  def attaquer(self, joueur):
    degats = random.randint(self.attaque - 3, self.attaque + 3)
    degats -= joueur.defense
    degats = max(0, degats)
    joueur.subir_degats(degats)
    print(f"{self.nom} attaque {joueur.nom} pour {degats} dégâts !")


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
    self.zone = "Forêt 🌲"
    self.arme = {
      "nom": "Épée rouillée 🗡️",
      "bonus_attaque": 2
    }

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

  def subir_degats(self, degats):
    self.sante -= degats
    self.sante = max(0, self.sante)

  def attaquer_ennemi(self, ennemi):
    critique = random.random() < 0.2
    attaque_totale = self.attaque + self.arme["bonus_attaque"]
    degats = random.randint(attaque_totale - 3, attaque_totale + 3)
    degats -= ennemi.defense

    if critique:
      degats *= 2
      print("💥 COUP CRITIQUE !")

    degats = max(0, degats)
    ennemi.subir_degats(degats)
    print(f"{self.nom} attaque {ennemi.nom} pour {degats} dégâts !")

  def capacite_speciale(self, ennemi):
    print("\n✨ CAPACITÉ SPÉCIALE ✨")

    if self.classe == "Guerrier":
      degats = (self.attaque + self.arme["bonus_attaque"]) * 2
      degats -= ennemi.defense
      degats = max(0, degats)
      ennemi.subir_degats(degats)
      print(f"💥 Coup Puissant ! {degats} dégâts infligés !")

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
      degats -= ennemi.defense
      degats = max(0, degats)
      ennemi.subir_degats(degats)
      print(f"🗡️ Attaque Furtive ! {degats} dégâts infligés !")

  def utiliser_potion(self):
    if self.potions > 0:
      soin = 30
      self.sante = min(self.sante_max, self.sante + soin)
      self.potions -= 1
      print(f"{self.nom} récupère {soin} PV !")
    else:
      print("❌ Plus de potion !")

  def gagner_xp(self, montant):
    self.xp += montant
    print(f"Vous gagnez {montant} XP !")

    while self.xp >= 100:
      self.xp -= 100
      self.monter_niveau()

  def monter_niveau(self):
    self.niveau += 1
    self.sante_max += 20
    self.attaque += 5
    self.defense += 2
    self.sante = self.sante_max
    if self.mana > 0:
      self.mana += 10
    print(f"🎉 Niveau {self.niveau} atteint !")


# ===== GÉNÉRATION ENNEMI =====
def generer_ennemi(joueur):
  niveau = joueur.niveau
  return Ennemi(
    "Gobelin 👹",
    50 + niveau * 15,
    8 + niveau * 3,
    3 + niveau,
    40 + niveau * 10,
    20 + niveau * 5
  )


def generer_boss(joueur):
  niveau = joueur.niveau
  return Ennemi(
    "Dragon 🐉",
    150 + niveau * 30,
    15 + niveau * 5,
    5 + niveau * 2,
    150 + niveau * 30,
    100 + niveau * 20
  )


# ===== COMBAT =====
def combat(joueur, ennemi):
  print(f"\n⚔️ Combat contre {ennemi.nom} !")

  while joueur.sante > 0 and ennemi.sante > 0:
    print(f"\n{joueur.nom}: {joueur.sante} PV")
    print(f"{ennemi.nom}: {ennemi.sante} PV")

    print("\n1. Attaquer")
    print("2. Capacité spéciale")
    print("3. Potion")

    choix = input("Action : ")

    if choix == "1":
      joueur.attaquer_ennemi(ennemi)
    elif choix == "2":
      joueur.capacite_speciale(ennemi)
    elif choix == "3":
      joueur.utiliser_potion()
    else:
      print("❌ Choix invalide.")
      continue

    if ennemi.sante > 0:
      ennemi.attaquer(joueur)

  if joueur.sante > 0:
    print(f"\n✅ {ennemi.nom} vaincu !")
    joueur.gagner_xp(ennemi.xp)
    joueur.or_ += ennemi.or_
    print(f"Vous gagnez {ennemi.or_} or !")
    return True
  else:
    print("\n💀 Vous êtes mort...")
    return False


# ===== MENU =====
def afficher_menu():
  print("\n=== MENU ===")
  print("1. Explorer")
  print("2. Statistiques")
  print("3. Sauvegarder")
  print("4. Quitter")


# ===== SAUVEGARDE =====
def sauvegarder(joueur):
  with open("sauvegarde.json", "w") as f:
    json.dump(joueur.__dict__, f, indent=2, ensure_ascii=False)
  print("💾 Sauvegarde réussie !")


def charger():
  try:
    with open("sauvegarde.json", "r") as f:
      data = json.load(f)

    joueur = Joueur(data["nom"], data["classe"])
    joueur.__dict__.update(data)
    print("✅ Partie chargée !")
    return joueur

  except FileNotFoundError:
    print("⚠️ Aucune sauvegarde trouvée.")
    return None

  except json.JSONDecodeError:
    print("⚠️ Fichier corrompu.")
    return None



# ===== MAIN =====
def main():
  print("Bienvenue dans l'Aventure Ultime 🗡️")

  print("1. Nouvelle partie")
  print("2. Charger")

  choix = input("Choix : ")

  if choix == "2":
    joueur = charger()
    if not joueur:
      return
  else:
    nom = input("Nom : ")
    print("1. Guerrier\n2. Mage\n3. Assassin")
    c = input("Classe : ")
    classes = {"1": "Guerrier", "2": "Mage", "3": "Assassin"}
    joueur = Joueur(nom, classes.get(c, "Guerrier"))

  while joueur.sante > 0:
    afficher_menu()
    choix = input("Action : ")

    if choix == "1":
      ennemi = generer_boss(joueur) if random.random() < 0.2 else generer_ennemi(joueur)
      if not combat(joueur, ennemi):
        break
    elif choix == "2":
      joueur.afficher_stats()
    elif choix == "3":
      sauvegarder(joueur)
    elif choix == "4":
      break
    else:
      print("❌ Choix invalide.")

  print("Fin du jeu 👋")


if __name__ == "__main__":
  main()
