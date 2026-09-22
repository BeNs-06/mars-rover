# Plan de réalisation — Simulateur de rover martien (phase Build)

Spécification de référence : intent/mars-rover-simulator/spec.md

## Contexte

`intent/mars-rover-simulator/intent.md` et `intent/mars-rover-simulator/spec.md` sont acceptés. Le spec (EX-01 à EX-11) décrit une cible que le code actuel de `mars_rover/` ne respecte pas encore, comme le documente déjà `CLAUDE.md` :

- **Interface web** au lieu du CLI actuel (EX-01, EX-02, EX-08).
- **Carte à obstacles** avec deux jeux de symboles emoji strictement équivalents et mélangeables (🟩/🟫 libre, 🌳/🪨 obstacle — EX-09/EX-10/EX-11), alors que `PlanetMap` actuel n'a aucune notion d'obstacle, seulement des limites rectangulaires.
- **Blocage qui n'interrompt pas la mission** : un déplacement bloqué (obstacle ou bord de carte) laisse le rover immobile pour cette commande et l'exécution **continue** avec les commandes suivantes (EX-05/EX-06/EX-07), alors que `run_mission` actuel lève `OutOfBoundsError` et **abandonne** toute la mission.
- **Validation préalable** : position de départ hors carte/sur obstacle, ou commande inconnue → message d'erreur, aucune commande exécutée (EX-02).

