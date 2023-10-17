"""Initial migration.

Revision ID: 819cbf6e030b
Revises:
Create Date: 2021-08-16 16:53:05.484024

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "819cbf6e030b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS shared")


def downgrade() -> None:
    op.execute("DROP SCHEMA shared")
