"""add strava scope

Revision ID: 8adcf1b4cd8e
Revises: a13c71267756
Create Date: 2023-05-05 16:55:57.603151

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8adcf1b4cd8e"
down_revision = "a13c71267756"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("strava_scope", sa.String(length=128), nullable=False),
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.drop_column("strava_scope")

    # ### end Alembic commands ###
