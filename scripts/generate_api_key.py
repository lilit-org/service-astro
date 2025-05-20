import secrets
import string


LENGTH = 50


def generate_api_key(length=LENGTH):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    api_key = generate_api_key()
    print("\n" + "-" * LENGTH + "\n")
    print(api_key)
    print("\n" + "-" * LENGTH + "\n")
