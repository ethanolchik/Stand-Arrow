from discord.ext import commands
import utils.model as model


class Context(commands.Context):
    """A custom implementation of the command invocation context
       that allows for cross-cutting concerns such as data access"""

    async def get_stand(self, stand_name: str):
        """Lists all of the relevant information for a particular stand.
           One stand attribute per line of output."""
        stand = await self.bot.pool.fetchrow(f"SELECT * from stand WHERE stand_name = '{stand_name}'")
        return tuple(stand) if stand else None

    async def get_player(self, player_name: str):
        """Get a particular user by their name"""
        user = await self.bot.pool.fetchrow(f"SELECT * from player WHERE player_name = {player_name}")
        return tuple(user) if user else None

    async def get_player_id_from_name(self, player_name: str):
        """Get's a player_id for a player_name"""
        record = await self.bot.pool.fetchrow(f"SELECT player_id from player WHERE \
                                             player_name = '{player_name}'")
        return record["player_id"]

    async def get_player_inventory(self, player_id: int) -> "model.Inventory":
        """Get a users inventory"""
        inventory_rows = await self.bot.pool.fetch(f"SELECT item.item_id, item.item_name, \
        item.item_description, user_item.amount \
        FROM user_item INNER JOIN \
        item ON (item.item_id = user_item.item_id) \
        WHERE player_id = {player_id}")
        dicts = [dict(row) for row in inventory_rows]
        # Item(item_id, item_name, item_description): item_amount
        inventory_items = {model.Item.factory(**dictionary): dictionary['amount'] \
                           for dictionary in dicts}
        inventory = model.Inventory(inventory_items)
        return inventory

    async def get_item_id_from_name(self, item_name: str) -> int:
        record = await self.bot.pool.fetchrow(f"SELECT item_id from item WHERE \
                                               item_name = '{item_name}'")
        return record["item_id"]

    async def insert_into_inventory(self, player_name: int, item_name: str, amt: int):
        item_id = await self.get_item_id_from_name(item_name)
        sql = f"""WITH new_values (player_id, item_id, amount) AS (
        SELECT player_id, {item_id}, {amt}
        FROM player
        WHERE player_name = '{player_name}'
        ),
        upsert AS (
        UPDATE user_item m
            SET amount = m.amount + nv.amount
        FROM new_values nv
        WHERE m.player_id = nv.player_id AND m.item_id = nv.item_id
        RETURNING m.*
        )
        INSERT INTO user_item (player_id, item_id, amount)
        SELECT player_id, item_id, amount
        FROM new_values
        WHERE NOT EXISTS (SELECT 1
                  FROM upsert up
                  WHERE up.player_id = new_values.player_id
                  AND up.item_id = new_values.item_id)
        """
        await self.bot.pool.execute(sql)

    async def clear_inventory(self, player_name: str):
        player_id = await self.get_player_id_from_name(player_name)
        sql = f"DELETE FROM user_item where player_id = {player_id}"
        await self.bot.pool.execute(sql)
