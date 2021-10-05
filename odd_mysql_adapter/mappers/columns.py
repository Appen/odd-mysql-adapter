from odd_contract.models import DataSetField, DataSetFieldType, Type
from . import (
    ColumnMetadataNamedtuple, _data_set_field_metadata_schema_url, _data_set_field_metadata_excluded_keys
)
from .metadata import append_metadata_extension, convert_bytes_to_str
from .types import TYPES_SQL_TO_ODD


def map_column(column_metadata: ColumnMetadataNamedtuple,
               owner: str, table_oddrn: str, parent_oddrn: str = None,
               is_key: bool = None, is_value: bool = None
               ) -> DataSetField:
    name: str = column_metadata.column_name
    resource_name: str = 'keys' if is_key else 'values' if is_value else 'subcolumns'

    data_type: str = convert_bytes_to_str(column_metadata.data_type)
    description = convert_bytes_to_str(column_metadata.column_comment)
    dsf: DataSetField = DataSetField(
        oddrn=f'{table_oddrn}/columns/{name}' if parent_oddrn is None else f'{parent_oddrn}/{resource_name}/{name}',
        name=name,
        owner=owner,
        metadata=[],
        type=DataSetFieldType(
            type=TYPES_SQL_TO_ODD.get(data_type, Type.TYPE_UNKNOWN),
            logical_type=convert_bytes_to_str(column_metadata.data_type),
            is_nullable=column_metadata.is_nullable == 'YES'
        ),
        default_value=convert_bytes_to_str(column_metadata.column_default),
        description=description or None
    )

    if convert_bytes_to_str(column_metadata.column_comment) != '':
        dsf.description = convert_bytes_to_str(column_metadata.column_comment)

    append_metadata_extension(dsf.metadata, _data_set_field_metadata_schema_url, column_metadata,
                              _data_set_field_metadata_excluded_keys)

    return dsf
