"""longer-picture-url

Revision ID: 840607e9ca93
Revises: 87dc9c13a451
Create Date: 2023-06-11 17:41:15.228540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "840607e9ca93"
down_revision = "87dc9c13a451"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.alter_column(
            "picture_url",
            existing_type=sa.VARCHAR(length=128),
            type_=sa.String(length=256),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("athlete", schema=None) as batch_op:
        batch_op.alter_column(
            "picture_url",
            existing_type=sa.String(length=256),
            type_=sa.VARCHAR(length=128),
            existing_nullable=True,
        )

    # ### end Alembic commands ###