from .models import User, Project
from sqlalchemy.orm import sessionmaker, session, Session


class UserHandler:
    def __init__(self, session_temp: Session, session_consolidada: Session):
        self.session_temp = session_temp
        self.session_consolidada = session_consolidada

    def create_user(self, user_data: dict):
        user_consolidada = (
            self.session_consolidada.query(User)
            .filter_by(login=user_data["login"])
            .first()
        )
        if user_consolidada:
            return {
                "created": False,
                "user": {
                    column.name: getattr(user_consolidada, column.name)
                    for column in User.__table__.columns
                },
            }
        print("No existe en consolidada")
        existing_user = (
            self.session_temp.query(User).filter_by(login=user_data["login"]).first()
        )
        if existing_user:
            for key, value in user_data.items():
                setattr(existing_user, key, value)
            self.session_temp.commit()
            return {"created": False, "user": existing_user}
        else:
            new_user = User(**user_data)
            self.session_temp.add(new_user)
            self.session_temp.commit()
            return {"created": True, "user": new_user}
