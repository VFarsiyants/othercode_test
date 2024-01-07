from fastapi import APIRouter

from .endpoints import auth, post, user

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(user.router)
router.include_router(auth.router)
router.include_router(post.router)
