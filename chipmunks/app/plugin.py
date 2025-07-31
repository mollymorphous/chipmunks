# SPDX-FileCopyrightText: © 2025 Molly Rose <molly@mollymorphous.dev>
# SPDX-License-Identifier: AGPL-3.0-or-later


from litestar.config.app import AppConfig
from litestar.plugins import InitPlugin


class ChipmunksPlugin(InitPlugin):
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        from . import config

        app_config.openapi_config = config.openapi
        return app_config
