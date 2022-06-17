import psycopg2
from sqlalchemy import create_engine

#создаем БД на postgresql
conn_string = 'postgresql://postgres:pass@127.0.0.1/Test_Database'

db = create_engine(conn_string)
conn = db.connect()
conn1 = psycopg2.connect(
    database="Test_Database",
    user='postgres',
    password='pass',
    host='127.0.0.1',
    port='5432'
)

conn1.autocommit = True
cursor = conn1.cursor()

# drop table if it already exists
cursor.execute('drop table if exists test_final')

sql = '''CREATE TABLE test_final(id int ,
day int ,test char(20),destination char(20));'''

cursor.execute(sql)

# converting df to sql
df.to_sql('test_final', conn, if_exists='replace')

# fetching all rows
sql1 = '''select * from test_final;'''
cursor.execute(sql1)
for i in cursor.fetchall():
    print(i)

conn1.commit()
conn1.close()
