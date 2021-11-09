import bcrypt

def hashPassword(password):
     password = password.encode()
     salt = bcrypt.gensalt(12)
     encryptedPassword = bcrypt.hashpw(password, salt)
     return encryptedPassword

def comparePassword(password, password_db):
     checkPassword = bcrypt.checkpw(password, password_db)
     return checkPassword