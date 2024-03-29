"""add canceled timestamp

Revision ID: 8c548e32cfbd
Revises: 744554627216
Create Date: 2023-11-13 09:43:37.010068

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8c548e32cfbd"
down_revision = "744554627216"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("activity_fetch_job", schema=None) as batch_op:
        batch_op.add_column(sa.Column("canceled_at", sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("activity_fetch_job", schema=None) as batch_op:
        batch_op.drop_column("canceled_at")

    # ### end Alembic commands ###
