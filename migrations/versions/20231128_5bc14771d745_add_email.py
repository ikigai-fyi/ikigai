"""add email

Revision ID: 5bc14771d745
Revises: 9cab90d665e9
Create Date: 2023-11-28 11:24:38.945990

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5bc14771d745"
down_revision = "9cab90d665e9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.drop_column("email")

    # ### end Alembic commands ###
