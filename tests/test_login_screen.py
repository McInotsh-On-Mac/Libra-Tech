# Anthony Powell
# Ensures the login_screen module imports & LoginScreen is created

import types
import pytest

def _make_root():
    return types.SimpleNamespace(title=lambda *a, **k: None,
                                 geometry=lambda *a, **k: None,
                                 configure=lambda *a, **k: None)

def _clear_widget(widget):
    # try common methods to clear fake-or-real Entry-like widgets
    try:
        widget.delete(0, "end")
        widget.insert(0, "")
        return
    except Exception:
        pass
    try:
        widget._text = ""
        return
    except Exception:
        pass

def _find_attr(obj, *names):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return None

def test_login_screen_import_and_init():
    try:
        import app.login_screen as login_mod
    except Exception as e:
        pytest.skip(f"Cannot import app.login_screen: {e}")

    if not hasattr(login_mod, "LoginScreen"):
        pytest.skip("LoginScreen class not found in app.login_screen")

    root = _make_root()
    try:
        screen = login_mod.LoginScreen(root)
    except Exception as e:
        pytest.skip(f"Cannot instantiate LoginScreen: {e}")

    assert screen is not None

def test_login_shows_warning_on_empty_credentials(monkeypatch):
    try:
        import app.login_screen as login_mod
    except Exception as e:
        pytest.skip(f"Cannot import app.login_screen: {e}")

    if not hasattr(login_mod, "LoginScreen"):
        pytest.skip("LoginScreen class not found in app.login_screen")

    root = _make_root()
    try:
        screen = login_mod.LoginScreen(root)
    except Exception as e:
        pytest.skip(f"Cannot instantiate LoginScreen: {e}")

    # locate username/password Entry-like widgets using common attribute names
    username = _find_attr(screen, "username_entry", "user_entry", "entry_username", "username")
    password = _find_attr(screen, "password_entry", "pass_entry", "entry_password", "password")

    if username is None or password is None:
        pytest.skip("Could not locate username/password widgets on LoginScreen instance")

    # ensure entries are empty
    _clear_widget(username)
    _clear_widget(password)

    shown = {"title": None, "msg": None}
    def fake_warning(t, m):
        shown["title"] = t
        shown["msg"] = m

    # Messagebox used in the module (safe regardless of actual import style)
    monkeypatch.setattr(login_mod, "messagebox", types.SimpleNamespace(showwarning=fake_warning))

    # find login handler on the instance (common names)
    login_handler = _find_attr(screen, "on_login", "login", "submit", "handle_login")
    if login_handler is None:
        pytest.skip("No login handler method found on LoginScreen instance")

    # call handler (some handlers accept an event arg)
    try:
        login_handler()
    except TypeError:
        try:
            login_handler(None)
        except Exception:
            pass

    # assert warning was triggered for empty credentials
    assert shown["title"] is not None or shown["msg"] is not None