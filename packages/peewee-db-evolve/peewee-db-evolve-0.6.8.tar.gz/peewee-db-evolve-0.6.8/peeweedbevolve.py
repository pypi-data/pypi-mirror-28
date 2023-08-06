from __future__ import print_function

import collections, re, sys, time, traceback

try:
  import colorama
  colorama.init()
except ImportError:
  print('colorama not installed')

try:
  import peewee as pw
  import playhouse.migrate
except ImportError:
  print('peewee or herman not installed')
  # don't error, because setup needs to be able to run this to get the version

if sys.version_info >= (3,0):
  raw_input = input


DEBUG = False

# peewee doesn't do defaults in the database - doh!
DIFF_DEFAULTS = False

__version__ = '0.6.8'


try:
  UNICODE_EXISTS = bool(type(unicode))
except NameError:
  unicode = lambda s: str(s)


def mark_fks_as_deferred(table_names):
  add_fks = []
  table_names_to_models = {cls._meta.db_table:cls for cls in all_models.keys() if cls._meta.db_table in table_names}
  for model in table_names_to_models.values():
    for field in model._meta.sorted_fields:
      if isinstance(field, pw.ForeignKeyField):
        add_fks.append(field)
        if not field.deferred:
          field.__pwdbev__not_deferred = True
          field.deferred = True
  return add_fks
  
def calc_table_changes(existing_tables, ignore_tables=None):
  if ignore_tables:
    ignore_tables = set(ignore_tables) | globals()['ignore_tables']
  else:
    ignore_tables = globals()['ignore_tables']
  existing_tables = set(existing_tables)
  table_names_to_models = {unicode(cls._meta.db_table):cls for cls in all_models.keys()}
  defined_tables = set(table_names_to_models.keys())
  adds = defined_tables - existing_tables - ignore_tables
  deletes = existing_tables - defined_tables - ignore_tables
  renames = {}
  for to_add in list(adds):
    cls = table_names_to_models[to_add]
    if hasattr(cls._meta, 'aka'):
      akas = cls._meta.aka
      if hasattr(akas, 'lower'):
        akas = [akas]
      for a in akas:
        a = unicode(a)
        if a in deletes:
          renames[a] = to_add
          adds.remove(to_add)
          deletes.remove(a)
          break
  add_fks = mark_fks_as_deferred(adds)
  return adds, add_fks, deletes, renames
  
def is_postgres(db):
  return isinstance(db, pw.PostgresqlDatabase)

def is_mysql(db):
  return isinstance(db, pw.MySQLDatabase)

def is_sqlite(db):
  return isinstance(db, pw.SqliteDatabase)

def auto_detect_migrator(db):
  if is_postgres(db):
    return playhouse.migrate.PostgresqlMigrator(db)
  if is_sqlite(db):
    return playhouse.migrate.SqliteMigrator(db)
  if is_mysql(db):
    return playhouse.migrate.MySQLMigrator(db)
  raise Exception("could not auto-detect migrator for %s - please provide one via the migrator kwarg" % repr(db.__class__.__name__))

_re_varchar = re.compile('^varchar[(]\\d+[)]$')
def normalize_column_type(t):
  t = t.lower()
  if t in ['serial','int','integer auto_increment']: t = 'integer'
  if t in ['timestamp without time zone']: t = 'timestamp'
  if t in ['timestamp with time zone', 'datetime_tz']: t = 'timestamptz'
  if t in ['time without time zone']: t = 'time'
  if t in ['character varying']: t = 'varchar'
  if _re_varchar.match(t): t = 'varchar'
  if t in ['decimal','real']: t = 'numeric'
  return unicode(t)
  
def normalize_field_type(field, qc):
#  t = field.get_column_type()
  t = qc.get_column_type(field.get_db_field())
  return normalize_column_type(t)
  
  
def normalize_default(default):
  if default is None: return None
  if hasattr(default, 'lower'):
    default = unicode(default)
    if default.startswith('nextval('): return None
    default = default.split('::')[0]
    default = default.strip("'")
  return default
  
def can_convert(type1, type2):
  if type1=='array': return False
  return True

def are_data_types_equal(db, type_a, type_b):
  if type_a == type_b: return True
  type_a, type_b = sorted([type_a, type_b])
  if is_mysql(db) and type_a=='bool' and type_b=='tinyint': return True
  if is_postgres(db) and type_a=='char' and type_b=='character': return True
  return False
  
