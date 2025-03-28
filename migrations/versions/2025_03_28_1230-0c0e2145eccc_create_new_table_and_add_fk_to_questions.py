"""create new table and add fk to questions

Revision ID: 0c0e2145eccc
Revises: 85d119cb56b5
Create Date: 2025-03-28 12:30:20.442127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = '0c0e2145eccc'
down_revision = '85d119cb56b5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=40),
               existing_nullable=False)

    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categories', ['category_id'], ['id'])



def downgrade():
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=40),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

