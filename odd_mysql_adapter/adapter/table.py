from odd_contract.models import DataEntity, DataSet, DataTransformer, Type, DataEntityType
from . import MetadataNamedtuple, ColumnMetadataNamedtuple, \
    _data_set_metadata_schema_url, _data_set_metadata_excluded_keys
from .column import map_column
from .metadata import append_metadata_extension
from .type import TABLE_TYPES_SQL_TO_ODD
from odd_mysql_adapter.app.oddrn import generate_table_oddrn, generate_schema_oddrn

import pytz


def map_tables(data_source_oddrn: str, tables: list[tuple], columns: list[tuple]) -> list[DataEntity]:
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
        data_entity: DataEntity = DataEntity(
            oddrn=table_oddrn,
            name=table_name,
            type=TABLE_TYPES_SQL_TO_ODD.get(metadata.table_type, DataEntityType.UNKNOWN),
            owner=metadata.table_schema,
            description=metadata.table_comment,
            metadata=[],
        )
        data_entities.append(data_entity)

        if metadata.table_type == 'BASE TABLE':
            # it is for full tables only
            append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url, metadata,
                                      _data_set_metadata_excluded_keys)

        if metadata.create_time is not None:
            data_entity.created_at = metadata.create_time.replace(tzinfo=pytz.utc).isoformat()
        if metadata.update_time is not None:
            data_entity.updated_at = metadata.update_time.replace(tzinfo=pytz.utc).isoformat()

        # Dataset
        data_entity.dataset = DataSet(
            parent_oddrn=schema_oddrn,
            rows_number=metadata.table_rows,
            field_list=[]
        )

        # DataTransformer
        if metadata.table_type == 'VIEW':
            data_entity.data_transformer = DataTransformer(sql=metadata.view_definition, inputs=[], outputs=[])

        # DatasetField
        while column_index < len(columns):
            column: tuple = columns[column_index]
            column_metadata: ColumnMetadataNamedtuple = ColumnMetadataNamedtuple(*column)

            if column_metadata.table_catalog == table_catalog and \
                    column_metadata.table_schema == table_schema and \
                    column_metadata.table_name == table_name:
                data_entity.dataset.field_list.append(map_column(column_metadata, data_entity.owner, table_oddrn))
                column_index += 1
            else:
                break

    return data_entities
