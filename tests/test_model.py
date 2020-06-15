from utils import model
from utils.exceptions import InsufficientQuantityError
import unittest
import asyncio
import discord.ext.test as dpytest
from bot import Bot
import traceback
from cogs.testing import Testing
from cogs.inventory import Inventory


class TestInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = Bot()
        cls.bot.add_cog(Testing(cls.bot))
        cls.bot.add_cog(Inventory(cls.bot))
        dpytest.configure(cls.bot)
        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.bot.connect_all())
        cls.loop.run_until_complete(dpytest.message("Stand Arrow debug_clear"))
        
    def test_add_remove_from_inventory(self):
        inventory = model.Inventory()
        requiem_arrow = "Requiem Arrow"
        
        inventory.add_item(requiem_arrow)
        self.assertEqual({"Requiem Arrow": 1}, inventory.show_inventory())
        inventory.add_item(requiem_arrow)
        self.assertEqual({"Requiem Arrow": 2}, inventory.show_inventory())
        inventory.remove_item(requiem_arrow)
        self.assertEqual({"Requiem Arrow": 1}, inventory.show_inventory())

        requiem_arrow = inventory.remove_item(requiem_arrow)
        self.assertEqual({}, inventory.show_inventory())
        self.assertEqual({"Requiem Arrow": 1}, requiem_arrow)

        with self.assertRaises(InsufficientQuantityError):
            inventory.remove_item("Requiem Arrow")
        self.assertEqual({}, inventory.show_inventory())

    # E2E test that tests whether changes to a users inventory properly persist
    # Database is not mocked.
    def test_inventory_changes_persist_for_a_user(self):
        try:
            self.loop.run_until_complete(dpytest.message("Stand Arrow debug_free_cash"))
            dpytest.verify_message("You have been given $1000!")
            self.loop.run_until_complete(dpytest.message("Stand Arrow debug_free_cash"))
            dpytest.verify_message("You have been given $1000!")
            self.loop.run_until_complete(dpytest.message("Stand Arrow show_inv"))
            dpytest.verify_message('TestUser#0001 Inventory:\n\nmoney: 2000\n')
        except Exception as e:
            traceback.print_exc()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
