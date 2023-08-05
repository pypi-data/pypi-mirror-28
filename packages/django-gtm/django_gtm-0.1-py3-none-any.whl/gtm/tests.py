import pytest

from .models import GTMSettings
from .context_processors import gtm


@pytest.mark.django_db
def test_singleton():
    """
    GTMSettings is a Singleton object.
    """
    gtm = GTMSettings.load()
    assert gtm.id == GTMSettings.load().id
