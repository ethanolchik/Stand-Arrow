from utils import model
import unittest


class TestInventory(unittest.TestCase):
    def test_add_remove_from_inventory(self):
        inventory = model.Inventory()
        inventory.add_item("Requiem Arrow")
        self.assertEqual({"Requiem Arrow": 1}, inventory.show_inventory())
        inventory.add_item("Requiem Arrow")
        self.assertEqual({"Requiem Arrow": 2}, inventory.show_inventory())
        inventory.remove_item("Requiem Arrow")
        self.assertEqual({"Requiem Arrow": 1}, inventory.show_inventory())
        requiem_arrow = inventory.remove_item("Requiem Arrow")
        self.assertEqual({}, inventory.show_inventory())
        self.assertEqual({"Requiem Arrow": 1}, requiem_arrow)


if __name__ == '__main__':
    unittest.main()
