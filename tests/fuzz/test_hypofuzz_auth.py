from hypothesis import given, settings, strategies as st

from src.auth_logic import authenticate


@given(
    st.text(),
    st.text()
)
def test_auth_fuzz(login, password):
    result = authenticate(login, password)
    assert isinstance(result, bool)

@given(data=st.binary(min_size=0, max_size=4096))
@settings(max_examples=3000, deadline=500)
def test_auth_fuzz_binary_decoded(data):
    text = data.decode("utf-8", errors="ignore")

    if ":" in text:
        login, password = text.split(":", 1)
    else:
        login, password = text, ""

    result = authenticate(login, password)

    assert isinstance(result, bool)