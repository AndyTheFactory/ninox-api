from pathlib import Path
from typing import Dict, Union
from ninox.api.adapter import NinoxApi


class Ninox:

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.ninox.com",
        version: str = "v1",
        skip_ssl_validation: bool = False,
    ) -> None:
        self.adapter = NinoxApi(api_key, base_url, version, skip_ssl_validation)

    def get_workspaces(self):
        return self.adapter.get("teams")

    def get_workspace(self, workspace_id: str):
        return self.adapter.get(f"teams/{workspace_id}")

    def get_databases(self, workspace_id: str):
        return self.adapter.get(f"teams/{workspace_id}/databases")

    def get_database(self, workspace_id: str, database_id: str):
        return self.adapter.get(f"teams/{workspace_id}/databases/{database_id}")

    def query(self, workspace_id: str, database_id: str, query: str):
        return self.adapter.post(
            f"teams/{workspace_id}/databases/{database_id}/query", data={"query": query}
        )

    def exec(self, workspace_id: str, database_id: str, query: str):
        return self.adapter.post(
            f"teams/{workspace_id}/databases/{database_id}/exec", data={"query": query}
        )

    def get_schemas(self, workspace_id: str, database_id: str):
        return self.adapter.get(f"teams/{workspace_id}/databases/{database_id}/tables")

    def get_schema(self, workspace_id: str, database_id: str, table_id: str):
        return self.adapter.get(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}"
        )

    def get_records(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        choice_style: str = "id",
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records",
            params={"choiceStyle": choice_style},
        )

    def get_record(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        choice_style: str = "id",
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records/{record_id}",
            params={"choiceStyle": choice_style},
        )

    def update_record(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        data: dict,
    ):
        return self.adapter.put(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records/{record_id}",
            data=data,
        )

    def search_record(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        query: Union[Dict, str],
        choice_style: str = "id",
        date_style: str = "id",
    ):
        return self.adapter.request(
            method="POST",
            endpoint=f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records",
            data=query,
            params={"choiceStyle": choice_style, "dateStyle": date_style},
        )

    def upsert_records(
        self, workspace_id: str, database_id: str, table_id: str, data: list
    ):
        return self.adapter.post(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records",
            data=data,
        )

    def get_database_changes(
        self, workspace_id: str, database_id: str, table_id: str, since_seqnr: str
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/databases/{database_id}/changes",
            params={"sinceSq": since_seqnr},
        )

    def get_table_changes(
        self, workspace_id: str, database_id: str, table_id: str, since_seqnr: str
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/changes",
            params={"sinceSq": since_seqnr},
        )

    def get_record_changes(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        since_seqnr: str,
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records/{record_id}/changes",
            params={"sinceSq": since_seqnr},
        )

    def delete_record(
        self, workspace_id: str, database_id: str, table_id: str, record_id: str
    ):
        return self.adapter.delete(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records/{record_id}"
        )

    def delete_records(
        self, workspace_id: str, database_id: str, table_id: str, record_ids: list
    ):
        return self.adapter.post(
            f"teams/{workspace_id}/databases/{database_id}/tables/{table_id}/records/delete",
            data=record_ids,
        )

    def get_file(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        filename: str,
    ):
        return self.adapter.post(
            f"teams/{workspace_id}/database/{database_id}/table/{table_id}/records/{record_id}/files/{filename}"
        )

    def upload_file(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        file_path: str,
    ):
        return self.adapter.post(
            f"teams/{workspace_id}/database/{database_id}/table/{table_id}/records/{record_id}/files",
            files={"file": (Path(file_path).name, open(file_path, "rb"))},
        )

    def delete_file(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        filename: str,
    ):
        return self.adapter.delete(
            f"teams/{workspace_id}/database/{database_id}/table/{table_id}/records/{record_id}/files/{filename}"
        )

    def get_files_metadata(
        self, workspace_id: str, database_id: str, table_id: str, record_id: str
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/database/{database_id}/table/{table_id}/records/{record_id}/files"
        )

    def get_file_metadata(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        filename: str,
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/database/{database_id}/table/{table_id}/records/{record_id}/files/{filename}/metadata"
        )

    def get_file_thumbnail(
        self,
        workspace_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        filename: str,
    ):
        return self.adapter.get(
            f"teams/{workspace_id}/database/{database_id}/table/{table_id}/records/{record_id}/files/{filename}/thumb.jpg"
        )
