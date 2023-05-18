from database import client, MONGO_DB_NAME

from schemas.user import *
from bson import ObjectId

collection_name = "user_collection"
collection = client[MONGO_DB_NAME][collection_name]

async def get_users():
    results = []
    async for document in collection.find({}):
        document["_id"] = str(document["_id"])
        results.append(document)
    return results


async def get_user(document_id):
    result = await collection.find_one({"_id": ObjectId(document_id)})
    if not result:
        return "User not found"
    result["_id"] = str(result["_id"])
    return result


async def get_user_by_name(document_name):
    result = await collection.find_one({"username": document_name})
    if not result:
        return "User not found"
    result["_id"] = str(result["_id"])
    return result


async def post_user(document):
    result = await collection.insert_one(document)
    return str(result.inserted_id)


async def update_user(document_id, document):

    user_doc = await get_user(document_id)
    if not user_doc:
        return "User not found"
    user_doc["_id"] = str(user_doc["_id"])

    update_data = {k: v for k, v in document.items() if k != '_id'}
    updated_user_doc = {**user_doc, **update_data}
    updated_user_doc.pop("_id", None)
    result = await collection.update_one(
        {"_id": ObjectId(user_doc["_id"])}, {"$set": updated_user_doc}
    )

    if result.modified_count == 1:
        updated_user_doc = await get_user(user_doc["_id"])
        updated_user_doc["_id"] = str(updated_user_doc["_id"])
        return updated_user_doc

    return "error"


async def delete_user(document_id):
    result = await collection.delete_one({"_id": ObjectId(document_id)})

    if result.deleted_count == 1:
        return {"message": "User deleted successfully."}

    return {"message": "User not found."}