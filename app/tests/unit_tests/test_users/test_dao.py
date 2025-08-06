from app.users.dao import UserDAO
import pytest

@pytest.mark.parametrize("user_id,email,exist", [
    (1, "test@test.com", True),
    (2, "kocepi@nobody.com", True),
    (3, "wrong_info", False),
])
async def test_find_user_by_id(user_id,email,exist):
    user = await UserDAO.find_by_id(user_id)
    if exist:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user

