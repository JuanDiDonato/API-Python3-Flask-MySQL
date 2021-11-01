import bcrypt

def hashPassword(password):
     password = password.encode()
     salt = bcrypt.gensalt(12)
     encryptedPassword = bcrypt.hashpw(password, salt)
     return encryptedPassword

def comparePassword(password, dbPassword):
     checkPassword = bcrypt.checkpw(password, dbPassword)
     return checkPassword