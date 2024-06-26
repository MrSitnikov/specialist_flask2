"""upgrade rating

Revision ID: 3c1434c86905
Revises: f72bcb5a1c8c
Create Date: 2024-06-05 16:35:03.992610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c1434c86905'
down_revision = 'f72bcb5a1c8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), server_default='1', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
