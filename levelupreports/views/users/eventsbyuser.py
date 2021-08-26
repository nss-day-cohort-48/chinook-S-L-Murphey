"""Module for generating events that each gamer has signed up for by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event, Gamer, Game
from levelupreports.views import Connection


def events_by_user(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all events, with related user info.
            db_cursor.execute("""
                SELECT
                    g.id AS user_id,
                    e.id,
                    e.description,
                    e.date,
                    e.time,
                    gm.name,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_event e
                JOIN levelupapi_eventgamer eg ON e.id = eg.event_id
                JOIN levelupapi_gamer g ON eg.gamer_id = g.id
                JOIN auth_user u ON u.id = g.user_id
                JOIN levelupapi_game gm ON e.game_id=gm.id;

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

            events_by_user = {}

            for row in dataset:
                # Crete an Event instance and set its properties
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in events_by_user:

                    # Add the current game to the `events` list for it
                    events_by_user[uid]['events'].append({
                        "id": row['id'],
                        "description": row['description'],
                        "date": row['date'],
                        "time": row['time'],
                        "game_name": row['name']
                    })

                else:
                    # Otherwise, create the key and dictionary value
                    events_by_user[uid] = {
                        "gamer_id": uid,
                        "full_name": row['full_name'],
                        "events": 
                            [ 
                                {
                                "id": row['id'],
                                "description": row['description'],
                                "date": row['date'],
                                "time": row['time'],
                                "game_name": row['name']
                                }
                            ]
                    }
                    

        # Get only the values from the dictionary and create a list from them
        events = events_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'events_by_user': events
        }

        return render(request, template, context)