Décisions validées avec l'utilisateur pour cette phase Build :
- Le CLI actuel (`cli.py`, `__main__.py`, script console `mars-rover`) est **remplacé** par l'interface web — pas de double interface à maintenir, pas de comportement contradictoire au spec à conserver.
- Le web sera construit avec **Flask** (nouvelle dépendance, absente du repo aujourd'hui qui est 100 % stdlib) : un formulaire Jinja2 + une route testable via `app.test_client()`.

Étape 0 (ce document) : enregistrer ce plan dans `intent/mars-rover-simulator/plan.md` et commiter uniquement ce fichier, sur la branche `build/mars-rover-simulator` (créée depuis `main`).

## Fichiers à créer ou modifier

### Domaine (réutilisé tel quel)
- `mars_rover/direction.py` — inchangé (logique de rotation/déplacement générique, déjà conforme).
- `mars_rover/rover.py` — inchangé (`Rover` immuable, `turned_left/right`, `next_position`, `moved_to`).
- `mars_rover/commands.py` — inchangé (`Command`, `parse_commands`, `InvalidCommandError` : la validation en amont de toute exécution est déjà garantie car `parse_commands` construit la liste complète avant que `run_mission` ne commence à l'exécuter).

### Domaine (à réécrire)
- `mars_rover/planet_map.py` :
  - Ajouter un état de case (`CellState` : `FREE`/`OBSTACLE`, ou équivalent simple).
  - Ajouter le mapping de normalisation des symboles : `🟩`, `🟫` → libre ; `🌳`, `🪨` → obstacle (EX-09/EX-10/EX-11).
  - Ajouter un parseur de carte (`PlanetMap.from_rows(rows: list[str])` ou `parse_map(raw: str)`) qui construit la grille, en dérivant `width`/`height` du nombre de colonnes/lignes ; lève une erreur explicite (ex. `InvalidMapError`) sur symbole non reconnu ou carte vide/irrégulière.
  - Garder `Position` et `is_within_bounds` ; ajouter `is_free(position)` (ou `is_obstacle`) qui compose bornes + état de case.
- `mars_rover/simulator.py` :
  - Ajouter une validation préalable explicite (EX-02) : position de départ dans les limites **et** sur case libre (sinon `InvalidStartPositionError` ou équivalent), commandes toutes reconnues (`parse_commands` déjà suffisant). Cette validation doit s'exécuter avant toute exécution — aucune commande n'est appliquée si elle échoue.
  - Réécrire la boucle d'exécution : les rotations s'appliquent sans condition (inchangé) ; pour avancer, si la case cible est hors limites **ou** obstacle, le rover reste immobile pour cette commande et l'exécution **continue** (EX-05/EX-06/EX-07) — plus d'exception qui abandonne la mission.
  - Supprimer `OutOfBoundsError` (le comportement qu'elle portait n'existe plus dans le spec accepté).

### Interface (remplace le CLI)
- Supprimer `mars_rover/cli.py`.
- `mars_rover/__main__.py` : remplacé pour lancer le serveur web (`python -m mars_rover` démarre l'appli Flask) au lieu du CLI argparse.
- `mars_rover/web/app.py` (nouveau) : factory `create_app()` Flask, une route `/` qui :
  - en `GET`, affiche le formulaire (carte, x, y, orientation, commandes) — EX-01 ;
  - en `POST`, valide puis exécute la mission via `mars_rover.simulator`, affiche la position/orientation finales (EX-08) ou un message d'erreur sans rien exécuter en cas d'entrée invalide (EX-02).
- `mars_rover/web/templates/index.html` (nouveau) : template Jinja2 du formulaire + zone de résultat/erreur.
- `mars_rover/__init__.py` : mettre à jour les exports publics (retirer `OutOfBoundsError`, ajouter les nouveaux types de `planet_map`/`simulator`).
- `pyproject.toml` : ajouter la dépendance `flask`, remplacer `[project.scripts] mars-rover = "mars_rover.cli:main"` par un point d'entrée qui lance le serveur web ; inclure le template dans le package (`package-data` ou `include_package_data` pour `mars_rover/web/templates/`).
- `README.md` : réécrire la section usage pour documenter l'interface web (comment lancer le serveur, ce que fait la page) à la place des exemples CLI actuels.

## Ordre de travail

1. **Plan** : écrire `intent/mars-rover-simulator/plan.md` (ce contenu), commit de ce seul fichier sur `build/mars-rover-simulator`.
2. **Carte à obstacles** : réécrire `planet_map.py` (états de case, parsing, normalisation des symboles) + `tests/test_planet_map.py`.
3. **Moteur de simulation** : réécrire `simulator.py` (validation préalable + blocage sans abandon) + `tests/test_simulator.py`.
4. **Interface web** : ajouter `mars_rover/web/` (app Flask + template) + `tests/test_web.py` ; mettre à jour `mars_rover/__main__.py` et `mars_rover/__init__.py`.
5. **Nettoyage** : supprimer `cli.py` et `tests/test_cli.py` (remplacé par `test_web.py`) ; mettre à jour `pyproject.toml` (dépendance Flask, entry point, données de package) et `README.md`.
6. **Vérification** : `pytest` complet, puis lancement réel du serveur web et test manuel du chemin nominal (carte mixte 🟩/🌳/🟫/🪨, blocage par obstacle et par bord de carte, entrée invalide) dans un navigateur.

`direction.py`, `rover.py`, `commands.py` ne bougent pas et n'ont donc pas besoin de nouveaux tests.

## Tests prévus

Style existant conservé : un fichier de test par module, `pytest.mark.parametrize`, pas de `conftest.py` sauf si strictement nécessaire.

- `tests/test_planet_map.py` (réécrit) : parsing d'une carte avec uniquement 🟩/🌳 (EX-09) ; avec uniquement 🟫/🪨 (EX-10) ; avec un mélange des deux jeux, comportement identique à une carte équivalente à jeu unique (EX-11) ; symbole inconnu → erreur ; `is_within_bounds` (conservé) ; `is_free`/`is_obstacle` sur case libre vs obstacle.
- `tests/test_simulator.py` (réécrit) : avancer sur case libre déplace le rover (EX-03, inchangé) ; tourner change l'orientation sans toucher la position (EX-04, inchangé) ; avancer vers un obstacle laisse le rover immobile (EX-05) ; avancer vers l'extérieur de la carte laisse le rover immobile (EX-06) ; une commande bloquée suivie d'autres commandes (ex. tourner puis avancer) — les commandes suivantes s'exécutent normalement (EX-07) ; position de départ hors carte → erreur de validation avant toute exécution (EX-02) ; position de départ sur obstacle → même erreur (EX-02) ; commande inconnue dans la liste → erreur avant toute exécution, aucune commande appliquée (EX-02).
- `tests/test_web.py` (nouveau, remplace `test_cli.py`) via `app.test_client()` : `GET /` affiche le formulaire (EX-01) ; `POST /` avec entrées valides affiche la position/orientation finales (EX-08) ; `POST /` avec position de départ hors carte ou sur obstacle affiche un message d'erreur et aucun résultat de simulation (EX-02) ; `POST /` avec une commande inconnue affiche un message d'erreur (EX-02) ; `POST /` avec une carte 🟩/🌳 pure fonctionne (EX-09) ; avec une carte 🟫/🪨 pure fonctionne (EX-10) ; avec une carte mélangeant les deux jeux, résultat identique à un agencement équivalent à jeu unique (EX-11) ; une commande bloquée suivie d'autres commandes produit le résultat final attendu (EX-07) via le endpoint HTTP.
- `tests/test_direction.py`, `tests/test_rover.py`, `tests/test_commands.py` : inchangés, aucun nouveau cas requis.

## Vérification

- `pytest` (suite complète) doit passer en vert après chaque étape 2 à 5.
- Lancement manuel du serveur web (`python -m mars_rover` ou `flask run`) et test dans un navigateur du chemin nominal : saisie d'une carte mixte avec obstacles, exécution d'une séquence contenant un blocage suivi d'autres commandes, vérification de l'affichage final ; puis test d'une entrée invalide (position sur obstacle, commande inconnue) pour vérifier l'affichage du message d'erreur et l'absence d'exécution.
