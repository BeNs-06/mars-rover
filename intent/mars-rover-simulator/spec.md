# Spec : Simulateur de rover martien

Intention de référence : intent/mars-rover-simulator/intent.md

## Périmètre

Le simulateur valide la logique de navigation du rover avant son intégration, pour les développeurs de l'équipe Mars Rover. Il reçoit un point de départ (x, y), une orientation initiale (N, S, E ou W), une carte plaçant les obstacles et une liste de commandes ; il interprète les commandes d'avance et de rotation à 90°, immobilise le rover face à un obstacle, et affiche la position et l'orientation finales. Aucune contrainte particulière n'a été identifiée dans l'intention au-delà de ce périmètre.

## Exigences

### EX-01 — Initialisation du rover via une interface web

Origine dans l'intention : « reçoit un point de départ (x, y), une orientation (N, S, E ou W), une carte plaçant les obstacles, et une liste de commandes » ; format précisé par décision du Product Owner (voir Questions ouvertes).
Comportement attendu : l'utilisateur saisit, via une interface web, un point de départ (x, y), une orientation initiale (N, S, E ou W), une carte indiquant les cases libres et les obstacles, et une liste de commandes ; le simulateur initialise le rover avec ces valeurs.

Scénario
- Situation de départ : une page web affichant les champs de saisie (carte, point de départ, orientation, commandes).
- Action : l'utilisateur renseigne les champs et déclenche la simulation.
- Résultat attendu : le rover est initialisé à la position et à l'orientation saisies, prêt à exécuter la liste de commandes.

### EX-02 — Rejet des entrées invalides avant exécution

Origine dans l'intention : découle du besoin de fiabilité pour « valider la logique de navigation » ; comportement précisé par décision du Product Owner (voir Questions ouvertes).
Comportement attendu : si la position de départ est hors de la carte ou sur une case obstacle, ou si la liste de commandes contient une commande non reconnue, le simulateur affiche un message d'erreur sur l'interface web et n'exécute aucune commande.

Scénario
- Situation de départ : point de départ saisi hors des limites de la carte (ou sur un obstacle), ou une commande non reconnue présente dans la liste.
- Action : l'utilisateur déclenche la simulation.
- Résultat attendu : un message d'erreur s'affiche sur la page, aucune commande n'est exécutée, le rover ne se déplace pas.

### EX-03 — Avance du rover

Origine dans l'intention : « interprète les commandes : avancer, ou tourner de 90° à droite ou à gauche ».
Comportement attendu : lorsque la commande avancer est exécutée et que la case adjacente dans la direction de l'orientation courante est libre, le rover se déplace d'une case dans cette direction ; son orientation ne change pas.

Scénario
- Situation de départ : rover positionné en (x, y), orientation courante donnée, case adjacente dans cette direction libre.
- Action : exécution de la commande avancer.
- Résultat attendu : le rover occupe la case adjacente correspondante, avec la même orientation.

### EX-04 — Rotation du rover

Origine dans l'intention : « interprète les commandes : ... tourner de 90° à droite ou à gauche ».
Comportement attendu : lorsqu'une commande tourner à droite (ou à gauche) est exécutée, l'orientation du rover change de 90° dans le sens correspondant (cycle N→E→S→W→N pour la droite, et l'inverse pour la gauche) ; sa position ne change pas.

Scénario
- Situation de départ : rover en (x, y), orientation N.
- Action : exécution de la commande tourner à droite.
- Résultat attendu : le rover reste en (x, y), orientation E.

### EX-05 — Blocage par un obstacle

Origine dans l'intention : « reste immobile si un obstacle bloque l'avancée ».
Comportement attendu : lorsque la commande avancer est exécutée et que la case adjacente dans la direction de l'orientation courante contient un obstacle, le rover reste à sa position et son orientation actuelles.

Scénario
- Situation de départ : rover en (x, y), orientation courante, case adjacente marquée obstacle.
- Action : exécution de la commande avancer.
- Résultat attendu : le rover reste en (x, y), avec la même orientation.

### EX-06 — Blocage en bord de carte

Origine dans l'intention : question ouverte « comportement du rover en bord de carte », tranchée par décision du Product Owner (voir Questions ouvertes).
Comportement attendu : lorsque la commande avancer déplacerait le rover en dehors des limites de la carte, le rover reste à sa position et son orientation actuelles, comme s'il rencontrait un obstacle.

Scénario
- Situation de départ : rover positionné sur une case en bordure de la carte, orientation dirigée vers l'extérieur de la carte.
- Action : exécution de la commande avancer.
- Résultat attendu : le rover reste sur la même case, avec la même orientation.

### EX-07 — Poursuite de la séquence après un blocage

Origine dans l'intention : réserve identifiée lors de la spécification (comportement non précisé par l'intention pour la suite des commandes après un blocage), tranchée par décision du Product Owner (voir Réserves).
Comportement attendu : après qu'une commande avancer a été bloquée (obstacle ou bord de carte), le simulateur poursuit l'exécution des commandes suivantes de la liste.