def column_def_changed(db, a, b):
  # b is the defined column
  return (
    a.null!=b.null or 
    not are_data_types_equal(db, a.data_type, b.data_type) or 
    a.max_length!=b.max_length or 
    (b.precision is not None and a.precision!=b.precision) or 
    (b.scale is not None and a.scale!=b.scale) or 
    a.primary_key!=b.primary_key or
    (DIFF_DEFAULTS and normalize_default(a.default)!=normalize_default(b.default))
  )

ColumnMetadata = collections.namedtuple('ColumnMetadata', (
  'name', 'data_type', 'null', 'primary_key', 'table', 'default', 'max_length', 'precision', 'scale'
))

def get_columns_by_table(db, schema='public'):
  columns_by_table = collections.defaultdict(list)
  if is_postgres(db) or is_mysql(db):
    if schema=='public' and is_mysql(db):
      schema_check = 'c.table_schema=DATABASE()'
      params = []
    else:
      schema_check = 'c.table_schema=%s'
      params = [schema]
    sql = '''
        select 
          c.column_name, 
          c.data_type, 
          c.is_nullable='YES' as is_nullable, 
          coalesce(tc.constraint_type='PRIMARY KEY',false) as primary_key, 
          c.table_name, 
          c.column_default,
          c.character_maximum_length as max_length,
          c.numeric_precision,
          c.numeric_scale
        from information_schema.columns as c
        left join information_schema.key_column_usage as kcu
        on (c.table_name=kcu.table_name and c.table_schema=kcu.table_schema and c.column_name=kcu.column_name)
        left join information_schema.table_constraints as tc
        on (tc.table_name=kcu.table_name and tc.table_schema=kcu.table_schema and tc.constraint_name=kcu.constraint_name)
        where %s
        order by c.ordinal_position
    ''' % schema_check
    cursor = db.execute_sql(sql, params)
  else:
    raise Exception("don't know how to get columns for %s" % db)
  for row in cursor.fetchall():
    data_type = normalize_column_type(row[1])
    max_length = None if row[6]==4294967295 else row[6] # MySQL returns 4294967295L for LONGTEXT fields
    default = None if row[5] is not None and row[5].startswith('nextval') else row[5]
    precision = row[7] if data_type=='numeric' else None
    scale = row[8] if data_type=='numeric' else None
    column = ColumnMetadata(row[0], data_type, row[2], row[3], row[4], default, max_length, precision, scale)
    columns_by_table[column.table].append(column)
  return columns_by_table

ForeignKeyMetadata = collections.namedtuple('ForeignKeyMetadata', ('column', 'dest_table', 'dest_column', 'table', 'name'))
    
def get_foreign_keys_by_table(db, schema='public'):
  fks_by_table = collections.defaultdict(list)
  if is_postgres(db):
    sql = """
      select kcu.column_name, ccu.table_name, ccu.column_name, tc.table_name, tc.constraint_name
      from information_schema.table_constraints as tc
      join information_schema.key_column_usage as kcu
        on (tc.constraint_name = kcu.constraint_name and tc.constraint_schema = kcu.constraint_schema)
      join information_schema.constraint_column_usage as ccu
        on (ccu.constraint_name = tc.constraint_name and ccu.constraint_schema = tc.constraint_schema)
      where tc.constraint_type = 'FOREIGN KEY' and tc.table_schema = %s
    """
    cursor = db.execute_sql(sql, (schema,))
  elif is_mysql(db):
    sql = """
      select column_name, referenced_table_name, referenced_column_name, table_name, constraint_name
      from information_schema.key_column_usage
      where table_schema=database() and referenced_table_name is not null and referenced_column_name is not null
    """
    cursor = db.execute_sql(sql, [])
  elif is_sqlite(db):
    # does not work
    sql = """
      SELECT sql
        FROM (
              SELECT sql sql, type type, tbl_name tbl_name, name name
                FROM sqlite_master
               UNION ALL
              SELECT sql, type, tbl_name, name
                FROM sqlite_temp_master
             )
       WHERE type != 'meta'
         AND sql NOTNULL
         AND name NOT LIKE 'sqlite_%'
         AND sql LIKE '%REFERENCES%'
       ORDER BY substr(type, 2, 1), name
    """
    cursor = db.execute_sql(sql, [])
  else:
    raise Exception("don't know how to get FKs for %s" % db)
  for row in cursor.fetchall():
    fk = ForeignKeyMetadata(row[0], row[1], row[2], row[3], row[4])
    fks_by_table[fk.table].append(fk)
  return fks_by_table

