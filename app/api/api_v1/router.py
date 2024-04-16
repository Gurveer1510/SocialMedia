from fastapi import APIRouter
from .handlers.user_route import user_router
from .handlers.post_route import post_router
from .handlers.like_route import like_router
from ..auth import auth

router = APIRouter()


router.include_router(router=user_router, prefix='/api/v1')
router.include_router(router=auth.auth_router, prefix='/api/v1')
router.include_router(router=post_router, prefix='/api/v1')
router.include_router(router=like_router, prefix='/api/v1')