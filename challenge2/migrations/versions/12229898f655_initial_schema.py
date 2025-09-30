"""initial schema"""
from alembic import op
import sqlalchemy as sa


revision = '12229898f655'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('target_width', sa.Integer(), nullable=False),
        sa.Column('total_frames', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('csv_source', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'image_frames',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('image_id', sa.Integer(), nullable=False),
        sa.Column('depth', sa.Float(), nullable=False),
        sa.Column('pixels', sa.JSON(), nullable=False),
        sa.Column('color_map_pixels', sa.JSON(), nullable=True),
        sa.Column('colormap_name', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('colormap_applied_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE')
    )
    op.create_index('idx_image_depth', 'image_frames', ['image_id', 'depth'], unique=True)
    op.create_index('idx_colormap_status', 'image_frames', ['image_id', 'colormap_name'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_colormap_status', table_name='image_frames')
    op.drop_index('idx_image_depth', table_name='image_frames')
    op.drop_table('image_frames')
    op.drop_table('images')