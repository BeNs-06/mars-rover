# Intent : Simulateur de rover martien

Auteur : non renseigné.

## Problème
Les développeurs de l'équipe Mars Rover ont besoin de valider la logique de navigation du rover avant de l'intégrer, sans disposer aujourd'hui d'un moyen de simuler son comportement face à un point de départ, une carte et une liste de commandes.

## Résultat proposé
Un simulateur qui :
- reçoit un point de départ (x, y), une orientation (N, S, E ou W), une carte plaçant les obstacles, et une liste de commandes ;
- interprète les commandes : avancer, ou tourner de 90° à droite ou à gauche ;
- reste immobile si un obstacle bloque l'avancée ;
- affiche la position et la direction finales du rover ;
- accepte une carte utilisant soit les symboles 🟩 (libre) et 🌳 (obstacle), soit 🟫 (libre) et 🪨 (obstacle).

## Utilisateurs et systèmes concernés
Les développeurs de l'équipe Mars Rover, pour valider la logique de navigation avant son intégration.

## Contraintes
Aucune contrainte particulière identifiée à ce stade.

## Questions ouvertes
- Format exact des entrées (fichier, arguments en ligne de commande, API, etc.) et de la sortie affichée.
- Comportement du rover en bord de carte (arrêt, carte cyclique, etc.).
- Jeu de commandes complet (avancer/tourner uniquement, ou aussi reculer ?).
- Équivalence de sens entre les deux jeux de symboles (🟩/🌳 et 🟫/🪨) : signifient-ils la même chose (libre/obstacle) ou des états différents ?
