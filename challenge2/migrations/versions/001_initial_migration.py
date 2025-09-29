"""Initial migration - Create ImageFrame table

Revision ID: 001
Revises:
Create Date: 2025-09-29

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('image_frames',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('depth', sa.Float(), nullable=False),
        sa.Column('pixels', sa.JSON(), nullable=False),
        sa.Column('color_map_pixels', sa.JSON(), nullable=True),
        sa.Column('colormap_name', sa.String(50), nullable=True),
        sa.Column('colormap_applied_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('depth', name='uq_image_frames_depth')
    )
    op.create_index('idx_colormap_status', 'image_frames', ['colormap_name'])


def downgrade():
    op.drop_index('idx_colormap_status', table_name='image_frames')
    op.drop_table('image_frames')