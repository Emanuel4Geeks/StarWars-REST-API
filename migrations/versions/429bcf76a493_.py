"""empty message

Revision ID: 429bcf76a493
Revises: 0da256076824
Create Date: 2023-03-11 02:11:48.066768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '429bcf76a493'
down_revision = '0da256076824'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planeta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('diametro', sa.Integer(), nullable=False),
    sa.Column('clima', sa.String(length=100), nullable=False),
    sa.Column('terreno', sa.String(length=100), nullable=False),
    sa.Column('gravedad', sa.String(length=100), nullable=False),
    sa.Column('poblacion', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personaje',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=250), nullable=False),
    sa.Column('altura', sa.Integer(), nullable=False),
    sa.Column('peso', sa.Integer(), nullable=False),
    sa.Column('fecha_nacimiento', sa.String(), nullable=False),
    sa.Column('genero', sa.String(length=50), nullable=False),
    sa.Column('planeta_origen_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planeta_origen_id'], ['planeta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favoritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('personaje_id', sa.Integer(), nullable=True),
    sa.Column('planeta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personaje_id'], ['personaje.id'], ),
    sa.ForeignKeyConstraint(['planeta_id'], ['planeta.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_registro', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('nombre', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('apellido', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('apellido')
        batch_op.drop_column('nombre')
        batch_op.drop_column('fecha_registro')

    op.drop_table('favoritos')
    op.drop_table('personaje')
    op.drop_table('planeta')
    # ### end Alembic commands ###