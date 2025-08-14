
from fastapi import FastAPI

description = """
Fastapi CRUD 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Fastapi CRUD",
    description=description,
    summary="Fastapi CRUD",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Fastapi CRUD",
        "url": "http://example.com/contact/",
        "email": "admin@mail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
