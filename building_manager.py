from buildings import Building
from typing import Dict, Tuple

# has array of buildings
# check if they can be built somewhere etc?
# used for simulating them?

class BuildingManager:
    def __init__(self):
        self.building_dict = {
            (3,3): Building(3,3)
        }
    