def get_indexes_by_table(db, table, schema='public'):
  # peewee's get_indexes returns the columns in an index in arbitrary order
  if is_postgres(db):
    query = '''
      select index_class.relname,
        idxs.indexdef,
        array_agg(table_attribute.attname order by array_position(index.indkey, table_attribute.attnum)),
        index.indisunique,
        table_class.relname
      from pg_catalog.pg_class index_class
      join pg_catalog.pg_index index on index_class.oid = index.indexrelid
      join pg_catalog.pg_class table_class on table_class.oid = index.indrelid
      join pg_catalog.pg_attribute table_attribute on table_class.oid = table_attribute.attrelid and table_attribute.attnum = any(index.indkey)
      join pg_catalog.pg_indexes idxs on idxs.tablename = table_class.relname and idxs.indexname = index_class.relname
      where table_class.relname = %s and table_class.relkind = %s and idxs.schemaname = %s
      group by index_class.relname, idxs.indexdef, index.indisunique, table_class.relname;
    '''
    cursor = db.execute_sql(query, (table, 'r', schema))
    return [pw.IndexMetadata(*row) for row in cursor.fetchall()]
  else:
    return db.get_indexes(table, schema=schema)

def calc_column_changes(db, migrator, etn, ntn, existing_columns, defined_fields, existing_fks):
  qc = db.compiler()
  defined_fields_by_column_name = {unicode(f.db_column):f for f in defined_fields}
  defined_columns = [ColumnMetadata(
    unicode(f.db_column),
    normalize_field_type(f, qc),
    f.null,
    f.primary_key,
    unicode(ntn),
    f.default,
    f.max_length if hasattr(f,'max_length') else None,
    f.max_digits if hasattr(f,'max_digits') else None,
    f.decimal_places if hasattr(f,'decimal_places') else None,
  ) for f in defined_fields if isinstance(f, pw.Field)]
  
  existing_cols_by_name = {c.name:c for c in existing_columns}
  defined_cols_by_name = {c.name:c for c in defined_columns}
  existing_col_names = set(existing_cols_by_name.keys())
  defined_col_names = set(defined_cols_by_name.keys())
  new_cols = defined_col_names - existing_col_names
  delete_cols = existing_col_names - defined_col_names
  rename_cols = {}
  for cn in list(new_cols):
    sc = defined_cols_by_name[cn]
    field = defined_fields_by_column_name[cn]
    if hasattr(field, 'akas'):
      for aka in field.akas:
        if aka in delete_cols:
          ec = existing_cols_by_name[aka]
          if can_convert(sc.data_type, ec.data_type):
            rename_cols[ec.name] = sc.name
            new_cols.discard(cn)
            delete_cols.discard(aka)
  
  alter_statements = []
  renames_new_to_old = {v:k for k,v in rename_cols.items()}
  not_new_columns = defined_col_names - new_cols
  
  # look for column metadata changes
  for col_name in not_new_columns:
    existing_col = existing_cols_by_name[renames_new_to_old.get(col_name, col_name)]
    defined_col = defined_cols_by_name[col_name]
    field = defined_fields_by_column_name[defined_col.name]
    if column_def_changed(db, existing_col, defined_col):
      len_alter_statements = len(alter_statements)
      if existing_col.null and not defined_col.null:
        alter_statements += add_not_null(db, migrator, ntn, field, defined_col.name)
      if not existing_col.null and defined_col.null:
        op = migrator.drop_not_null(ntn, defined_col.name, generate=True)
        alter_statements.append(qc.parse_node(op))
      if existing_col.data_type != defined_col.data_type and can_convert(existing_col.data_type, defined_col.data_type):
        stmts = change_column_type(db, migrator, ntn, defined_col.name, field)
        alter_statements += stmts
      if existing_col.data_type==defined_col.data_type and (existing_col.max_length!=defined_col.max_length or (defined_col.precision is not None and existing_col.precision!=defined_col.precision) or (defined_col.scale is not None and existing_col.scale!=defined_col.scale)):
        stmts = change_column_type(db, migrator, ntn, defined_col.name, field)
        alter_statements += stmts
      if DIFF_DEFAULTS:
        if normalize_default(existing_col.default) is not None and normalize_default(defined_col.default) is None:
          alter_statements += drop_default(db, migrator, ntn, defined_col.name, field)
        elif normalize_default(existing_col.default) != normalize_default(defined_col.default):
          alter_statements += set_default(db, migrator, ntn, defined_col.name, field)
      if not (len_alter_statements < len(alter_statements)):
        if existing_col.data_type == u'array':
          # type reporting for arrays is broken in peewee
          # it returns the underlying type of the array, not array
          # ignore array columns for now (HACK)
          pass
        else:
          raise Exception("In table %s I don't know how to change %s into %s" % (repr(ntn), existing_col, defined_col))
  
  # look for fk changes
  existing_fks_by_column = {fk.column:fk for fk in existing_fks}
  for col_name in not_new_columns:
    existing_column_name = renames_new_to_old.get(col_name, col_name)
    defined_field = defined_fields_by_column_name[col_name]
    existing_fk = existing_fks_by_column.get(existing_column_name)
    if isinstance(defined_field, pw.ForeignKeyField) and not existing_fk and not (hasattr(defined_field,'fake') and defined_field.fake):
      op = qc._create_foreign_key(defined_field.model_class, defined_field)
      alter_statements.append(qc.parse_node(op))
    if not isinstance(defined_field, pw.ForeignKeyField) and existing_fk:
      alter_statements += drop_foreign_key(db, migrator, ntn, existing_fk.name)
        

  return new_cols, delete_cols, rename_cols, alter_statements

