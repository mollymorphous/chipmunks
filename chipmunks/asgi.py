# SPDX-FileCopyrightText: © 2025 Molly Rose <molly@mollymorphous.dev>
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import TYPE_CHECKING

from litestar import get

from .app.plugin import ChipmunksPlugin

if TYPE_CHECKING:
    from litestar import Litestar


@get("/")
async def hello() -> str:
    return "Hello, chipmunks!"


def create_app() -> "Litestar":
    from litestar import Litestar

    return Litestar(route_handlers=[hello], plugins=[ChipmunksPlugin()])
