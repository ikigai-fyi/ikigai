"""add settings

Revision ID: f277fece4aed
Revises: 10d97bb9c086
Create Date: 2023-11-22 12:12:44.842351

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f277fece4aed"
down_revision = "10d97bb9c086"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "settings",
        sa.Column("refresh_period_in_hours", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_settings")),
    )
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.add_column(sa.Column("settings_id", sa.Integer(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_athlete_settings_id"),
            ["settings_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_athlete_settings_id_settings"),
            "settings",
            ["settings_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_athlete_settings_id_settings"),
            type_="foreignkey",
        )
        batch_op.drop_index(batch_op.f("ix_athlete_settings_id"))
        batch_op.drop_column("settings_id")

    op.drop_table("settings")
