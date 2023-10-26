import psycopg2

connection = psycopg2.connect(
    user="postgres",
    password="Diyarbek05",
    host="localhost",
    port="5432",
    database="antiscam",
)

connection.autocommit = True

cursor = connection.cursor()

def add_sites(url):
    cursor.execute(
        "INSERT INTO sites (site, category, correct) VALUES (%s, %s, %s)",
        (url, "scam", True)
    )


with open("domain-list.txt", "r") as file:
    for line in file:
        line = line.strip("\n")
        add_sites(line)

with open("feed.txt", "r") as file:
    for line in file:
        line = line.strip("\n")
        add_sites(line)

with open("links.txt", "r") as file:
    for line in file:
        line = line.strip("\n")
        add_sites(line)

with open("list.txt", "r") as file:
    for line in file:
        line = line.strip("\n")
        add_sites(line)

with open("feed5.txt", "r") as file:
    for line in file:
        line = line.strip("\n")
        add_sites(line)