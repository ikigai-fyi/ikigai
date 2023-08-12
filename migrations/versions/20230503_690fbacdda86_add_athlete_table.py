"""Add athlete table

Revision ID: 690fbacdda86
Revises: 
Create Date: 2023-05-03 16:03:14.433485

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "690fbacdda86"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "athlete",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("uuid", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_athlete")),
    )
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_athlete_uuid"), ["uuid"], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_athlete_uuid"))

    op.drop_table("athlete")
    # ### end Alembic commands ###
