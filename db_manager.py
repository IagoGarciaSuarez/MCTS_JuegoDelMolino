import sqlite3
import const

class UserDB():
    '''Objeto para acceso a la db de usuarios'''
    def __init__(self, database='users.db'):
        '''Selección de la base de datos.'''
        self.database = const.USERS_DATABASE_DIR + database
        self.create_table()

    def _create_connection(self, database_file):
        '''Crea la conexión.'''
        conn = sqlite3.connect(database_file)
        conn.row_factory = lambda cursor, row: row[0]
        return conn

    def drop_table(self):
        '''Vacía la base de datos.'''
        drop_table_sql = 'DROP TABLE IF EXISTS users'
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(drop_table_sql)
        conn.close()

    def create_table(self):
        '''Crea una tabla si no existe.'''
        create_table_sql = 'CREATE TABLE IF NOT EXISTS users ' + \
            '(uid text PRIMARY KEY,username text NOT NULL,password text NOT NULL,' + \
                'total_games text,wins integer,losses integer,ratio decimal);'
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
        conn.close()

    def get_all(self):
        '''Devuelve todos los registros.'''
        get_all_sql = 'SELECT * FROM users'
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(get_all_sql)
            result = cursor.fetchall()
        conn.close()
        return result

    def is_registered(self, username):
        '''Comprueba si está en la bbdd.'''
        exist_sql = "SELECT * FROM users WHERE EXISTS(SELECT 1 " + \
            f"FROM users WHERE username='{username}');"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(exist_sql)
            result = False
            if cursor.fetchone():
                result = True
        conn.close()
        return result
    
    def verify_login(self, username, password_hash):
        'Verifica si las credenciales son correctas'
        exist_sql = "SELECT uid FROM users WHERE EXISTS(SELECT 1 " + \
            f"FROM users WHERE username='{username}' AND password='{password_hash}');"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(exist_sql)
            user_uid = cursor.fetchone()
        conn.close()
        return user_uid

    def new_user(self, user_uid, username, password_hash):
        '''Añade un nuevo usuario a la base de datos.'''
        add_sql = f"INSERT INTO users VALUES('{user_uid}','{username}','{password_hash}',0,0,0,0)"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(add_sql)
            conn.commit()
        conn.close()

    def get_id_by_name(self, name):
        '''Obtiene el id según el nombre.'''
        get_id_by_name_sql = f"SELECT uid FROM users WHERE username LIKE '%{name}%' " + \
            "COLLATE NOCASE"

        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(get_id_by_name_sql)
            result = cursor.fetchall()
        return result
    
    def get_id(self, name, password):
        '''Obtiene el id de un usuario específico.'''
        get_id_by_name_sql = f"SELECT uid FROM users WHERE username='{name}' AND " + \
            f"password={password} COLLATE NOCASE"

        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(get_id_by_name_sql)
            result = cursor.fetchone()
        return result

    def get_name_by_id(self, user_id):
        '''Obtiene el nombre según el id.'''
        get_by_name_sql = f"SELECT username FROM users WHERE uid='{user_id}'"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(get_by_name_sql)
            result = cursor.fetchone()
        return result

    def rename_user(self, user_id, username):
        '''Renombra un registro.'''
        rename_user_sql = f"UPDATE users SET username='{username}' WHERE uid='{user_id}'"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(rename_user_sql)
            conn.commit()
        conn.close()

    def change_password(self, user_id, password_hash):
        '''Renombra un registro.'''
        rename_user_sql = f"UPDATE users SET password='{password_hash}' WHERE uid='{user_id}'"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(rename_user_sql)
            conn.commit()
        conn.close()

    def remove_user(self, user_id):
        '''Elimina un registro.'''
        remove_user_sql = f"DELETE FROM users WHERE uid='{user_id}'"
        with self._create_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(remove_user_sql)
            conn.commit()
        conn.close()