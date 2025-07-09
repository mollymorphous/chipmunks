# SPDX-FileCopyrightText: © 2025 Molly Rose
# SPDX-License-Identifier: AGPL-3.0-or-later

import sys


def run():
    try:
        from granian import Granian
        from granian.constants import Interfaces
    except ImportError:
        print("Install chipmunks_api[granian] to run the server")
        sys.exit(1)

    Granian(
        "chipmunks_api",
        interface=Interfaces.ASGI,
        log_access=True,
    ).serve()
