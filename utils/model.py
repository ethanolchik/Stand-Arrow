from typing import List
from dataclasses import dataclass
from collections import defaultdict
import copy
from utils.exceptions import InsufficientQuantityError


@dataclass
class Player:
    player_id: int
    base_stats: dict
    inventory: "Inventory"


class Inventory():

    def __init__(self):
        self.storage = defaultdict(int)

    def show_inventory(self) -> dict:
        return copy.deepcopy(self.storage)

    def get_item(self, item_name: str) -> "Item" or None:
        pass

    def add_item(self, item_name: str, amt=1) -> bool:
        self.storage[item_name] += amt

    def remove_item(self, item_name: str, amt=1) -> dict:
        if self.storage[item_name] < amt:
            raise InsufficientQuantityError("Attempted to remove {amt} \
                                            of {item_name} from inventory but \
                                            there is {self.storage[item_name]")
        self.storage[item_name] -= amt
        if self.storage[item_name] == 0:
            self.storage.pop(item_name)
        return {item_name: amt}


class Stand:
    stand_id: int
    stand_description: str
    bonuses: dict
    effects: List[str]


class Item:
    item_id: int
    item_name: str
