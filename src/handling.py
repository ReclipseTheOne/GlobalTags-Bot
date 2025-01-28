import requests
import tags
import logs

ServerURL = "http://127.0.0.1:8000"


def handleCreateTagRequest(tag: tags.TagSchema):
    payload = tag.model_dump()
    # logs.GTLogger.debug(f"Payload being sent: {payload}")

    response = requests.post(f"{ServerURL}/tags", json=payload)

    if response.content == b'Internal Server Error':
        logs.GTLogger.error("Internal Server Error")
        return response.content
    else:
        logs.GTLogger.success(f"Created tag: {tag.name}")
        logs.GTLogger.info(response.json().__str__())

    return response.json()


def handleDeleteTagRequest(tag_name: str, key: str):
    response = requests.delete(f"{ServerURL}/tags/{tag_name}", json={'key': key})

    if response.content == b'Internal Server Error':
        logs.GTLogger.error("Internal Server Error")
        return response.content
    else:
        logs.GTLogger.success(f"Deleted tag: {tag_name}")
        logs.GTLogger.info(response.json())

    return response.json()


def fetchTag(name: str):
    response = requests.get(f"{ServerURL}/tags/{name}")

    logs.GTLogger.success(f"Fetched tag: {name}")
    logs.GTLogger.info(response.json().__str__())

    return response.json()

def fetchTags():
    response = requests.get(f"{ServerURL}/tags")

    logs.GTLogger.success(f"Fetched tags")
    logs.GTLogger.info(response.json().__str__())

    return response.json()