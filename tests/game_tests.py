import json
from django.conf.urls import url
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game
from django.contrib.auth.models import User, Permission
from rest_framework.authtoken.models import Token

class GameTests(APITestCase):
    
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

         # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        getUser = User.objects.get()
        getUser.user_permissions.set([Permission.objects.get(codename="change_game"), Permission.objects.get(codename="view_game"), Permission.objects.get(codename="add_game"), Permission.objects.get(codename="delete_game")])

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "description": "Murder Mystery",
            "name": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Clue")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["description"], "Murder Mystery")
        self.assertEqual(json_response["number_of_players"], 6)

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.game_type_id = 1 #must be a game_type instance
        game.description = "The Classic Board Game"
        game.name = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1 #must be a gamer instance

        game.save()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["name"], "Monopoly")
        self.assertEqual(response.data["maker"], "Milton Bradley")
        self.assertEqual(response.data["description"], "The Classic Board Game")
        self.assertEqual(response.data["number_of_players"], 4)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.description = "Sorry was an ok game in the minds of many."
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        url = f'/games/{game.id}'

        # DEFINE NEW PROPERTIES FOR GAME
        new_game = {
            "gameTypeId": 1,
            "description": "No one actually liked this game.",
            "name": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.put(url, new_game, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(response.data["name"], "Sorry")
        self.assertEqual(response.data["maker"], "Hasbro")
        self.assertEqual(response.data["description"], "No one actually liked this game.")
        self.assertEqual(response.data["number_of_players"], 4)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.description = "Sorry was based on the ancient Indian cross and circle game Pachisi"
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)