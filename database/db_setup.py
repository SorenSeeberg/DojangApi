from database.tables import create_tables
from database.belt import create_belt_rows
from database.category import create_category_rows
from database.info import create_info_rows
from database.user import create_user_rows
from database.access_token import create_access_token

if __name__ == '__main__':
    create_tables()
    create_user_rows()
    create_access_token(user_id=1)
    create_belt_rows()
    create_category_rows()
    create_info_rows()
