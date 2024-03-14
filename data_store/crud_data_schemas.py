from pydantic import BaseModel
from typing import Optional, List, Any


class UpdateTableSchema(BaseModel):
    update_table: Optional[bool] = True
    table_name: str
    primary_key: dict
    sort_key: Optional[dict] = None
    data_to_update: Any


class ReadTableSchema(BaseModel):
    read_table: Optional[bool] = True
    table_name: str
    primary_key: str
    primary_key_value: str
    sort_key: Optional[str] = None
    sort_key_value: Optional[str] = None
    index_name: Optional[str] = None
    all_results: Optional[bool] = None


class CreateEntrySchema(BaseModel):
    add_row: Optional[bool] = True
    table_name: str
    row_data: Any


class DeleteEntrySchema(BaseModel):
    pass
