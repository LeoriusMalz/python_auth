from hashlib import sha256


RELEASE_DATABASE = {
    "admin": "a35c5f63916fff41369754c7a01cc4a82e9e3e5f1e05628791b5f5770435d6b0",  # @dm1n
    "vovuas": "77459b9b941bcb4714d0c121313c900ecf30541d158eb2b9b178cdb8eca6457e",  # 2003
}


def myhash(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be str")

    return sha256(value.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str, database=None) -> bool:
    if not isinstance(login, str):
        raise TypeError("login must be str")

    if not isinstance(password, str):
        raise TypeError("password must be str")

    if database is None:
        database = RELEASE_DATABASE

    password_hash = myhash(password)
    real_hash = database.get(login)

    if real_hash is None:
        return False

    return password_hash == real_hash