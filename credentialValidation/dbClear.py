from replit import db


del db["valid"]
del db["invalid"]

db["valid"] = list()
db["invalid"] = list()


print("\nValid:", db["valid"], "\n\nInvalid:", db["invalid"])