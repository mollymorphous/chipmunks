# SPDX-FileCopyrightText: © 2025 Molly Rose
# SPDX-License-Identifier: AGPL-3.0-or-later

from chipmunks_api import app as chipmunks_api
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route


async def hello(request):
    return PlainTextResponse("Hello, chipmunks!")


app = Starlette(
    debug=True,
    routes=[
        Route("/", hello),
        Mount("/api/v0", chipmunks_api),
    ],
)
