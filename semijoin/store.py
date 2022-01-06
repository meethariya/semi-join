import mysql.connector as MYSQL

def connector():
    conn = MYSQL.connect(host='localhost',password='root',user='root')
    cur = conn.cursor()
    return conn,cur

def get_info():
    info = []
    conn, cur = connector()
    cur.execute('SHOW DATABASES LIKE "ads4_%";')
    dbs = cur.fetchall()
    for db in dbs:
        db = db[0]
        cur.execute(f'use {db};')
        cur.execute(f'show tables;')
        table = cur.fetchone()
        table = table[0]
        cur.execute(f'''SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA='{db}';''')
        cols=cur.fetchall()
        cols = [j[0] for j in cols]
        cur.execute(f"select * from {table};")
        rows = cur.fetchall()
        obj = {
            'db':db,
            'name':table,
            'columns':cols,
            'rows':rows,
        }
        info.append(obj)
    return info

# steps
# table2 ids to product table
# join at prodcut
# send results back to table2
# join and display result

def joins(table,db):
    conn, cur = connector()
    cur.execute(f"SELECT id from {db}.{table};")
    ids = cur.fetchall()
    ids = [j[0] for j in ids]
    format_strings = ','.join(['%s'] * len(ids))
    data_cols = ["id", "name", "price", f"{table + '_id'}"]
    cur.execute(f"SELECT id, name, price, {table + '_id'} from ads4_1.product where id in ({format_strings});",ids)
    data = cur.fetchall()
    cur.execute(f'''SELECT p.id, p.name, p.price, {'p.' + table + '_id'}, t2.name
                    from ads4_1.product as p
                    inner join {db}.{table} as t2
                    where {'p.' + table + '_id'} = t2.id;
            ''')
    results = cur.fetchall()
    results_col = ["p.id", "p.name", "p.price", f"{'p.' + table + '_id'}", f"{table+'_name'}"]
    dictionary = {
        'database':db,
        'table':table,
        'ids': ids,
        'data_cols':data_cols,
        'data': data,
        'results_cols':results_col,
        'results': results
    } 
    return dictionary