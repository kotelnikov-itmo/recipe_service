from models import Tag, User, Recipe, DishTypes
from db import LocalSession
from sqlalchemy.orm import Session


def create_inithial_data(db_session: Session):
    try:
        tags = [
            Tag(title="asian"), Tag(title="fast-food")
        ]
        db_session.add_all(tags)
        db_session.commit()

        users = [
            User(username="test_user", hpass="@---", is_active=True),
            User(username="other_user", hpass="qwerty", is_active=False)
        ]
        db_session.add_all(users)
        db_session.commit()
        # db_session.refresh(users)

        recipes = [
            Recipe(
                title="pancakes", description="classic russian pancakes", likes_count=120,
                author_id=users[0].id, is_active=True, dish_type=DishTypes.desert
            ), Recipe(
                title="pizza", description="Four Cheeses", likes_count=20,
                author_id=users[0].id, is_active=True, dish_type=DishTypes.second
            ), Recipe(
                title="cream soup", description="...", likes_count=0, tags=[tags[1], ],
                author_id=users[1].id, is_active=True, dish_type=DishTypes.soup
            ), Recipe(
                title="Wok + chicken", description="wok for 4 person", likes_count=200,
                author_id=users[0].id, is_active=False, dish_type=DishTypes.first, tags=[tags[0], ]
            )
        ]
        db_session.add_all(recipes)
        db_session.commit()

    finally:
        db_session.close()


if __name__ == '__main__':
    create_inithial_data(db_session=LocalSession())
