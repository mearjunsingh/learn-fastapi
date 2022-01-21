from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2


router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'User has already liked the post')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Successfully Voted'}
    else:
        if not vote_found:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'User has not liked the post')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Successfully Unvoted'}