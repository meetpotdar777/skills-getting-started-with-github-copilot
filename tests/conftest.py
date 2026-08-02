import copy

import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity store before and after each test."""
    original = copy.deepcopy(app_module.activities)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))

    yield

    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
