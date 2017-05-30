from app import DB, BCRYPT

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = BCRYPT.generate_password_hash(password)

    def verify_password(self, password):
        return BCRYPT.check_password_hash(password, self.password_hash)