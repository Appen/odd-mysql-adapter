from collections import namedtuple

_adapter_prefix: str = "mysql/"

_data_set_metadata_schema_url: str = \
    "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/" \
    "extensions/mysql.json#/definitions/MysqlDataSetExtension"
_data_set_field_metadata_schema_url: str = \
    "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/" \
    "extensions/mysql.json#/definitions/MysqlDataSetFieldExtension"

_table_metadata: str = \
    "table_catalog, table_schema, table_name, table_type, engine, version, row_format, table_rows, " \
    "avg_row_length, data_length, max_data_length, index_length, data_free, auto_increment, create_time, " \
    "update_time, check_time, table_collation, checksum, create_options, table_comment"
_table_table: str = "information_schema.tables"
_table_order_by: str = "table_catalog, table_schema, table_name"

_column_metadata: str = \
    "table_catalog, table_schema, table_name, column_name, ordinal_position, column_default, is_nullable, " \
    "data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_scale, " \
    "datetime_precision, character_set_name, collation_name, column_type, column_key, extra, privileges, " \
    "column_comment, generation_expression"  # , srs_id"  # column is not included in MariaDB (MySQL only)
_column_table: str = "information_schema.columns"
_column_order_by: str = f"{_table_order_by}, ordinal_position"

MetadataNamedtuple = namedtuple("MetadataNamedtuple", _table_metadata)
ColumnMetadataNamedtuple = namedtuple("ColumnMetadataNamedtuple", _column_metadata)
