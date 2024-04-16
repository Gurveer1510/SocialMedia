from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.models.user_model import Users
from app.models.likes_model import Likes, LikeModel
from app.models.posts_model import Post
from pymongo import errors
from uuid import UUID

like_router = APIRouter(tags=["like"])


@like_router.post("/post/like/{post_id}")
async def like_post(
    post_id: UUID, current_user: Users = Depends(UserService.get_current_user)
):
    like_payload: LikeModel = {"post_id": post_id, "user_id": current_user.user_id}
    # print(like_payload)
    try:

        like = Likes(like=like_payload)
        like_res = await like.insert()

        post = await Post.find_one(Post.post_id == post_id)
        
        if post:
            post.liked_by.append(current_user)
            post.likes += 1
            await post.save()

        return {"message": "like registererd", "like_res": like_res}

    except errors.DuplicateKeyError:

        existing_like = await Likes.find_one(
            Likes.like.user_id == like_payload["user_id"],
            Likes.like.post_id == like_payload["post_id"],
        )
        post = await Post.find_one(Post.post_id == post_id)
        post.likes -= 1
        await post.save()
        await existing_like.delete()
        return {"message": "like removed successfully"}
