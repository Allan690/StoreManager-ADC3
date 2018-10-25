from werkzeug.security import generate_password_hash
from .db_connect import DatabaseConnection


class User(DatabaseConnection):
    def __init__(self, data):
        super().__init__()
        self.username = data['username']
        self.password = generate_password_hash(data['password'])
        self.email = data['email']
        self.role = data['role']

        db = DatabaseConnection()
        db.create_db_tables()
        self.conn = db.connection()

    def add_user(self):
        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
            (self.email, self.password, self.role)
        )
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        db = DatabaseConnection()
        self.conn = db.connection()
        db.create_db_tables()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()
        users = []
        user_result = {}

        for user in results:
            user_result['user_id'] = user[0]
            user_result["email"] = user[1]
            user_result["password"] = user[2]
            user_result['role'] = user[3]
            users.append(user_result)

        self.conn.close()
        return users