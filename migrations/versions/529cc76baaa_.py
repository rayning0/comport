"""empty message

Revision ID: 529cc76baaa
Revises: 1d31622bbed
Create Date: 2015-09-21 15:30:17.545617

"""

# revision identifiers, used by Alembic.
revision = '529cc76baaa'
down_revision = '1d31622bbed'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('departments', 'what_this_is')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departments', sa.Column('what_this_is', sa.TEXT(), autoincrement=False, nullable=True))
    ### end Alembic commands ###