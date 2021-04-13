from odd_contract.models import DataSetField, DataSetFieldType
from adapter import ColumnMetadataNamedtuple, \
    _data_set_field_metadata_schema_url, _data_set_field_metadata_excluded_keys
from adapter.metadata import _append_metadata_extension, _convert_bytes_to_str
from adapter.type import TYPES_SQL_TO_ODD


def _map_column(column_metadata: ColumnMetadataNamedtuple,
                owner: str, table_oddrn: str, parent_oddrn: str = None,
                is_key: bool = None, is_value: bool = None
                ) -> list[DataSetField]:
    result: list[DataSetField] = []

    name: str = column_metadata.column_name
    resource_name: str = 'keys' if is_key else 'values' if is_value else 'subcolumns'

    dsf: DataSetField = DataSetField()

    dsf.oddrn = f'{table_oddrn}/columns/{name}' if parent_oddrn is None else f'{parent_oddrn}/{resource_name}/{name}'
    dsf.name = name
    dsf.owner = owner

    dsf.metadata = []
    _append_metadata_extension(dsf.metadata, _data_set_field_metadata_schema_url, column_metadata,
                               _data_set_field_metadata_excluded_keys)

    # dsf.parent_field_oddrn = parent_oddrn

    dsf.type = DataSetFieldType()
    data_type: str = _convert_bytes_to_str(column_metadata.data_type)
    dsf.type.type = TYPES_SQL_TO_ODD[data_type] if data_type in TYPES_SQL_TO_ODD else 'TYPE_UNKNOWN'
    dsf.type.logical_type = _convert_bytes_to_str(column_metadata.column_type)
    dsf.type.is_nullable = True if column_metadata.is_nullable == 'YES' else False

    # dsf.is_key = bool(is_key)
    # dsf.is_value = bool(is_value)
    dsf.default_value = _convert_bytes_to_str(column_metadata.column_default)
    if _convert_bytes_to_str(column_metadata.column_comment) != '':
        dsf.description = _convert_bytes_to_str(column_metadata.column_comment)

    result.append(dsf)
    return result
