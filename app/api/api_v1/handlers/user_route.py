from fastapi import APIRouter, status, HTTPException, UploadFile, File, Depends
import secrets
from PIL import Image
from app.models.user_model import Users
from app.models.posts_model import Post
from app.schemas.user_schema import UserAuth
from app.schemas.user_schema import UserOut
from app.services.user_service import UserService
import pymongo
from uuid import UUID
from beanie.odm.operators.update.array import Push


user_router = APIRouter(tags=['users'])


@user_router.post("/users/",status_code=status.HTTP_201_CREATED,response_description=f"user created successfully", response_model=UserOut)
async def create_user(user: UserAuth):
    
    try:
       print(user.model_dump())
       return await UserService.create_user(user)

    except pymongo.errors.DuplicateKeyError :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"email or username already taken")




@user_router.post("/users/upload/profile")
async def upload_profile_image(file : UploadFile = File(...), current_user = Depends(UserService.get_current_user)):
    FILEPATH = "app/static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ['png', 'jpg', 'PNG', 'JPG']:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"only png and jpg format accepted")

    token_name = f"{secrets.token_hex(10)}.{extension}"

    generated_name = f"{FILEPATH}{token_name}"

    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)
    
    # PILLOW
    img = Image.open(generated_name)
    img = img.resize(size=(900,700))
    img.save(generated_name)

    file.close()

    await Users.find_one(Users.username == current_user.username).set({Users.profile_pic : f"http://localhost:8000/{generated_name}"})

    posts_from_current_user =  Post.find({"owner.username" : current_user.username})
    
    
            
    myList = await posts_from_current_user.to_list()
   
    for post in myList:
        post.owner.profile_pic =  f"http://localhost:8000/{generated_name}"
        await post.replace()


    return {
        "profile_image" : f"http://localhost:8000/{generated_name}"
    }


@user_router.get('/user/{username}', response_model=UserOut)
async def get_user_by_username(username: str, current_user = Depends(UserService.get_current_user)):
    user = await Users.find_one(Users.username == username)
    print(current_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with that username does not exist")
    
    return user


@user_router.post("/user/follow", name="follow/unfollow user")
async def follow_user(userId : UUID, current_user = Depends(UserService.get_current_user)):
    
    try: 
            message = await UserService.follow_user(userId, current_user)
            return {
                'message' : message
            }
    except:
           
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"someting went wrong")
        