Scénario
- Situation de départ : liste de commandes contenant une commande avancer bloquée suivie d'autres commandes (par exemple tourner, avancer).
- Action : exécution complète de la liste.
- Résultat attendu : la commande bloquée est ignorée pour le déplacement (rover immobile pour celle-ci) et les commandes suivantes s'exécutent normalement.

### EX-08 — Affichage du résultat final

Origine dans l'intention : « affiche la position et la direction finales du rover » ; support précisé par décision du Product Owner (voir Questions ouvertes).
Comportement attendu : après exécution de toutes les commandes (ou après le rejet décrit en EX-02), l'interface web affiche la position finale (x, y) et l'orientation finale du rover.

Scénario
- Situation de départ : liste de commandes entièrement exécutée.
- Action : fin de l'exécution.
- Résultat attendu : la page affiche la position (x, y) et l'orientation finales du rover.

### EX-09 — Carte avec le jeu de symboles 🟩/🌳

Origine dans l'intention : « accepte une carte utilisant soit les symboles 🟩 (libre) et 🌳 (obstacle) ».
Comportement attendu : le simulateur interprète 🟩 comme case libre et 🌳 comme obstacle.

Scénario
- Situation de départ : carte saisie utilisant les symboles 🟩 et 🌳.
- Action : exécution des commandes.
- Résultat attendu : les cases 🟩 sont traversables, les cases 🌳 bloquent l'avancée (comportement d'EX-05).

### EX-10 — Carte avec le jeu de symboles 🟫/🪨

Origine dans l'intention : « ... soit 🟫 (libre) et 🪨 (obstacle) ».
Comportement attendu : le simulateur interprète 🟫 comme case libre et 🪨 comme obstacle.

Scénario
- Situation de départ : carte saisie utilisant les symboles 🟫 et 🪨.
- Action : exécution des commandes.
- Résultat attendu : les cases 🟫 sont traversables, les cases 🪨 bloquent l'avancée (comportement d'EX-05).

### EX-11 — Équivalence et mélange des deux jeux de symboles

Origine dans l'intention : question ouverte « équivalence de sens entre les deux jeux de symboles », tranchée par décision du Product Owner (voir Questions ouvertes).
Comportement attendu : 🟩 et 🟫 ont strictement le même sens (case libre), 🌳 et 🪨 ont strictement le même sens (case obstacle) ; une carte peut combiner librement des symboles des deux jeux sans changer leur interprétation.

Scénario
- Situation de départ : carte combinant des cases 🟩, 🌳, 🟫 et 🪨.
- Action : exécution des commandes.
- Résultat attendu : le comportement du rover est identique à celui obtenu avec une carte n'utilisant qu'un seul jeu de symboles pour un agencement équivalent de cases libres/obstacles.

## Conception proposée

