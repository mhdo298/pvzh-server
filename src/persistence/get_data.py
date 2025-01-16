from quart import request

from src.utils.misc import get_id, merge_json
import orjson as json


async def get_user_data(mod_name):
    data = await request.get_json()
    pid = get_id()
    async with request.db.cursor() as cursor:
        await cursor.execute(
            """
            SELECT users_data FROM users where player_id = %s and mod_name = %s
            """
            , (pid, mod_name))
        existing_data = await cursor.fetchone()
        if existing_data is None:
            existing_data = {}
        else:
            existing_data = existing_data[0]
        merge_json(existing_data, data)
        await cursor.execute(
            """
            INSERT INTO users (player_id, mod_name, users_data) VALUES (%s, %s, %s)
            ON CONFLICT (player_id, mod_name)  DO 
            UPDATE SET users_data=excluded.users_data;
            """
            , (pid, mod_name, json.dumps(existing_data)))
    return existing_data


async def get_inventory_data(mod_name):
    data = await request.get_json()
    pid = get_id()
    async with request.db.cursor() as cursor:
        await cursor.execute(
            """
            SELECT inventory_data FROM inventory where player_id = %s and mod_name = %s
            """
            , (pid, mod_name))
        existing_data = await cursor.fetchone()
        if existing_data is None:
            existing_data = {}
        else:
            existing_data = existing_data[0]
        merge_json(existing_data, data)
        await cursor.execute(
            """
            INSERT INTO inventory (player_id, mod_name, inventory_data) VALUES (%s, %s, %s)
            ON CONFLICT (player_id, mod_name)  DO 
            UPDATE SET inventory_data=excluded.inventory_data;
            """
            , (pid, mod_name, json.dumps(existing_data)))
    return existing_data


async def get_decks_data(mod_name):
    data = await request.get_json()
    pid = get_id()
    async with request.db.cursor() as cursor:
        await cursor.execute("""
               CREATE TEMP TABLE added_tmp_decks
               (LIKE decks INCLUDING DEFAULTS)
               ON COMMIT DROP;
               """)
        async with cursor.copy("""COPY added_tmp_decks (player_id, mod_name, deck_id, deck_data) FROM STDIN""") as copy:
            for deck in data["Decks"]:
                if deck["Name"] is not None:
                    await copy.write_row((pid, mod_name, deck['Id'], json.dumps(deck)))
                else:
                    await copy.write_row((pid, mod_name, deck['Id'], None))
        await cursor.execute(
            """
            INSERT INTO decks
            SELECT * FROM added_tmp_decks WHERE deck_data IS NOT NULL
            ON CONFLICT (player_id, mod_name, deck_id)  DO 
            UPDATE SET deck_data=excluded.deck_data;
            """
        )
        await cursor.execute(
            """
            DELETE FROM decks WHERE (player_id, mod_name, deck_id) in 
            (SELECT player_id, mod_name, deck_id FROM added_tmp_decks WHERE deck_data IS NULL);
            """
        )
        await cursor.execute(
            """
            SELECT deck_data FROM decks where player_id = %s and mod_name = %s
            """
            , (pid, mod_name))
        all_decks = [row[0] for row in await cursor.fetchall()]
        return all_decks
