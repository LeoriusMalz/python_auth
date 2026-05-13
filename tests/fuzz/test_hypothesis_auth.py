import pytest
from hypothesis import given, settings, strategies as st

from src.auth_logic import authenticate, myhash


@given(value=st.text(min_size=0, max_size=4096))
@settings(max_examples=3000, deadline=500)
def test_myhash_does_not_crash_on_text(value):
    result = myhash(value)

    assert isinstance(result, str)
    assert len(result) == 64


@given(
    login=st.text(min_size=0, max_size=1024),
    password=st.text(min_size=0, max_size=1024),
)
@settings(max_examples=3000, deadline=500)
def test_authenticate_does_not_crash_on_text(login, password):
    result = authenticate(login, password)

    assert isinstance(result, bool)


@given(data=st.binary(min_size=0, max_size=4096))
@settings(max_examples=3000, deadline=500)
def test_authenticate_does_not_crash_on_binary_decoded_input(data):
    text = data.decode("utf-8", errors="ignore")

    if ":" in text:
        login, password = text.split(":", 1)
    else:
        login, password = text, ""

    result = authenticate(login, password)

    assert isinstance(result, bool)


def test_valid_admin_credentials():
    assert authenticate("admin", "@dm1n") is True


def test_valid_vovuas_credentials():
    assert authenticate("vovuas", "2003") is True


def test_invalid_credentials():
    assert authenticate("admin", "wrong") is False
    assert authenticate("unknown", "2003") is False

def test_myhash_rejects_non_string():
    with pytest.raises(TypeError):
        myhash(123)


def test_authenticate_rejects_non_string_login():
    with pytest.raises(TypeError):
        authenticate(123, "password")


def test_authenticate_rejects_non_string_password():
    with pytest.raises(TypeError):
        authenticate("admin", 123)