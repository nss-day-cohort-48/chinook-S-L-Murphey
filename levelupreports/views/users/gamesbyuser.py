"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection


def usergame_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    id,
                    name,
                    maker,
                    game_type_id,
                    number_of_players,
                    description,
                    user_id,
                    full_name
                FROM
                    GAMES_BY_USER
            """)

            dataset = db_cursor.fetchall()

            # This takes the flat data from the database, and builds the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "games": [
            #             {
            #                 "id": 1,
            #                 "name": "Foo",
            #                 "maker": "Bar Games",
            #                 "description": "Crazy new Game to play with friends.",
            #                 "number_of_players": 4,
            #                 "game_type_id": 2
            #             }
            #         ]
            #     }
            # }

            games_by_user = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                game = Game()
                game.name = row["name"]
                game.maker = row["maker"]
                game.description = row["description"]
                game.number_of_players = row["number_of_players"]
                game.game_type_id = row["game_type_id"]

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in games_by_user:

                    # Add the current game to the `games` list for it
                    games_by_user[uid]['games'].append(game)

                else:
                    # Otherwise, create the key and dictionary value
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_games = games_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_users_with_games
        }

        return render(request, template, context)