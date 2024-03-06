import pytest

from ninox import Ninox
from dotenv import load_dotenv, find_dotenv
from os import environ


@pytest.fixture
def api():
    load_dotenv(dotenv_path=".env")
    api_key = environ.get("NINOX_API_KEY")
    return Ninox(
        api_key=api_key,
    )


class TestApi:

    def test_workspaces(self, api):
        workspaces = api.get_workspaces()
        assert len(workspaces) > 0

        workspace = api.get_workspace(workspaces[0]["id"])
        assert workspace["id"] == workspaces[0]["id"]

    def test_databases(self, api):
        workspaces = api.get_workspaces()
        databases = api.get_databases(workspaces[0]["id"])
        assert len(databases) > 0

        database = api.get_database(workspaces[0]["id"], databases[0]["id"])
        assert len(database["schema"]) > 0
