from replit import db

#print("Raw Data:\nvalid:", db["valid"], "\n\ninvalid:", db["invalid"])

print("\n--- Valid credentials ---")
for i in range(len(db["valid"])):
  print("Username:", db["valid"][i][0], ", Password:", db["valid"][i][1])
  for j in db["valid"][i][2]:
    print("   ", j, ": ", db["valid"][i][2][j])

print("\n--- Invalid credentials ---")
for i in range(len(db["invalid"])):
  print("Username:", db["invalid"][i][0], ", Password:", db["invalid"][i][1])
  for j in db["invalid"][i][2]:
    print("   ", j, ": ", db["invalid"][i][2][j])