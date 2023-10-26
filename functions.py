import psycopg2
import requests
from pydantic import BaseModel
from scam import bitdefender_check
import re

connection = psycopg2.connect(
    user="postgres",
    password="Diyarbek05",
    host="localhost",
    port="5432",
    database="antiscam",
)

connection.autocommit = True

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        id SERIAL PRIMARY KEY,
        site VARCHAR(800),
        category VARCHAR(255),
        correct BOOLEAN DEFAULT false
    )""")


class Site(BaseModel):
    site: str
    category: str

def validate_https_url(url):
    regex = re.compile(
        r'^https://'  # https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

async def get_all_sites():
    cursor.execute("SELECT * FROM sites")
    return cursor.fetchall()

async def is_have(url):
    try:
        requests.get(url)
        return True
    except requests.exceptions.ConnectionError:
        return False

async def add_sites(site: Site):
    cursor.execute(
        "INSERT INTO sites (site, category) VALUES (%s, %s)",
        (site.site, site.category)
    )
    return cursor.execute("SELECT id FROM sites WHERE site = %s", (site.site,))


async def verify_site(id: int):
    cursor.execute(
        "UPDATE sites SET correct = true WHERE id = %s",
        (id,)
    )


async def get_scam_sites():
    cursor.execute("SELECT * FROM sites WHERE correct = true")
    return cursor.fetchall()


async def get_unverified_sites():
    cursor.execute("SELECT * FROM sites WHERE correct = false")
    return cursor.fetchall()


async def delete_site(id: int):
    cursor.execute(
        "DELETE FROM sites WHERE id = %s",
        (id,)
    )


async def check_url(url: str):
    cursor.execute("SELECT * FROM sites WHERE site = %s", (url,))
    result = cursor.fetchone()
    if result:
        return {
            "status": "danger",
            "message": "This URL is a scam. It is a phishing website."
        }
    elif await bitdefender_check(url):
        return {
               "status": "success",
               "message": ""
        }
    else:
        cursor.execute("INSERT INTO sites (site, category, correct) VALUES (%s, %s, %s)", (url, "Scam", True))
        return {
            "status": "danger",
            "message": "This URL is not safe. It is a phishing website."
        }