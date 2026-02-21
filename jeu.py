# === Mini jeu d'aventure ===

def afficher_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Explorer")
    print("2. Voir le personnage")
    print("3. Quitter")

def main():
    print("Bienvenue dans le jeu 🗡️")

    while True:
        afficher_menu()
        choix = input("Que veux-tu faire ? ")

        if choix == "1":
            print("Tu pars explorer...")
        elif choix == "2":
            print("Voici ton personnage.")
        elif choix == "3":
            print("À bientôt 👋")
            break
        else:
            print("Choix invalide.")

main()
