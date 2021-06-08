"""Adds instance parameters.

Revision ID: 9f927a8e4679
Revises: 995a59897e01
Create Date: 2020-09-25 12:48:21.180604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9f927a8e4679"
down_revision = "995a59897e01"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("workflow_instance", sa.Column("parameters", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("workflow_instance", "parameters")
    # ### end Alembic commands ###