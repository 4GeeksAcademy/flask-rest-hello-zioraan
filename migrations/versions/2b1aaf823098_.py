"""empty message

Revision ID: 2b1aaf823098
Revises: a5cffa318ac2
Create Date: 2024-08-07 23:11:55.705918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b1aaf823098'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=40), nullable=True),
    sa.Column('climate', sa.String(length=40), nullable=True),
    sa.Column('terrain', sa.String(length=40), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('height', sa.String(length=20), nullable=True),
    sa.Column('skin_color', sa.String(length=20), nullable=True),
    sa.Column('birth_year', sa.String(length=20), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('homeworld', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homeworld'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_list', sa.Integer(), nullable=True),
    sa.Column('planet_list', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_list'], ['person.id'], ),
    sa.ForeignKeyConstraint(['planet_list'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_list', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ['favorites_list'])
        batch_op.create_foreign_key(None, 'favorites', ['favorites_list'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('favorites_list')

    op.drop_table('favorites')
    op.drop_table('person')
    op.drop_table('planet')
    # ### end Alembic commands ###