def drop_foreign_key(db, migrator, table_name, fk_name):
  drop_stmt = 'drop foreign key' if is_mysql(db) else 'DROP CONSTRAINT'
  op = pw.Clause(pw.SQL('ALTER TABLE'), pw.Entity(table_name), pw.SQL(drop_stmt), pw.Entity(fk_name))
  return normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, op)

def drop_default(db, migrator, table_name, column_name, field):
  op = pw.Clause(pw.SQL('ALTER TABLE'), pw.Entity(table_name), pw.SQL('ALTER COLUMN'), pw.Entity(column_name), pw.SQL('DROP DEFAULT'))
  return normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, op)

def set_default(db, migrator, table_name, column_name, field):
  default = field.default
  if callable(default): default = default()
  param = pw.Param(field.db_value(default))
  op = pw.Clause(pw.SQL('ALTER TABLE'), pw.Entity(table_name), pw.SQL('ALTER COLUMN'), pw.Entity(column_name), pw.SQL('SET DEFAULT'), param)
  return normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, op)

def alter_add_column(db, migrator, ntn, column_name, field):
  qc = db.compiler()
  operation = migrator.alter_add_column(ntn, column_name, field, generate=True)
  to_run = [qc.parse_node(operation)]
  if is_mysql(db) and isinstance(field, pw.ForeignKeyField):
    op = qc._create_foreign_key(field.model_class, field)
    to_run.append(qc.parse_node(op))
  return to_run

