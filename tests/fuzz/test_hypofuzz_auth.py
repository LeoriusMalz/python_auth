from hypothesis import given, strategies as st

from src.auth_logic import authenticate


@given(
    st.text(),
    st.text()
)
def test_auth_fuzz(login, password):
    result = authenticate(login, password)
    assert isinstance(result, bool)