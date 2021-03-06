"""empty message

Revision ID: 2357b6b3d76
Revises: fecca96b9d
Create Date: 2015-10-27 10:26:52.074526

"""

# revision identifiers, used by Alembic.
revision = '2357b6b3d76'
down_revision = 'fecca96b9d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('citizen_complaints', sa.Column('service_type', sa.String(length=255), nullable=True))
    op.add_column('citizen_complaints', sa.Column('source', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('citizen_complaints', 'source')
    op.drop_column('citizen_complaints', 'service_type')
    ### end Alembic commands ###
