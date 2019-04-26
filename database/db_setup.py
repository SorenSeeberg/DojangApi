from database.db import SessionSingleton
from query.access_token import create as create_access_token
from database.tables import create_tables
from query.belt import create_belt_rows
from query.category import create_category_rows
from query.info import create_info_rows
from query.user import create_user_rows

if __name__ == '__main__':
    create_tables()
    create_user_rows()
    create_access_token(SessionSingleton().get_session(), user_id=1)
    create_belt_rows()
    create_category_rows()
    create_info_rows()
