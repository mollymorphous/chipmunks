<!-- SPDX-FileCopyrightText: © 2025 Molly Rose -->
<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# Chipmunks API

API backend of 🐿️ Chipmunks, a cute little inventory manager for groceries and
household supplies

Written in [:snake: Python 3](https://www.python.org/) and powered by
[:zap: FastAPI](https://fastapi.tiangolo.com/) and
[:alembic: SQLAlchemy](https://www.sqlalchemy.org/). It's designed to run
on modest hardware and uses [:feather: SQLite](https://www.sqlite.org/) and a
`data` directory for its database and storage, but can be easily adapted to
use another SQL database or storage backend.

Typically, this is served by the all-in-one server in the `chipmunks` package,
but it exports an ASGI application at `chipmunks_api:app` which you can serve
with your choice of ASGI servers. If installed with the
[:unicorn: Granian](https://github.com/emmett-framework/granian)
extra, `chipmunks-api[granian]`, it can serve itself from the command line.

# License

Copyright © 2025 Molly Rose.

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU Affero General Public License][] as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
[GNU Affero General Public License][] for more details.

You should have received a copy of the [GNU Affero General Public License][]
along with this program. If not, see <https://www.gnu.org/licenses/>.

[GNU Affero General Public License]: COPYING.md
