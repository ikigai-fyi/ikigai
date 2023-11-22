"""Add current_activity_refreshed_at column

Revision ID: 10d97bb9c086
Revises: 8c548e32cfbd
Create Date: 2023-11-17 17:16:00.148582

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "10d97bb9c086"
down_revision = "8c548e32cfbd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("current_activity_refreshed_at", sa.DateTime(), nullable=True),
        )

    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.execute(
            "UPDATE athlete SET current_activity_refreshed_at = created_at;",
        )
        batch_op.alter_column(
            "current_activity_refreshed_at",
            existing_type=sa.DateTime(),
            type_=sa.DateTime(),
            existing_nullable=True,
            nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.drop_column("current_activity_refreshed_at")

    # ### end Alembic commands ###
