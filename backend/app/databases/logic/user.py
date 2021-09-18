from sqlalchemy.orm import Session

from databases.models.user import User



def get_user_by_user_name_and_password(db_session: Session, user_name: str, password: str) -> User:
    return db_session.query(User) \
                      .filter(User.email == user_name, 
                             User.password == password) \
                      .first()


def get_user_by_email(db_session: Session, email: str) -> User:
    return db_session.query(User) \
                      .filter(User.email == email) \
                      .first()