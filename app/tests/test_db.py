from sqlmodel import Session 
from models.user import User
import pytest

def test_create_user(session: Session):
    user = User(id=1, email="test@mail.ru", password="1234")
    session.add(user)
    session.commit()
    
def test_fail_create_user(session: Session):
    with pytest.raises(Exception) as ex:
        user = User(id=1, email="test_2@mail.ru", password="12")
        session.add(user)
        session.commit()
        
def test_delete_user(session: Session):
    test_create_user(session)
    
    user = session.get(User, 1)
    assert user is not None, "User with id=0 not found"

    session.delete(user)
    session.commit()

    deleted_user = session.get(User, 1)
    assert deleted_user is None, "User was not deleted"
