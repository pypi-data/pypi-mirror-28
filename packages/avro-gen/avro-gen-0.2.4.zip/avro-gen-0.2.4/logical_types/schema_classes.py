import json
import os.path
import decimal
import datetime
from avrogen.dict_wrapper import DictWrapper
from avrogen import logical
from avro import schema as avro_schema


def __read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

def __get_names_and_schema(file_name):
    names = avro_schema.Names()
    schema = avro_schema.make_avsc_object(json.loads(__read_file(file_name)), names)
    return names, schema

__NAMES, SCHEMA = __get_names_and_schema(os.path.join(os.path.dirname(__file__), "schema.avsc"))
__SCHEMAS = {}
def get_schema_type(fullname):
    return __SCHEMAS.get(fullname)
__SCHEMAS = dict((n.fullname, n) for n in __NAMES.names.itervalues())


class SchemaClasses(object):
    
    
    class LogicalTypesTestClass(DictWrapper):
        
        """
        
        """
        
        
        RECORD_SCHEMA = get_schema_type("LogicalTypesTest")
        
        
        def __init__(self, inner_dict=None):
            super(SchemaClasses.LogicalTypesTestClass, self).__init__(inner_dict)
            if inner_dict is None:
                self.decimalField = decimal.Decimal(0)
                self.decimalFieldWithDefault = decimal.Decimal(SchemaClasses.LogicalTypesTestClass.RECORD_SCHEMA.fields[1].default)
                self.decimalFieldWithDefault = decimal.Decimal(0)
                self.dateField = datetime.datetime.today().date()
                self.dateFieldWithDefault = logical.DateLogicalTypeProcessor().convert_back(SchemaClasses.LogicalTypesTestClass.RECORD_SCHEMA.fields[3].default)
                self.dateFieldWithDefault = datetime.datetime.today().date()
                self.timeMillisField = datetime.datetime.today().time()
                self.timeMillisFieldWithDefault = logical.TimeMicrosLogicalTypeProcessor().convert_back(SchemaClasses.LogicalTypesTestClass.RECORD_SCHEMA.fields[5].default)
                self.timeMillisFieldWithDefault = datetime.datetime.today().time()
                self.timeMicrosField = datetime.datetime.today().time()
                self.timeMicrosFieldWithDefault = logical.TimeMicrosLogicalTypeProcessor().convert_back(SchemaClasses.LogicalTypesTestClass.RECORD_SCHEMA.fields[7].default)
                self.timeMicrosFieldWithDefault = datetime.datetime.today().time()
                self.timestampMillisField = datetime.datetime.now()
                self.timestampMillisFieldWithDefault = logical.TimestampMillisLogicalTypeProcessor().convert_back(SchemaClasses.LogicalTypesTestClass.RECORD_SCHEMA.fields[9].default)
                self.timestampMillisFieldWithDefault = datetime.datetime.now()
                self.timestampMicrosField = datetime.datetime.now()
                self.timestampMicrosFieldWithDefault = logical.TimestampMicrosLogicalTypeProcessor().convert_back(SchemaClasses.LogicalTypesTestClass.RECORD_SCHEMA.fields[11].default)
                self.timestampMicrosFieldWithDefault = datetime.datetime.now()
        
        
        @property
        def decimalField(self):
            """
            :rtype: decimal.Decimal
            """
            return self._inner_dict.get('decimalField')
        
        @decimalField.setter
        def decimalField(self, value):
            #"""
            #:param decimal.Decimal value:
            #"""
            self._inner_dict['decimalField'] = value
        
        
        @property
        def decimalFieldWithDefault(self):
            """
            :rtype: decimal.Decimal
            """
            return self._inner_dict.get('decimalFieldWithDefault')
        
        @decimalFieldWithDefault.setter
        def decimalFieldWithDefault(self, value):
            #"""
            #:param decimal.Decimal value:
            #"""
            self._inner_dict['decimalFieldWithDefault'] = value
        
        
        @property
        def dateField(self):
            """
            :rtype: datetime.date
            """
            return self._inner_dict.get('dateField')
        
        @dateField.setter
        def dateField(self, value):
            #"""
            #:param datetime.date value:
            #"""
            self._inner_dict['dateField'] = value
        
        
        @property
        def dateFieldWithDefault(self):
            """
            :rtype: datetime.date
            """
            return self._inner_dict.get('dateFieldWithDefault')
        
        @dateFieldWithDefault.setter
        def dateFieldWithDefault(self, value):
            #"""
            #:param datetime.date value:
            #"""
            self._inner_dict['dateFieldWithDefault'] = value
        
        
        @property
        def timeMillisField(self):
            """
            :rtype: datetime.time
            """
            return self._inner_dict.get('timeMillisField')
        
        @timeMillisField.setter
        def timeMillisField(self, value):
            #"""
            #:param datetime.time value:
            #"""
            self._inner_dict['timeMillisField'] = value
        
        
        @property
        def timeMillisFieldWithDefault(self):
            """
            :rtype: datetime.time
            """
            return self._inner_dict.get('timeMillisFieldWithDefault')
        
        @timeMillisFieldWithDefault.setter
        def timeMillisFieldWithDefault(self, value):
            #"""
            #:param datetime.time value:
            #"""
            self._inner_dict['timeMillisFieldWithDefault'] = value
        
        
        @property
        def timeMicrosField(self):
            """
            :rtype: datetime.time
            """
            return self._inner_dict.get('timeMicrosField')
        
        @timeMicrosField.setter
        def timeMicrosField(self, value):
            #"""
            #:param datetime.time value:
            #"""
            self._inner_dict['timeMicrosField'] = value
        
        
        @property
        def timeMicrosFieldWithDefault(self):
            """
            :rtype: datetime.time
            """
            return self._inner_dict.get('timeMicrosFieldWithDefault')
        
        @timeMicrosFieldWithDefault.setter
        def timeMicrosFieldWithDefault(self, value):
            #"""
            #:param datetime.time value:
            #"""
            self._inner_dict['timeMicrosFieldWithDefault'] = value
        
        
        @property
        def timestampMillisField(self):
            """
            :rtype: datetime.datetime
            """
            return self._inner_dict.get('timestampMillisField')
        
        @timestampMillisField.setter
        def timestampMillisField(self, value):
            #"""
            #:param datetime.datetime value:
            #"""
            self._inner_dict['timestampMillisField'] = value
        
        
        @property
        def timestampMillisFieldWithDefault(self):
            """
            :rtype: datetime.datetime
            """
            return self._inner_dict.get('timestampMillisFieldWithDefault')
        
        @timestampMillisFieldWithDefault.setter
        def timestampMillisFieldWithDefault(self, value):
            #"""
            #:param datetime.datetime value:
            #"""
            self._inner_dict['timestampMillisFieldWithDefault'] = value
        
        
        @property
        def timestampMicrosField(self):
            """
            :rtype: datetime.datetime
            """
            return self._inner_dict.get('timestampMicrosField')
        
        @timestampMicrosField.setter
        def timestampMicrosField(self, value):
            #"""
            #:param datetime.datetime value:
            #"""
            self._inner_dict['timestampMicrosField'] = value
        
        
        @property
        def timestampMicrosFieldWithDefault(self):
            """
            :rtype: datetime.datetime
            """
            return self._inner_dict.get('timestampMicrosFieldWithDefault')
        
        @timestampMicrosFieldWithDefault.setter
        def timestampMicrosFieldWithDefault(self, value):
            #"""
            #:param datetime.datetime value:
            #"""
            self._inner_dict['timestampMicrosFieldWithDefault'] = value
        
        
    pass
    