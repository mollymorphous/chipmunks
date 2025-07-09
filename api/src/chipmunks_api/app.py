# SPDX-FileCopyrightText: © 2025 Molly Rose
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import FastAPI

from . import __version__

app = FastAPI(
    name="Chipmunks",
    version=__version__,
    summary="Cute little inventory manager for groceries and household supplies",
    debug=True,
)


@app.get("/")
async def hello():
    return {"message": "Hello, chipmunks!"}
