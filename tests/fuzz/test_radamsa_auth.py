import sys

from src.auth_logic import authenticate


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_radamsa_auth.py <input_file>")
        sys.exit(2)

    with open(sys.argv[1], "rb") as f:
        data = f.read()

    text = data.decode("utf-8", errors="ignore")

    if ":" in text:
        login, password = text.split(":", 1)
    else:
        login = text
        password = ""

    result = authenticate(login, password)

    if not isinstance(result, bool):
        raise RuntimeError("authenticate() returned non-bool result")


if __name__ == "__main__":
    main()
