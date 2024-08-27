import psycopg2 as pg

# Connect to the Database
conn = pg.connect("host=localhost dbname=postgres user=postgres password='Jelibi20'")
cur = conn.cursor()

# Create a Table
def createTable():
    createCMD = """
                CREATE TABLE public."factorymachines"(
                machine_id character varying,
                sentDate timestamp without time zone,
                temperature double precision,
                pressure double precision,
                status character varying,
                humidity integer,
                sequence character varying PRIMARY KEY
                )
                """
    cur.execute(createCMD)

def insertRow():
    insertCMD = """ INSERT INTO public."factorymachines" VALUES(%s,%s,%s,%s,%s,%s,%s) """
    values = (100, "2022-09-20", 22.1, 9.3, "ON", 88, "20240720")
    cur.execute(insertCMD, values)

def bulkInsert():
    with open('data/machines.csv', 'r') as content:
        next(content)
        cur.copy_from(content, "factorymachines",  sep=',')

# createTable() # Only run this line once
# insertRow()
bulkInsert()

conn.commit()
