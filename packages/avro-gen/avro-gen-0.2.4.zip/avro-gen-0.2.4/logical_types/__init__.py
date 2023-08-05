from .schema_classes import SchemaClasses
LogicalTypesTest = SchemaClasses.LogicalTypesTestClass


from .schema_classes import SchemaClasses, SCHEMA as my_schema, get_schema_type
from avro.io import DatumReader


class SpecificDatumReader(logical.LogicalDatumReader):
    SCHEMA_TYPES = {
        "LogicalTypesTest": SchemaClasses.LogicalTypesTestClass,
    }
    def __init__(self, readers_schema=None, **kwargs):
        super(SpecificDatumReader, self).__init__(readers_schema=readers_schema,**kwargs)
    def read_record(self, writers_schema, readers_schema, decoder):
        
        result = super(SpecificDatumReader, self).read_record(writers_schema, readers_schema, decoder)
        
        if readers_schema.fullname in SpecificDatumReader.SCHEMA_TYPES:
            result = SpecificDatumReader.SCHEMA_TYPES[readers_schema.fullname](result)
        
        return result