from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_users():
    return [
        {
            "username": "Rick",
        },
        {
            "username": "Morty",
        }
    ]

@router.get("/users/me")
async def read_user_me():
    return {
        "username": "fakecurrentuser",
    }

@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {
        "username": f"{user_id}_user",
    }


