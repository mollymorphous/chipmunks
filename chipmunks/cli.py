# SPDX-FileCopyrightText: © 2025 Molly Rose <molly@mollymorphous.dev>
# SPDX-License-Identifier: AGPL-3.0-or-later

import os

from litestar.cli import litestar_group


def run_cli():
    """Run chipmunks CLI (which wraps Litestar CLI)"""
    os.environ["LITESTAR_APP"] = "chipmunks.asgi:create_app"
    os.environ["LITESTAR_APP_NAME"] = "Chipmunks"
    litestar_group()
