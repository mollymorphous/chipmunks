# SPDX-FileCopyrightText: © 2025 Molly Rose <molly@mollymorphous.dev>
# SPDX-License-Identifier: AGPL-3.0-or-later

from litestar.openapi import OpenAPIConfig

from . import __version__

openapi = OpenAPIConfig(
    title="Chimunks",
    version=__version__,
    description="Cute little inventory manager for groceries and household supplies",
)
