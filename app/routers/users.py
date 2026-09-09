from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserStatusUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.asc()).all()
    # Format role capitalizing for admin table view (e.g. Student, Organizer, Admin)
    results = []
    for u in users:
        formatted_role = "Student" if u.role.lower() == "user" else u.role.capitalize()
        results.append(UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            role=formatted_role,
            department=u.department or "",
            status=u.status
        ))
    return results

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    formatted_role = "Student" if user.role.lower() == "user" else user.role.capitalize()
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=formatted_role,
        department=user.department or "",
        status=user.status
    )

@router.patch("/{user_id}/status", response_model=UserResponse)
def toggle_user_status(
    user_id: int,
    status_data: Optional[UserStatusUpdate] = None,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if status_data and status_data.status:
        user.status = status_data.status
    else:
        user.status = "Inactive" if user.status == "Active" else "Active"

    db.commit()
    db.refresh(user)

    formatted_role = "Student" if user.role.lower() == "user" else user.role.capitalize()
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=formatted_role,
        department=user.department or "",
        status=user.status
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user)
    db.commit()
    return None
