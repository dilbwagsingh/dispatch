"""Adds a data model for incident feedback

Revision ID: 841d00729e31
Revises: 1a4a20476cc4
Create Date: 2020-10-19 11:47:09.835643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "841d00729e31"
down_revision = "1a4a20476cc4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.String(), nullable=True),
        sa.Column("feedback", sa.String(), nullable=True),
        sa.Column("incident_id", sa.Integer(), nullable=True),
        sa.Column("participant_id", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["incident_id"],
            ["incident.id"],
        ),
        sa.ForeignKeyConstraint(
            ["participant_id"],
            ["participant.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("feedback")
    # ### end Alembic commands ###