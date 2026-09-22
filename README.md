# mars-rover

Un simulateur de Mars Rover.

Le simulateur reçoit une carte (largeur x hauteur), un point de départ
(position + direction) et une liste de commandes, puis affiche la position
et la direction finales du rover.

## Commandes disponibles

- `L` : tourne de 90° vers la gauche (sur place)
- `R` : tourne de 90° vers la droite (sur place)
- `M` : avance d'une case dans la direction courante

Les directions sont `N`, `E`, `S`, `W` (nord, est, sud, ouest).

La carte est bornée : une commande qui ferait sortir le rover de la carte
est rejetée et une erreur est levée, sans modifier la position du rover.

## Utilisation

```bash
python -m mars_rover --width 5 --height 5 --start-x 1 --start-y 2 --start-direction N LMLMLMLMM
# -> 1:3:N
```

## Installation et tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .

pytest
```

## Utilisation en tant que bibliothèque

```python
from mars_rover import Direction, PlanetMap, Position, Rover, run_mission

planet_map = PlanetMap(width=5, height=5)
rover = Rover(Position(1, 2), Direction.NORTH)

final_rover = run_mission(planet_map, rover, "LMLMLMLMM")
print(final_rover)  # 1:3:N
```