def calc_changes(db, ignore_tables=None):
  migrator = None # expose eventually?
  if migrator is None:
    migrator = auto_detect_migrator(db)
    
  existing_tables = [unicode(t) for t in db.get_tables()]
  existing_indexes = {table:get_indexes_by_table(db, table) for table in existing_tables}
  existing_columns_by_table = get_columns_by_table(db)
  foreign_keys_by_table = get_foreign_keys_by_table(db)

  table_names_to_models = {cls._meta.db_table:cls for cls in all_models.keys()}

  qc = db.compiler()
  to_run = []

  table_adds, add_fks, table_deletes, table_renames = calc_table_changes(existing_tables, ignore_tables=ignore_tables)
  table_renamed_from = {v:k for k,v in table_renames.items()}
  to_run += [qc.create_table(table_names_to_models[tbl]) for tbl in table_adds]
  for field in add_fks:
    if hasattr(field, '__pwdbev__not_deferred') and field.__pwdbev__not_deferred:
      field.deferred = False
    op = qc._create_foreign_key(field.model_class, field)
    to_run.append(qc.parse_node(op))
  for k,v in table_renames.items():
    ops = migrator.rename_table(k,v, generate=True)
    if not hasattr(ops, '__iter__'): ops = [ops] # sometimes pw return arrays, sometimes not
    to_run += [qc.parse_node(op) for op in ops]


  rename_cols_by_table = {}
  deleted_cols_by_table = {}
  for etn, ecols in existing_columns_by_table.items():
    if etn in table_deletes: continue
    ntn = table_renames.get(etn, etn)
    model = table_names_to_models.get(ntn)
    if not model: continue
    defined_fields = model._meta.sorted_fields
    defined_column_name_to_field = {unicode(f.db_column):f for f in defined_fields}
    adds, deletes, renames, alter_statements = calc_column_changes(db, migrator, etn, ntn, ecols, defined_fields, foreign_keys_by_table[etn])
    for column_name in adds:
      field = defined_column_name_to_field[column_name]
      to_run += alter_add_column(db, migrator, ntn, column_name, field)
      if not field.null:
        # alter_add_column strips null constraints
        # add them back after setting any defaults
        if field.default is not None:
          operation = migrator.apply_default(ntn, column_name, field, generate=True)
          to_run.append(qc.parse_node(operation))
        else:
          to_run.append(('-- adding a not null column without a default will fail if the table is not empty',[]))
        to_run += add_not_null(db, migrator, ntn, field, column_name)
          
    for column_name in deletes:
      to_run += drop_column(db, migrator, ntn, column_name)
    for ocn, ncn in renames.items():
      field = defined_column_name_to_field[ncn]
      to_run += rename_column(db, migrator, ntn, ocn, ncn, field)
    to_run += alter_statements
    rename_cols_by_table[ntn] = renames
    deleted_cols_by_table[ntn] = deletes
  
  for ntn, model in table_names_to_models.items():
    etn = table_renamed_from.get(ntn, ntn)
    deletes = deleted_cols_by_table.get(ntn,set())
    existing_indexes_for_table = [i for i in existing_indexes.get(etn, []) if not any([(c in deletes) for c in i.columns])]
    to_run += calc_index_changes(db, migrator, existing_indexes_for_table, model, rename_cols_by_table.get(ntn, {}))
  
  '''
  to_run += calc_perms_changes($schema_tables, noop) unless $check_perms_for.empty?
  '''

  
  
  to_run += [qc.parse_node(pw.Clause(pw.SQL('DROP TABLE'), pw.Entity(tbl))) for tbl in table_deletes]
  return to_run

def rename_column(db, migrator, ntn, ocn, ncn, field):
  qc = db.compiler()
  if is_mysql(db):
    junk = pw.Clause(
      pw.SQL('ALTER TABLE'), pw.Entity(ntn), pw.SQL('CHANGE'), pw.Entity(ocn), qc.field_definition(field)
    )
  else:
    junk = migrator.rename_column(ntn, ocn, ncn, generate=True)
  return normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, junk)

def normalize_op_to_clause(db, migrator, op):
  if isinstance(op, pw.Clause): return op
  playhouse.migrate
  kwargs = op.kwargs.copy()
  kwargs['generate'] = True
  ret = getattr(migrator, op.method)(*op.args, **kwargs)
  return ret

def normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, junk):
  # sometimes a clause, sometimes an operation, sometimes a list mixed with clauses and operations
  # turn it into a list of (sql,params) tuples
  if not hasattr(junk, '__iter__'):
    junk = [junk]
  junk = [normalize_op_to_clause(db, migrator, o) for o in junk]
  qc = db.compiler()
  junk = [qc.parse_node(clause) for clause in junk]
  return junk

def drop_column(db, migrator, ntn, column_name):
  return normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, migrator.drop_column(ntn, column_name, generate=True, cascade=False))
  
def change_column_type(db, migrator, table_name, column_name, field):
  qc = db.compiler()
  column_type = qc.get_column_type(field.get_db_field())
  if is_postgres(db):
    op = pw.Clause(pw.SQL('ALTER TABLE'), pw.Entity(table_name), pw.SQL('ALTER'), field.as_entity(), pw.SQL('TYPE'), field.__ddl_column__(column_type))
  elif is_mysql(db):
    op = pw.Clause(*[pw.SQL('ALTER TABLE'), pw.Entity(table_name), pw.SQL('MODIFY')] + field.__ddl__(column_type))
  else:
    raise Exception('how do i change a column type for %s?' % db)
  return normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, op)
  
