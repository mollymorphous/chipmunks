# SPDX-FileCopyrightText: © 2025 Molly Rose
# SPDX-License-Identifier: AGPL-3.0-or-later

from granian import Granian
from granian.constants import Interfaces


def run():
    Granian(
        "chipmunks",
        interface=Interfaces.ASGI,
        log_access=True,
    ).serve()
