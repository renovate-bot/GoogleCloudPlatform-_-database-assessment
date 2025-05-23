# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from typing import TYPE_CHECKING

import duckdb
from rich.table import Table

if TYPE_CHECKING:
    import duckdb
    from rich.console import Console

    from dma.collector.query_managers.base import CanonicalQueryManager


def print_summary_mysql(
    console: Console,
    local_db: duckdb.DuckDBPyConnection,
    manager: CanonicalQueryManager,
) -> None:
    """Print Summary of the Migration Readiness Assessment."""
    summary_table = Table(show_edge=False, width=80)
    print_database_details(console=console, local_db=local_db, manager=manager)
    console.print(summary_table)


def print_database_details(
    console: Console,
    local_db: duckdb.DuckDBPyConnection,
    manager: CanonicalQueryManager,
) -> None:
    """Print Summary of the Migration Readiness Assessment."""
    calculated_metrics = local_db.sql(
        """
            select variable_category, variable_name, variable_value
            from collection_mysql_config
        """,
    ).fetchall()
    count_table = Table(show_edge=False, width=80)
    count_table.add_column("Variable Category", justify="right", style="green")
    count_table.add_column("Variable", justify="right", style="green")
    count_table.add_column("Value", justify="right", style="green")

    for row in calculated_metrics:
        count_table.add_row(*[str(col) for col in row])
    console.print(count_table)
