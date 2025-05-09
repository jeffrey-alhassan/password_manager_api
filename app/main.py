from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud, auth, database
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = auth.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/credentials", response_model=list[schemas.CredentialOut])
def read_credentials(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_credentials(db, user_id=current_user.id)

@app.post("/credentials", response_model=schemas.CredentialOut)
def create_credential(cred: schemas.CredentialCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.create_credential(db=db, cred=cred, user_id=current_user.id)

@app.get("/credentials/{cred_id}", response_model=schemas.CredentialOut)
def read_credential(cred_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_credential(db, cred_id=cred_id, user_id=current_user.id)

@app.put("/credentials/{cred_id}", response_model=schemas.CredentialOut)
def update_credential(cred_id: int, cred: schemas.CredentialCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.update_credential(db, cred_id=cred_id, cred=cred, user_id=current_user.id)

@app.delete("/credentials/{cred_id}")
def delete_credential(cred_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    crud.delete_credential(db, cred_id=cred_id, user_id=current_user.id)
    return {"detail": "Credential deleted"}


def main():
    print("Hello")


if __name__=='__main__':
    main()