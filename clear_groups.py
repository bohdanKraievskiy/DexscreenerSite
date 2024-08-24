from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb+srv://histennn:PM1gR78yI4Y5WYrU@cluster0.mrtj4.mongodb.net/')
db = client['aidjango']  # Замените на имя вашей базы данных
groups_collection = db['groups']

# Удаление всех документов в коллекции
result = groups_collection.delete_many({})

print(f"Удалено {result.deleted_count} документов.")
