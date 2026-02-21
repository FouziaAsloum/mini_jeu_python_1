# === Mini jeu d'aventure ===

def afficher_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Explorer")
    print("2. Voir le personnage")
    print("3. Quitter")

class Player:
    def __init__(self, nom):
        self.nom = nom
        self.vie = 100
        self.attaque = 10

    def afficher_stats(self):
        print("=== STATS DU PERSONNAGE ===")
        print("Nom :", self.nom)
        print("Vie :", self.vie)
        print("Attaque :", self.attaque)
        
    def attaquer(self, ennemi):
      print(self.nom, "attaque", ennemi.nom, "!")
      ennemi.vie -= self.attaque
      print(ennemi.nom, "perd", self.attaque, "points de vie.")

        
class Enemy:
    def __init__(self, nom, vie, attaque):
        self.nom = nom
        self.vie = vie
        self.attaque = attaque

    def afficher_stats(self):
        print("=== ENNEMI ===")
        print("Nom :", self.nom)
        print("Vie :", self.vie)
        print("Attaque :", self.attaque)


def main():
    print("Bienvenue dans le jeu 🗡️")
    nom_joueur = input("Choisis ton nom : ")
    joueur = Player(nom_joueur)


    while True:
        afficher_menu()
        choix = input("Que veux-tu faire ? ")

        if choix == "1":
            print("Tu pars explorer...")
            ennemi = Enemy("Gobelin", 50, 5)
            ennemi.afficher_stats()
    
            joueur.attaquer(ennemi)
            print("Vie restante de l'ennemi :", ennemi.vie)


        elif choix == "2":
          joueur.afficher_stats()
        elif choix == "3":
            print("À bientôt 👋")
            break
        else:
            print("Choix invalide.")

main()
