#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import cmd
import utils
import uuid
from getpass import getpass
from db_manager import UserDB

class main(cmd.Cmd):
    prompt = '>'
    user_uid = None
    username = None
    password_hash = None
    users_db = UserDB()

    def do_login(self, initial=None):
        'login - Log into the system with an existing account.\n'
        self.username = input('Nombre de usuario: ')
        self.password_hash = utils.get_password_sha256(getpass('Password: '))
        self.user_uid = self.users_db.verify_login(self.username, self.password_hash)
        if self.user_uid:
            print('Logged in successfully.\n')
        else:
            print('Wrong credentials.\n')
            self.username = None
            self.password_hash = None
            self.user_uid = None

    def do_logout(self, initial=None):
        'logout - Log out of the system.\n'
        if not self.user_uid:
            print('No user is logged in currently.\n')
            return
        self.user_uid = None
        self.username = None
        self.password_hash = None
        print('Logged out successfully.\n')        

    def do_createuser(self, initial=None):
        'createuser - Create a new user given a username and a password.\n'
        if self.user_uid:
            print('A user is already logged in.\n')
            return
        self.username = input('Nombre de usuario: ')
        self.password_hash = utils.get_password_sha256(getpass('Password: '))
        if self.username and self.password_hash:
            self.user_uid = str(uuid.uuid4())
            self.users_db.new_user(self.user_uid, self.username, self.password_hash)
            print('New user created successfully.\n')
    
    def do_updateuser(self, initial=None):
        ('updateuser - Update the username or the userpassword. If no input is written '
        'in any field, that field will not be updated.\n')
    
    def do_removeuser(self, initial=None):
        'removeuser - Remove the current account and all its data.\n'
        if not self.user_uid:
            print('No user is logged in currently.\n')
            return
        self.users_db.remove_user(self.user_uid)
        self.do_logout()
        print('User removed successfully.\n')

    def do_creategame(self, initial=None):
        'creategame - Ask the server to create a new game.\n'
    
    def do_listgames(self, initial=None):
        'listgames - List all the available games at the moment with their uid to join.\n'

    def do_joingame(self, arg, initial=None):
        'joingame <game uid> - Given a uid, try to join to the respective game.\n'

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