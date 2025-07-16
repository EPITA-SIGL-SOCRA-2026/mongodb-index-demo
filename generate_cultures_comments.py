import pandas as pd
import random
from faker import Faker
from pathlib import Path

commentaire_templates = [
    "Pousse bien à l'ombre",
    "Excellente en pleine lumière",
    "Rendement élevé cette année",
    "Sensibilité aux maladies",
    "Bonne tenue en sol humide",
    "Pas besoin de beaucoup d'entretien",
    "Besoin en arrosage faible",
    "Fleurs attractives pour les pollinisateurs",
    "Sensible aux gelées tardives",
    "Pousse rapide",
    "Idéale en permaculture",
    "Pas de parasites cette saison",
    "Plante rustique et stable",
    "Très productive",
    "Bonne croissance en sol sableux",
    "Demande beaucoup d’eau",
    "Préférence pour les sols acides",
    "Peu de succès cette année",
    "Problème de limaces",
    "À replanter l’an prochain",
    "Expérience positive dans le jardin",
    "S’adapte bien aux changements météo",
    "A bien supporté la canicule",
    "Croissance lente mais stable",
    "Nécessite un paillage important",
    "Très bonne conservation après récolte",
    "Testée sur différents terrains",
    "Compatible avec les fraisiers",
    "S'est bien développée avec les tomates",
    "Odeur agréable pendant la floraison",
    "Comestible et facile à cuisiner",
    "Utilisée en infusion",
    "Recommandée par d'autres jardiniers",
    "Peu d’entretien nécessaire",
    "A attiré de nombreux insectes",
    "Semis facile",
    "Plante expérimentale cette saison",
    "Nécessite beaucoup de soleil",
    "Bonne interaction avec les abeilles",
    "Utilisée pour fertiliser le sol",
    "Utilisation médicinale locale",
    "Bon rendement en balcon",
    "Plantée à côté des courgettes",
    "Nécessite un tuteurage",
    "Forte croissance en juin",
    "N’a pas survécu à l’hiver",
    "Présente dans le jardin communautaire",
    "Plantée en bac surélevé",
    "Plantation réussie près d’un mur",
]


def generate_cultures_with_comments(nb_jardins, nb_plantes, nb_jardiniers, output_dir):
    faker = Faker("fr_FR")
    Faker.seed(42)
    random.seed(42)

    plante_ids = list(range(1, nb_plantes + 1))
    jardinier_ids = list(range(1, nb_jardiniers + 1))

    cultures = []
    for jardin_id in range(nb_jardins):
        plantes_selected = random.sample(
            plante_ids, random.randint(5, int(nb_plantes / 3))
        )
        for plante_id in plantes_selected:
            # Génération d'un nombre aléatoire de commentaires entre 1 et 30
            # avec 90% de chance d'avoir entre 1 et 5 commentaires

            if random.random() < 0.9:
                # 90% de chance d'avoir entre 1 et 5 commentaires
                nb_comments = random.randint(1, 5)
            else:
                # 10% de chance d'avoir entre 6 et 30 commentaires
                nb_comments = random.randint(6, 30)
            commentaires = []
            for _ in range(nb_comments):
                commentaires.append(
                    {
                        "jardinier_id": random.choice(jardinier_ids),
                        "message": random.choice(commentaire_templates),
                        "date": faker.date_time_between(
                            start_date="-1y", end_date="now"
                        ).isoformat(),
                    }
                )
            cultures.append(
                {
                    "jardin_id": jardin_id,
                    "plante_id": plante_id,
                    "commentaires": commentaires,
                }
            )

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = Path(output_dir) / "commentaires.json"
    pd.DataFrame(cultures).to_json(
        path, orient="records", lines=False, force_ascii=False
    )
    print(f"✅ Fichier généré : {path.absolute()}")


if __name__ == "__main__":

    #  Argparse setup
    import argparse

    parser = argparse.ArgumentParser(
        description="Génère des données de cultures avec des commentaires."
    )

    parser.add_argument(
        "--nb-jardiniers",
        type=int,
        required=True,
        help="Nombre de jardiniers à utiliser pour les commentaires (obligatoire)",
    )

    parser.add_argument(
        "--nb-jardins",
        type=int,
        required=True,
        help="Nombre de jardins à utiliser pour les commentaires (obligatoire)",
    )

    parser.add_argument(
        "--nb-plantes",
        type=int,
        required=True,
        default=157,
        help="Nombre de plantes à utiliser pour les commentaires (obligatoire)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Répertoire de sortie pour les données générées (par défaut: .)",
    )
    args = parser.parse_args()

    generate_cultures_with_comments(
        nb_jardins=args.nb_jardins,
        nb_plantes=args.nb_plantes,
        nb_jardiniers=args.nb_jardiniers,
        output_dir=args.output_dir,
    )
