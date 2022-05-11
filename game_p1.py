#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import cmd
from http_manager import HttpManager
from server.server_manager import ServerManager
import utils
from prettytable import PrettyTable
from getpass import getpass
from db_manager import UserDB
from graphics import Graphics
from state import State

class main(cmd.Cmd):
    prompt = '\n>'
    username = None
    password_hash = None
    last_gamelist = None
    token = None
    users_db = UserDB()
    server = ServerManager()
    http_mgr = HttpManager()

    def do_login(self, initial=None):
        'login - Log into the system with an existing account.\n'
        try:
            self.username = input('Username: ')
            self.password_hash = utils.get_password_sha256(getpass('Password: '))
        except EOFError:
            return
        self.token = self.http_mgr.login(self.username, self.password_hash)
        if self.token:
            self.prompt = f'\n[{self.username}]>'
            print('Logged in successfully.\n')
        else:
            print('Wrong credentials.\n')

    def do_logout(self, initial=None):
        'logout - Log out of the system.\n'
        if self.http_mgr.logout(self.token):
            self.user_uid = None
            self.username = None
            self.password_hash = None
            self.last_gamelist = None
            self.token = None
            self.prompt = '\n>'
        else:
            print('Error in logout')

    def do_createuser(self, initial=None):
        'createuser - Create a new user given a username and a password.\n'
        if self.token:
            print('A user is already logged in.\n')
            return
        try:
            self.username = input('Username: ')
            if self.users_db.is_registered(self.username):
                print(f'Username {self.username} is already taken.\n')
                return
            self.password_hash = utils.get_password_sha256(getpass('Password: '))
        except EOFError:
            return
        if self.username and self.password_hash:
            if self.http_mgr.create_user(self.username, self.password_hash):
                print('New user created successfully.\n')
            else:
                print('Error creating new user.\n')

    def do_stats(self, initial=None):
        'stats - Check the stats for the currently logged user.\n'
        if not self.token:
            print('No user is logged in currently.\n')
            return
        stats = self.users_db.get_stats(self.user_uid)
        stats_table = PrettyTable(['Total Games', 'Wins', 'Losses', 'W/L Ratio'])
        stats_table.add_row(stats)
        print(stats_table)
    
    def do_updateuser(self, initial=None):
        ('updateuser - Update the username or the userpassword. If no input is written '
        'in any field, that field will not be updated.\n')  
        if not self.token:
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
            if self.http_mgr.update_user(self.username, self.password_hash):
                print('User data updated correctly\n')
                self.prompt = f'\n[{self.username}]>'
            else:
                print('Error updating user\n')
    
    def do_removeuser(self, initial=None):
        'removeuser - Remove the current account and all its data.\n'
        if not self.token:
            print('No user is logged in currently.\n')
            return
        if self.http_mgr.remove_user(self.token):
            self.do_logout()
            print('User removed successfully.\n')

    def do_newgame(self, arg, initial=None):
        ('newgame <mode>- Ask the server to create a new game in mode <mode>.\n'
        '\t0 -> PvP Local\n\t1 -> PvP Online\n\t2 -> PvMC\n\t4 -> MCvMC\n')
        if not self.token:
            print('No user is logged in currently.\n')
            return
        try:
            if not arg.strip().isdigit():
                print('Mode needs to be numeric.\n')
                return
            mode = int(arg.strip())
            if mode not in [0, 1, 2, 4]:
                print('Invalid mode\n')
                return
            if mode == 0:
                game = Graphics(mode=0)
                result = game.game()
            elif mode == 1:
                game_name = input('Game name: ')
                if not game_name:
                    return
                game_password = getpass('Game password: ')
                if game_password:
                    game_password = utils.get_password_sha256(game_password)
                print('\nCreating new game, please wait...\n')
                game_data = self.http_mgr.new_game(self.token, game_name, game_password)
                print(f'New game created. Joining...\n')
                game = State()
                game.load_state(game_data)
                game = Graphics(mode=mode, state=game, player=0, http_mgr=self.http_mgr)
                result = game.game()
            elif mode == 2:
                game = Graphics(mode=2, player=1)
                result = game.game()
            elif mode == 4:
                game = Graphics(mode=4)
                result = game.game()
            print('Game terminated.\n')
            print(result)
        except EOFError:
            print('Game creation cancelled.\n')
            return
    
    def do_listgames(self, initial=None):
        'listgames - List all the available games at the moment with their uid to join.\n'
        if not self.token:
            print('You need an account to see the list of games.\n')
            return
        games_list = self.http_mgr.list_games()
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
        if not self.token:
            print('You need an account to join a game.\n')
            return
        if arg.strip().isdigit() and self.last_gamelist:
            try:
                game_uid = self.last_gamelist[int(arg)]
            except IndexError:
                print(f'No game found in the games list with index {arg}.\n')
                return
        else:
            game_uid = arg.strip()
        game_password = getpass('Game password: ')
        if game_password:
            game_password = utils.get_password_sha256(game_password)
        game_data = self.http_mgr.join_game(self.token, game_uid, game_password)
        print(f'\nJoining {arg}...\n')
        if not game_data:
            print(f'No game found with ID \'{game_uid}\'.\n')
            return
        game = State()
        game.load_state(game_data)
        game = Graphics(mode=1, player=1, http_mgr=self.http_mgr)
        result = game.game()
        print('RESULT: ', result)
        print('Game terminated.\n')

    def do_monoloco(self, initial=None):
        'monoloco - Starts games simulation using Montecarlo vs Monoloco and returns stats\n'
        game = Graphics(mode=3)
        results = game.game()
        print(f'############# SIMULACIÓN FINALIZADA #############.\nVictorias Montecarlo: {results[0]}\nVictorias Monoloco: {results[1]}')

    def do_exit(self, initial=None):
        'exit - Stop and exit the application.\n'
        self.do_logout()
        return self.close()

    def close(self):
        return True


if __name__ == "__main__":
    game = main()
    try:
        game.cmdloop()
    except KeyboardInterrupt:
        game.close()