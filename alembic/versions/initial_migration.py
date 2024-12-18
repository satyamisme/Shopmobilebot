"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2023-09-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('telegram_id', sa.Integer(), unique=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('permissions', sa.String()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create user_roles association table
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id')),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # Create shops table
    op.create_table(
        'shops',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('imei', sa.String(), unique=True, nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('ram', sa.String()),
        sa.Column('storage', sa.String()),
        sa.Column('network', sa.String()),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('condition', sa.String()),
        sa.Column('status', sa.String(), default='in_stock'),
        sa.Column('shop_id', sa.Integer(), sa.ForeignKey('shops.id')),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('products')
    op.drop_table('shops')
    op.drop_table('user_roles')
    op.drop_table('roles')
    op.drop_table('users')