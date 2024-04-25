import bcrypt

# Création du mot de passe haché
password = "ozzri123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

print(hashed)
