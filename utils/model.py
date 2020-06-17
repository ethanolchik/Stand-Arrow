from typing import List
from dataclasses import dataclass, field
from utils.exceptions import InsufficientQuantityError


@dataclass
class Player:
    player_id: int
    base_stats: dict
    inventory: "Inventory"


class Inventory():

    def __init__(self, items: dict = None):
        self.__storage = dict()
        if items is not None:
            self.__storage = items

    def show_inventory(self) -> dict:
        return {str(item): self.__storage[item] for item in self.__storage}

    def add_item(self, item: "Item", amt=1) -> bool:
        if item not in self.__storage:
            self.__storage[item] = amt
        else:
            self.__storage[item] += amt
        return True

    def remove_item(self, item: "Item", amt=1) -> dict:
        if item not in self.__storage or self.__storage[item] < amt:
            raise InsufficientQuantityError("Attempted to remove {amt} \
                                            of {item_name} from inventory but \
                                            there is {self.storage[item_name]")
        self.__storage[item] -= amt
        if self.__storage[item] == 0 and \
           item in self.__storage.keys():

            self.__storage.pop(item)
        return {item: amt}


class Stand:
    stand_id: int
    stand_description: str
    bonuses: dict
    effects: List[str]


class Item:

    @staticmethod
    def factory(*args, **kwargs) -> "Item":
        item_id = kwargs['item_id']
        item_name = kwargs['item_name']
        item_description = kwargs['item_description']
        return Item(item_id, item_name, item_description)
    
    def __init__(self, item_id: int, item_name: str, item_description: str):
        self.item_id = item_id
        self.item_name = item_name
        self.item_description = item_description

    def __str__(self):
        return self.item_name

    def __eq__(self, other):
        return sef.isinstance(other, Item) and self.item_id \
            == other.item_id and \
            self.item_name == other.item_name \
            and self.item_description == other.item_description

    def __hash__(self):
        return hash((self.item_id, self.item_name, self.item_description))
