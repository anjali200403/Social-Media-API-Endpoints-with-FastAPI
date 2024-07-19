from typing import List, Optional
from fastapi import  HTTPException, Response,status,Depends,APIRouter
from .. import models,oauth
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..schemas import Post,PostOut

router=APIRouter( tags=['Posts'])

@router.get("/posts",response_model=List[PostOut])
def get_posts(db: Session=Depends(get_db),getCurrentUser:int=Depends(oauth.get_current_user),limit:int=10,skip:int =0,search:Optional[str]=""):
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get("/posts/myposts",response_model=List[PostOut])
def get_your_posts(db: Session=Depends(get_db),getCurrentUser:int=Depends(oauth.get_current_user)):
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.user_id==getCurrentUser.id).all()
    return posts

@router.get("/posts/{id}",response_model=PostOut)
def get_post_by_id(id: int,db: Session=Depends(get_db),getCurrentUser:int=Depends(oauth.get_current_user)):
    req_post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not req_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"posts with id={id} not found")
    return req_post


@router.post("/posts")
def create_post(post: PostIn,db: Session=Depends(get_db),getCurrentUser:int=Depends(oauth.get_current_user)):
    new_post_data = post.model_dump()  
    new_post_data["user_id"] = getCurrentUser.id  
    new_post = models.Post(**new_post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"New post created": new_post}

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session=Depends(get_db),getCurrentUser:int=Depends(oauth.get_current_user)):
    query_post=db.query(models.Post).filter(models.Post.id==id)
    post=query_post.first()
    if not query_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"posts with id={id} not found")
    if post.user_id!=getCurrentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the given action")
    query_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id:int,post:Post,db: Session=Depends(get_db),getCurrentUser:int=Depends(oauth.get_current_user)):
    query_post=db.query(models.Post).filter(models.Post.id==id)
    post=query_post.first()
    if not query_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"posts with id={id} not found")
    if post.user_id!=getCurrentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the given action")
    query_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return {"Updated Post ":query_post.first()}
