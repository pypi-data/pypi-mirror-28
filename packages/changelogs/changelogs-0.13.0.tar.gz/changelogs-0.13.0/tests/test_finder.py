import pytest
from changelogs.finder import contains_project_name


def test_contains_project_name():
    call = contains_project_name
    assert call("foolscap", "https://github.com/warner/foolscap/")
    assert call("Pillow", "https://github.com/python-pillow/pillow")
    assert call("python-boto", "https://github.com/bla/boto")
    assert call("py-boto", "https://github.com/bla/boto")
    assert call("acsone_recipe_odoo_pydev",
                "https://github.com/acsone/acsone.recipe.odoo.pydev/issues/1")
    assert call("xmlstats_py",
                "https://raw.githubusercontent.com/danielwelch/xmlstats-py/master/CHANGES.rst")


def test_not_contains_project_name():
    call = contains_project_name
    assert not call('dj-dashboard', 'https://github.com/audreyr/cookiecutter')
    assert not call('dj-dashboard', 'https://github.com/pydanny/cookiecutter-djangopackage')


def test_find_repo_urls():
    pass
