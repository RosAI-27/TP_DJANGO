# TP : API de réservation de salles

> **À compléter par votre groupe avant le dernier push.**

## Groupe

| Membre | Compte GitHub | Rôle / tâches principales |
|--------|---------------|---------------------------|
| Rose Ange BAPFUBUSA SIAPZE| https://github.com/RosAI-27/TP_DJANGO           | TP Complet                       |

## Installation

bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver


Comptes de test (mot de passe : motdepasse123) : alice, bob, charlie.
Super-utilisateur : admin / admin123.

## Endpoints

> À compléter : listez les routes de votre API, les méthodes autorisées et qui a le droit de les appeler.

| Route | Méthodes | Permissions |
|-------|----------|-------------|
| /api/salles/ | GET | Accès public |
| /api/salles/ | POST | Administrateurs uniquement (IsAdminUser) |
| /api/salles/{id}/ | GET | Accès public |
| /api/salles/{id}/ | PUT, PATCH, DELETE | Administrateurs uniquement (IsAdminUser) |
| /api/salles/{id}/occupation/ | GET | Accès public |
| /api/reservations/ | GET | Accès public |
| /api/reservations/ | POST | Utilisateurs authentifiés (IsAuthenticated) |
| /api/reservations/{id}/ | GET | Accès public |
| /api/reservations/{id}/ | PUT, PATCH, DELETE | Propriétaire de la réservation uniquement (IsOwnerOrReadOnly) |

## Choix de conception et difficultés rencontrées

> Quelques lignes : comment avez-vous défini le chevauchement ? Qu'est-ce qui vous a posé problème ?

### Définition du chevauchement

Deux réservations pour une même salle se chevauchent si leurs plages horaires s'intersectent. Le chevauchement est vérifié grâce à la condition logique : la nouvelle réservation commence avant la fin de l'existante (debut < fin_existante) ET se termine après le début de l'existante (fin > debut_existante). Dans l'ORM Django, cela s'exprime par 'debut__lt=fin' et fin__gt=debut'. Les bornes exactes étant exclues (< et >), deux réservations consécutives (par exemple de 09h00 à 10h00, puis de 10h00 à 11h00) ne sont pas considérées en conflit.

### Difficultés rencontrées

- 'PATCH' : Lors de la validation dans le serializer, certains champs comme 'debut' ou 'fin' peuvent être absents des données envoyées. Il a fallu récupérer les valeurs existantes via 'self.instance' si elles n'étaient pas fournies.
- Exclusion lors de la modification : Pour éviter qu'une réservation ne bloque sa propre modification lors d'un 'PUT' ou 'PATCH', il a fallu explicitement ajouter '.exclude(pk=instance.pk)' au filtre de recherche de conflits.
- Règles de permissions : Garantir que le champ 'utilisateur' reste en lecture seule tout en l'attribuant automatiquement à l'utilisateur connecté lors de la création via la méthode 'perform_create' du ViewSet.