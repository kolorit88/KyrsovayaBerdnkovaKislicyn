# backend/infrastructure/db/migrations/versions/c30c8bbdd23b_seed_all_data.py
"""seed_all_data

Revision ID: c30c8bbdd23b
Revises: 1f480ed971f2
Create Date: 2026-04-24 21:30:30.269059

"""
import json
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'c30c8bbdd23b'
down_revision: Union[str, Sequence[str], None] = '1f480ed971f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def load_seed_data() -> dict:
    """Загружает все данные из JSON файла"""
    # Путь относительно файла миграции
    data_file = Path(__file__).parent.parent.parent / "seeders" / "data" / "merchandise_default_test.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def upgrade() -> None:
    """Заполняем категории, товары и вариации"""
    data = load_seed_data()
    connection = op.get_bind()
    
    # 1. Вставляем категории
    for category in data['categories']:
        connection.execute(
            sa.text("""
                INSERT INTO merchandise_categories (name, slug, description)
                VALUES (:name, :slug, :description)
                ON CONFLICT (slug) DO NOTHING
            """),
            category
        )
    
    # 2. Получаем map slug -> id категорий
    categories = connection.execute(
        sa.text("SELECT id, slug FROM merchandise_categories")
    ).fetchall()
    slug_to_id = {cat.slug: cat.id for cat in categories}
    
    # 3. Вставляем товары и вариации
    for merch in data['merchandise']:
        category_id = slug_to_id[merch['category_slug']]
        
        # Вставляем товар
        result = connection.execute(
            sa.text("""
                INSERT INTO merchandise (category_id, name, description, image)
                VALUES (:category_id, :name, :description, :image)
                RETURNING id
            """),
            {
                'category_id': category_id,
                'name': merch['name'],
                'description': merch['description'],
                'image': merch['image']
            }
        )
        merchandise_id = result.scalar()
        
        # Вставляем вариации для товара
        for variation in merch['variations']:
            connection.execute(
                sa.text("""
                    INSERT INTO merchandise_variations 
                    (merchandise_id, quantity, price, variation_text, weight_gram)
                    VALUES (:merchandise_id, :quantity, :price, :variation_text, :weight_gram)
                """),
                {
                    'merchandise_id': merchandise_id,
                    **variation
                }
            )


def downgrade() -> None:
    """Удаляем все данные (в обратном порядке)"""
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM merchandise_variations"))
    connection.execute(sa.text("DELETE FROM merchandise"))
    connection.execute(sa.text("DELETE FROM merchandise_categories"))