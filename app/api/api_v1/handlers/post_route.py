from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from app.schemas.post_schema import Post_Schema
from app.schemas.user_schema import FollowSchema
from app.models.posts_model import Post
from app.services.user_service import UserService
from secrets import token_hex
from PIL import Image
from uuid import UUID

post_router = APIRouter(tags=['post'])

@post_router.post('/post/create')
async def create_post(caption : str, file : UploadFile = File(...), current_user = Depends(UserService.get_current_user)):

    FILEPATH = "app/posts/"
    filename = file.filename
    extension = filename.split('.')[1]

    if extension not in ['jpg', 'png', 'JPG', 'PNG']:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'only jpg or png files accepted')
       
    token_name = f'{token_hex(10)}.{extension}'

    generated_name = f'{FILEPATH}{token_name}'

    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

        #PILLOW
    img = Image.open(generated_name)
    img = img.resize(size=(500,500))
    img.save(generated_name)

    file.close()
    
    post = Post(caption=caption, owner=current_user, post_image=f'http://localhost:8000/{generated_name}')

    await post.insert()

    if post :
        return  post
    
@post_router.get("/posts/{username}")
async def get_all_posts(username : str, current_user = Depends(UserService.get_current_user)):
    posts = await Post.find({'owner.username' : username}).to_list()
    
    for post in posts:
        print(post)
    
    if not posts:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no posts found")
    
    return {
        "data": posts
    }

@post_router.delete("/post/remove/{post_id}")
async def remove_post(post_id : UUID, current_user : FollowSchema = Depends(UserService.get_current_user)):

    try:

        post = await Post.find_one(Post.post_id == post_id)
        post_dump = post.model_dump()
        print(post_dump.get('owner')['username'])
        print(current_user.username)
        if post:

            if post_dump.get('owner')['username'] == current_user.username : 
                await post.delete()
                return{
                    'status' : status.HTTP_204_NO_CONTENT
                }
        
            else: 
                return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not the owner of this post")

    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"no post found with {post_id} post id")

