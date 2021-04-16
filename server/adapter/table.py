from odd_contract.models import DataEntity, DataSet, DataTransformer
from adapter import MetadataNamedtuple, ColumnMetadataNamedtuple, \
    _data_set_metadata_schema_url, _data_set_metadata_excluded_keys
from adapter.column import _map_column
from adapter.metadata import _append_metadata_extension
from adapter.type import TABLE_TYPES_SQL_TO_ODD
from app.oddrn import generate_table_oddrn, generate_schema_oddrn


def _map_table(data_source_oddrn: str, tables: list[tuple], columns: list[tuple]) -> list[DataEntity]:
    data_entities: list[DataEntity] = []
    column_index: int = 0

    for table in tables:
        metadata: MetadataNamedtuple = MetadataNamedtuple(*table)

        table_catalog: str = metadata.table_catalog
        table_schema: str = metadata.table_schema
        table_name: str = metadata.table_name

        schema_oddrn: str = generate_schema_oddrn(data_source_oddrn, table_catalog, table_schema)
        table_oddrn: str = generate_table_oddrn(data_source_oddrn, table_catalog, table_schema, table_name)

        # DataEntity
        data_entity: DataEntity = DataEntity()
        data_entities.append(data_entity)

        data_entity.oddrn = table_oddrn
        data_entity.name = table_name
        data_entity.owner = metadata.table_schema

        if metadata.table_type == 'BASE TABLE':  # data_entity.dataset.subtype == 'DATASET_TABLE'
            data_entity.metadata = []
            # it is for full tables only
            _append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url, metadata,
                                       _data_set_metadata_excluded_keys)

        if metadata.create_time is not None:
            data_entity.created_at = metadata.create_time.isoformat()
        if metadata.update_time is not None:
            data_entity.updated_at = metadata.update_time.isoformat()
        else:
            if metadata.create_time is not None:
                data_entity.updated_at = data_entity.created_at

        data_entity.dataset = DataSet()

        data_entity.dataset.parent_oddrn = schema_oddrn
        if not (metadata.table_comment == '' or (metadata.table_type == 'VIEW' and metadata.table_comment == 'VIEW')):
            data_entity.dataset.description = metadata.table_comment

        data_entity.dataset.rows_number = metadata.table_rows

        data_entity.dataset.subtype = TABLE_TYPES_SQL_TO_ODD[metadata.table_type] \
            if metadata.table_type in TABLE_TYPES_SQL_TO_ODD else 'DATASET_TABLE'  # DATASET_UNKNOWN

        data_entity.dataset.field_list = []

        # DataTransformer
        if metadata.table_type == 'VIEW':  # data_entity.dataset.subtype == 'DATASET_VIEW'
            data_entity.data_transformer = DataTransformer()

            if not (metadata.table_comment == '' or metadata.table_comment == 'VIEW'):
                data_entity.data_transformer.description = metadata.table_comment
            # data_entity.data_transformer.source_code_url = None
            data_entity.data_transformer.sql = metadata.view_definition

            data_entity.data_transformer.inputs = []
            data_entity.data_transformer.outputs = []

            data_entity.data_transformer.subtype = 'DATATRANSFORMER_VIEW'

        # DatasetField
        while column_index < len(columns):
            column: tuple = columns[column_index]
            column_metadata: ColumnMetadataNamedtuple = ColumnMetadataNamedtuple(*column)

            if column_metadata.table_catalog == table_catalog and \
                    column_metadata.table_schema == table_schema and \
                    column_metadata.table_name == table_name:
                data_entity.dataset.field_list.extend(_map_column(column_metadata, data_entity.owner, table_oddrn))
                column_index += 1
            else:
                break

    return data_entities
