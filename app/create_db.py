import secrets

def generate_random_hex():
  """Generates a random 32-character hexadecimal string."""
  return secrets.token_hex(32)

if __name__ == "__main__":
  random_hex = generate_random_hex()
  print(random_hex)