def add_not_null(db, migrator, table, field, column_name):
  qc = db.compiler()
  cmds = []
  if field.default is not None:
    # if default is a function, turn it into a value
    # this won't work on columns requiring uniquiness, like UUIDs
    # as all columns will share the same called value
    default = field.default() if hasattr(field.default, '__call__') else field.default
    op = pw.Clause(pw.SQL('UPDATE'), pw.Entity(table), pw.SQL('SET'), field.as_entity(), pw.SQL('='), default, pw.SQL('WHERE'), field.as_entity(), pw.SQL('IS NULL'))
    cmds.append(qc.parse_node(op))
  if is_postgres(db) or is_sqlite(db):
    junk = migrator.add_not_null(table, column_name, generate=True)
    cmds += normalize_whatever_junk_peewee_migrations_gives_you(db, migrator, junk)
    return cmds
  elif is_mysql(db):
    op = pw.Clause(pw.SQL('ALTER TABLE'), pw.Entity(table), pw.SQL('MODIFY'), qc.field_definition(field))
    cmds.append(qc.parse_node(op))
    return cmds
  raise Exception('how do i add a not null for %s?' % db)

def indexes_are_same(i1, i2):
  return unicode(i1.table)==unicode(i2.table) and i1.columns==i2.columns and i1.unique==i2.unique

def normalize_indexes(indexes):
  return [(unicode(idx.table), tuple(unicode(c) for c in idx.columns), idx.unique) for idx in indexes]

  
def calc_index_changes(db, migrator, existing_indexes, model, renamed_cols):
  qc = db.compiler()  
  to_run = []
  fields = list(model._meta.sorted_fields)
  fields_by_column_name = {f.db_column:f for f in fields}
  pk_cols = set([unicode(f.db_column) for f in fields if f.primary_key])
  existing_indexes = [i for i in existing_indexes if not all([(unicode(c) in pk_cols) for c in i.columns])]
  normalized_existing_indexes = normalize_indexes(existing_indexes)
  existing_indexes_by_normalized_existing_indexes = dict(zip(normalized_existing_indexes, existing_indexes))
  normalized_existing_indexes = set(normalized_existing_indexes)
  defined_indexes = [pw.IndexMetadata('', '', [f.db_column], f.unique, model._meta.db_table) for f in model._fields_to_index()]
  for fields, unique in model._meta.indexes:
    try:
      columns = [model._meta.fields[fname].db_column for fname in fields]
    except KeyError as e:
      raise Exception("Index %s on %s references field %s in a multi-column index, but that field doesn't exist. (Be sure to use the field name, not the db_column name, when specifying a multi-column index.)" % ((fields, unique), model.__name__, repr(e.message)))
    defined_indexes.append(pw.IndexMetadata('', '', columns, unique, model._meta.db_table))
  normalized_defined_indexes = set(normalize_indexes(defined_indexes))
  to_add = normalized_defined_indexes - normalized_existing_indexes
  to_del = normalized_existing_indexes - normalized_defined_indexes
  for index in to_del:
    index = existing_indexes_by_normalized_existing_indexes[index]
    op = migrator.drop_index(model._meta.db_table, index.name, generate=True)
    to_run.append(qc.parse_node(op))
  for index in to_add:
    to_run.append(qc.create_index(model, [fields_by_column_name[col] for col in index[1]], index[2]))
  return to_run
  
def evolve(db, interactive=True, ignore_tables=None):
  if interactive:
    print((colorama.Style.BRIGHT + colorama.Fore.RED + 'Making updates to database: {}'.format(db.database) + colorama.Style.RESET_ALL))
  to_run = calc_changes(db, ignore_tables=ignore_tables)
  if not to_run:
    if interactive:
      print('Nothing to do... Your database is up to date!')
    return
  
  commit = True
  if interactive:
    commit = _confirm(db, to_run)

  _execute(db, to_run, interactive=interactive, commit=commit)


def _execute(db, to_run, interactive=True, commit=True):
  if interactive: print()
  try:
    with db.atomic() as txn:
      for sql, params in to_run:
        if interactive or DEBUG: print_sql(' %s; %s' % (sql, params or ''))
        if sql.strip().startswith('--'): continue
        db.execute_sql(sql, params)
      if interactive:
        print()
        print(
          (colorama.Style.BRIGHT + 'SUCCESS!' + colorama.Style.RESET_ALL) if commit else 'TEST PASSED - ROLLING BACK', 
          colorama.Style.DIM + '-', 
          'https://github.com/keredson/peewee-db-evolve' + colorama.Style.RESET_ALL
        )
        print()
      if not commit:
        txn.rollback()
  except Exception as e:
    print()
    print('------------------------------------------')
    print(colorama.Style.BRIGHT + colorama.Fore.RED + ' SQL EXCEPTION - ROLLING BACK ALL CHANGES' + colorama.Style.RESET_ALL)
    print('------------------------------------------')
    print()
    raise e

