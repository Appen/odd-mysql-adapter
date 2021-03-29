# https://dev.mysql.com/doc/refman/8.0/en/data-types.html
# 1) integer, smallint, decimal, numeric, float, real, double precision, bit
# date, time, datetime, timestamp, year
# char, varchar, binary, varbinary, blob, text, enum, set, json
# tinyblob, tinytext, mediumblob, mediumtext, longblob, longtext
# 2) tinyint, smallint, mediumint, int, integer, bigint
# float, double, double precision, real, decimal, numeric, bit

TYPES_SQL_TO_ODD = {

    "tinyint": "TYPE_INTEGER",
    "smallint": "TYPE_INTEGER",
    "mediumint": "TYPE_INTEGER",
    "int": "TYPE_INTEGER",
    "integer": "TYPE_INTEGER",
    "bigint": "TYPE_INTEGER",

    "float": "TYPE_NUMBER",
    "real": "TYPE_NUMBER",
    "double": "TYPE_NUMBER",
    "double precision": "TYPE_NUMBER",
    "decimal": "TYPE_NUMBER",
    "numeric": "TYPE_NUMBER",

    "bit": "TYPE_BINARY",
    "boolean": "TYPE_BOOLEAN",

    "char": "TYPE_CHAR",
    "varchar": "TYPE_STRING",
    "tinytext": "TYPE_STRING",
    "mediumtext": "TYPE_STRING",
    "longtext": "TYPE_STRING",
    "text": "TYPE_STRING",

    "interval": "TYPE_DURATION",
    "date": "TYPE_DATETIME",
    "time": "TYPE_DATETIME",
    "datetime": "TYPE_DATETIME",
    "timestamp": "TYPE_DATETIME",
    "year": "TYPE_INTEGER",

    "binary": "TYPE_BINARY",
    "varbinary": "TYPE_BINARY",
    "tinyblob": "TYPE_BINARY",
    "mediumblob": "TYPE_BINARY",
    "longblob": "TYPE_BINARY",
    "blob": "TYPE_BINARY",

    "json": "TYPE_STRING",

    "enum": "TYPE_UNION",
    "set": "TYPE_LIST"
}
