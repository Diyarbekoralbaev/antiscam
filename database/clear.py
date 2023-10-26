import pymongo

# MongoDB-ga ulanish
client = pymongo.MongoClient("mongodb+srv://Diyarbek:Diyarbek05@diyarbek.lqwy3of.mongodb.net/?retryWrites=true&w=majority")

# Ma'lumotlar bazasi va collection tanlash
db = client.antiscam
collection = db.sites

# Tozalash shartlari
query = {}  # Barcha dokumentlarni tanlash

# Ma'lumotlarni tozalash
result = collection.delete_many(query)

print(f"{result.deleted_count} ta dokument o'chirildi.")
