from collections.abc import Mapping
from asyncpg import Record

Mapping.register(Record)