- **Modèle de domaine** (accepté) : un Rover (position x, y + orientation N/S/E/W), une Carte (grille de cases dont l'état est libre ou obstacle, obtenu par normalisation des symboles selon EX-11), et une Commande parmi avancer, tourner à gauche, tourner à droite (EX-03/EX-04, jeu de commandes confirmé sans recul).
- **Interface web** (accepté dans son principe, détails d'interaction à affiner en Build) : un formulaire de saisie du point de départ, de l'orientation, de la carte et de la liste de commandes, un déclencheur de simulation, et une zone d'affichage du résultat (position/orientation finales, EX-08) ou du message d'erreur (EX-02). Le choix précis des composants de saisie (ex. zone de texte vs éditeur visuel de grille) n'est pas fixé par cette spécification et n'affecte pas le comportement attendu ; il relève de la phase Build.
- **Validation préalable** (accepté) : avant toute exécution, vérifie que la position de départ est dans les limites de la carte et sur une case libre, et que chaque commande de la liste appartient au jeu reconnu ; en cas d'échec, affiche un message d'erreur et n'exécute rien (EX-02).
- **Moteur d'exécution** (accepté) : exécute les commandes une à une, dans l'ordre. Pour avancer, vérifie si la case cible est libre et dans les limites de la carte avant de déplacer le rover ; sinon le rover reste immobile pour cette commande et l'exécution continue avec la commande suivante (EX-05, EX-06, EX-07). Pour tourner à gauche/à droite, modifie l'orientation sans vérification de carte (EX-04).
- **Normalisation des symboles de carte** (accepté) : à la lecture de la carte, 🟩 et 🟫 sont convertis en état « libre », 🌳 et 🪨 en état « obstacle » (EX-11), ce qui permet leur mélange dans une même carte.

## Réserves

### R-01 — Poursuite de la séquence de commandes après un blocage

Origine : ambiguïté identifiée lors de la spécification ; l'intention ne précisait pas si le rover devait continuer d'exécuter les commandes suivantes après un blocage (obstacle ou bord de carte) ou si l'exécution devait s'arrêter.
Exigences concernées : EX-05, EX-06, EX-07.
Conséquences : affecte le comportement observable pour toute liste de commandes contenant un blocage suivi d'autres commandes.
Statut : **Résolue.**
Décision : le simulateur poursuit l'exécution des commandes suivantes après un blocage (le rover reste immobile pour la commande bloquée uniquement).
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co).
Date : 2026-09-22.
Justification : choix explicite parmi les options proposées lors de la session de spécification.
Éléments modifiés : ajout d'EX-07 ; scénarios d'EX-05 et EX-06 précisés en conséquence.

### R-02 — Traitement des entrées invalides

Origine : ambiguïté identifiée lors de la spécification ; l'intention ne précisait pas le comportement attendu si la position de départ est hors carte ou sur un obstacle, ou si une commande inconnue figure dans la liste.
Exigences concernées : EX-01, EX-02, EX-08.
Conséquences : affecte la fiabilité de l'outil pour l'usage visé (validation de la logique de navigation) et le contenu affiché en cas d'entrée incorrecte.
Statut : **Résolue.**
Décision : le simulateur affiche un message d'erreur et n'exécute aucune commande lorsque les entrées sont invalides.
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co).
Date : 2026-09-22.
Justification : choix explicite parmi les options proposées lors de la session de spécification.
Éléments modifiés : ajout d'EX-02.

### R-03 — Mélange des deux jeux de symboles sur une même carte

Origine : ambiguïté identifiée lors de la spécification, liée à la question ouverte de l'intention sur l'équivalence de sens des deux jeux de symboles ; l'intention ne précisait pas si une carte pouvait combiner des symboles des deux jeux.
Exigences concernées : EX-09, EX-10, EX-11.
Conséquences : détermine si le moteur doit gérer un seul jeu de symboles par carte ou une normalisation tolérant le mélange.
Statut : **Résolue** (par la même décision que la question ouverte sur l'équivalence de sens, voir Questions ouvertes).
Décision : les deux jeux de symboles sont strictement équivalents (libre/obstacle) et interchangeables ; une carte peut les mélanger.
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co).
Date : 2026-09-22.
Justification : choix explicite parmi les options proposées lors de la session de spécification.
Éléments modifiés : ajout d'EX-11.

## Questions ouvertes

### Format exact des entrées et de la sortie affichée

Statut : **Répondue.**
Réponse : interface web — carte, point de départ, orientation et commandes saisis via une page web ; position et orientation finales affichées sur la même page.
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co). Date : 2026-09-22.
Effet sur le Build : n'est plus bloquante ; formalisée dans EX-01, EX-02 et EX-08.

### Comportement du rover en bord de carte

Statut : **Répondue.**
Réponse : le rover reste immobile, comme s'il rencontrait un obstacle.
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co). Date : 2026-09-22.
Effet sur le Build : n'est plus bloquante ; formalisée dans EX-06.

### Jeu de commandes complet (avancer/tourner uniquement, ou aussi reculer ?)

Statut : **Répondue.**
Réponse : avancer et tourner uniquement ; pas de commande de recul.
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co). Date : 2026-09-22.
Effet sur le Build : n'est plus bloquante ; le jeu de commandes est fixé dans EX-03/EX-04 et dans la Conception proposée.

### Équivalence de sens entre les deux jeux de symboles (🟩/🌳 et 🟫/🪨)

Statut : **Répondue.**
Réponse : les deux jeux signifient strictement la même chose (libre/obstacle) et sont interchangeables, y compris mélangés sur une même carte.
Auteur : Product Owner (aisdlc09@ia.academy.thiga.co). Date : 2026-09-22.
Effet sur le Build : n'est plus bloquante ; formalisée dans EX-11.

## Contexte de génération

### Demande initiale

Commande `/spec intent/mars-rover/intent.md`. Remarque : ce chemin n'existe pas dans le dépôt ; l'unique intention présente est `intent/mars-rover-simulator/intent.md`, dont la version acceptée (PR #2, mergée le 2026-09-22) a été utilisée pour cette spécification.

### Skills utilisées

| Chemin | Commit Git de la version utilisée |
| --- | --- |
| .claude/skills/spec/SKILL.md | 5274ac3d8c1d510427aa46f70b70eda523cf65d9 |

### Révisions

Aucune révision à ce stade — première rédaction.