COLORED_WORDS = None

def init_COLORED_WORDS():
  global COLORED_WORDS
  COLORED_WORDS = [
    (colorama.Fore.GREEN, ['CREATE', 'ADD']),
    (colorama.Fore.YELLOW, ['ALTER', 'SET', 'RENAME']),
    (colorama.Fore.RED, ['DROP']),
    (colorama.Style.BRIGHT + colorama.Fore.BLUE, ['INTEGER','VARCHAR','TIMESTAMP','TEXT','SERIAL']),
    (colorama.Style.BRIGHT, ['BEGIN','COMMIT']),
    (colorama.Fore.CYAN, ['FOREIGN KEY', 'REFERENCES', 'UNIQUE']),
    (colorama.Style.BRIGHT + colorama.Fore.CYAN, ['PRIMARY KEY']),
    (colorama.Style.BRIGHT + colorama.Fore.MAGENTA, ['NOT NULL','NULL']),
    (colorama.Style.DIM, [' ON ', '(', ')', 'INDEX', 'TABLE', 'COLUMN', 'CONSTRAINT' ,' TO ',';']),
  ]

def print_sql(sql):
  if COLORED_WORDS is None: init_COLORED_WORDS()
  for color, patterns in COLORED_WORDS:
    for pattern in patterns:
      sql = sql.replace(pattern, color + pattern + colorama.Style.RESET_ALL)
  print(sql)
  

def _confirm(db, to_run):
  print()
  print("Your database needs the following %s:" % ('changes' if len(to_run)>1 else 'change'))
  print()
  if is_postgres(db): print_sql('  BEGIN TRANSACTION;\n')
  for sql, params in to_run:
    print_sql('  %s; %s' % (sql, params or ''))
  if is_postgres(db): print_sql('\n  COMMIT;')
  print()
  while True:
    print('Do you want to run %s? (%s)' % (('these commands' if len(to_run)>1 else 'this command'), ('type yes, no or test' if is_postgres(db) else 'yes or no')), end=' ')
    response = raw_input().strip().lower()
    if response=='yes' or (is_postgres(db) and response=='test'):
      break
    if response=='no':
      sys.exit(1)
  print('Running in', end=' ')
  for i in range(3):
    print('%i...' % (3-i), end=' ')
    sys.stdout.flush()
    time.sleep(1)
  print()
  return response=='yes'
  



all_models = {}
ignore_tables = set()

def register(model):
  if hasattr(model._meta, 'evolve') and not model._meta.evolve:
    ignore_tables.add(model._meta.db_table)
  else:
    all_models[model] = []

def unregister(model):
  del all_models[model]

def clear():
  all_models.clear()
  ignore_tables.clear()

def _add_model_hook():
  init = pw.BaseModel.__init__
  def _init(*args, **kwargs):
    cls = args[0]
    fields = args[3]
    if '__module__' in fields:
      del fields['__module__']
    register(cls)
    init(*args, **kwargs)
  pw.BaseModel.__init__ = _init

def _add_field_hook():
  init = pw.Field.__init__
  def _init(*args, **kwargs):
    self = args[0]
    if 'aka' in kwargs:
      akas = kwargs['aka']
      if hasattr(akas, 'lower'):
        akas = [akas]
      self.akas = akas
      del kwargs['aka']
    init(*args, **kwargs)
  pw.Field.__init__ = _init

def _add_fake_fk_field_hook():
  init = pw.ForeignKeyField.__init__
  def _init(*args, **kwargs):
    self = args[0]
    if 'fake' in kwargs:
      self.fake = kwargs['fake']
      del kwargs['fake']
    init(*args, **kwargs)
  pw.ForeignKeyField.__init__ = _init

def add_evolve():
  pw.Database.evolve = evolve

if 'pw' in globals():
  _add_model_hook()
  _add_field_hook()
  _add_fake_fk_field_hook()
  add_evolve()


__all__ = ['evolve']

