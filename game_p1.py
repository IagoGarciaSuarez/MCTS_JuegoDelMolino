#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import cmd
from server.server_manager import ServerManager
import utils
import uuid
from prettytable import PrettyTable
from getpass import getpass
from db_manager import UserDB
from graphics import Graphics
from state import State

class main(cmd.Cmd):
    prompt = '\n>'
    user_uid = None
    username = None
    password_hash = None
    last_gamelist = None
    users_db = UserDB()
    server = ServerManager()

    def do_login(self, initial=None):
        'login - Log into the system with an existing account.\n'
        try:
            self.username = input('Username: ')
            self.password_hash = utils.get_password_sha256(getpass('Password: '))
        except EOFError:
            return
        self.user_uid = self.users_db.verify_login(self.username, self.password_hash)
        if self.user_uid:
            self.prompt = f'\n[{self.username}]>'
            print('Logged in successfully.\n')
        else:
            print('Wrong credentials.\n')
            self.do_logout()

    def do_logout(self, initial=None):
        'logout - Log out of the system.\n'
        self.user_uid = None
        self.username = None
        self.password_hash = None
        self.last_gamelist = None
        self.prompt = '\n>'

    def do_createuser(self, initial=None):
        'createuser - Create a new user given a username and a password.\n'
        if self.user_uid:
            print('A user is already logged in.\n')
            return
        try:
            self.username = input('Username: ')
            if self.users_db.is_registered(self.username):
                print(f'Username {self.username} is already taken.\n')
                self.do_logout()
                return
            self.password_hash = utils.get_password_sha256(getpass('Password: '))
        except EOFError:
            return
        if self.username and self.password_hash:
            self.user_uid = str(uuid.uuid4())
            self.users_db.new_user(self.user_uid, self.username, self.password_hash)
            print('New user created successfully.\n')

    def do_stats(self, initial=None):
        'stats - Check the stats for the currently logged user.\n'
        if not self.user_uid:
            print('No user is logged in currently.\n')
            return
        stats = self.users_db.get_stats(self.user_uid)
        stats_table = PrettyTable(['Total Games', 'Wins', 'Losses', 'W/L Ratio'])
        stats_table.add_row(stats)
        print(stats_table)
    
    def do_updateuser(self, initial=None):
        ('updateuser - Update the username or the userpassword. If no input is written '
        'in any field, that field will not be updated.\n')  
        if not self.user_uid:
            print('No user is logged in currently.\n')
            return
        try:
            self.username = input('New username: ')
            if self.users_db.is_registered(self.username):
                print(f'Username {self.username} is already taken.\n')
                self.do_logout()
                return
            self.password_hash = utils.get_password_sha256(getpass('New password: '))
        except EOFError:
            return
        if self.username and self.password_hash:
            self.users_db.update_user(self.user_uid, self.username, self.password_hash)
            print('User data updated correctly\n')
            self.prompt = f'\n[{self.username}]>'
    
    def do_removeuser(self, initial=None):
        'removeuser - Remove the current account and all its data.\n'
        if not self.user_uid:
            print('No user is logged in currently.\n')
            return
        self.users_db.remove_user(self.user_uid)
        self.do_logout()
        print('User removed successfully.\n')

    def do_gamecreate(self, initial=None):
        'gamecreate - Ask the server to create a new game.\n'
        if not self.user_uid:
            print('No user is logged in currently.\n')
            return
        try:
            game_name = input('Game name: ')
            if not game_name:
                return
            game_password = getpass('Game password: ')
            if game_password:
                game_password = utils.get_password_sha256(game_password)
        except EOFError:
            print('Game creation cancelled.\n')
            return
        print('\nCreating new game, please wait...\n')
        game_uid = self.server.new_game(self.username, game_name, game_password)
        print(f'New game created with ID: {game_uid}\n')
        game = Graphics(State(**self.server.get_game_data(game_uid)))
        result = game.game()
        print('Game terminated.\n')
        print(result)
    
    def do_listgames(self, initial=None):
        'listgames - List all the available games at the moment with their uid to join.\n'
        if not self.user_uid:
            print('You need an account to see the list of games.\n')
            return
        games_list = self.server.list_games()
        self.last_gamelist = [game for game in games_list]
        games_table = PrettyTable(["Index", "Name", "Creator", "Public", "Created On"])
        for game, index in zip(games_list, range(len(list(games_list)))):
            game_data = games_list[game]
            games_table.add_row(
                [index, game_data["name"], game_data["creator"],
                game_data["public"], game_data["created_on"]])
        print(games_table)

    def do_joingame(self, arg, initial=None):
        'joingame <game index|game uid> - Given a uid, try to join to the respective game.\n'
        if not self.user_uid:
            print('You need an account to join a game.\n')
            return
        if arg.strip().isdigit() and self.last_gamelist:
            try:
                game_uid = self.last_gamelist[int(arg)]
                game_data = self.server.get_game_data(game_uid)
            except IndexError:
                print(f'No game found in the games list with index {arg}.\n')
                return
        else:
            game_data = self.server.get_game_data(arg.strip())

        print(f'\nJoining {arg}...\n')
        if not game_data:
            print(f'No game found with ID \'{arg.strip()}\'.\n')
            return
        print(game_data)
        print('Game terminated.\n')


    def do_exit(self, initial=None):
        'exit - Stop and exit the application.\n'
        return self.close()

    def close(self):
        return True


if __name__ == "__main__":
    game = main()
    try:
        game.cmdloop()
    except KeyboardInterrupt:
        game.close()