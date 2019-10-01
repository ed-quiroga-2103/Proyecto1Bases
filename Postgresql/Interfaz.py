import psycopg2

conn = psycopg2.connect(database="sk8database", user = "postgres", password = "hastael8", host = "127.0.0.1", port = "5432")

print ("Opened database successfully")

cur = conn.cursor()

cur.execute("INSERT INTO COUNTRY (IDCOUNTRY,NAME) \
      VALUES (1, 'CostaRica')");

conn.commit()
print ("Complete insertion of country");
conn.close()