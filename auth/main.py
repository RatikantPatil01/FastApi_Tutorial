# ==============================
# IMPORTS
# ==============================

# FastAPI → Create API
# Depends → Dependency Injection (auto execute functions)
# HTTPException → Raise custom errors
# status → Ready HTTP status codes (401,403,404...)
from fastapi import FastAPI, Depends, HTTPException, status

# Session → Used to communicate with database
from sqlalchemy.orm import session

# models → SQLAlchemy tables
# schemas → Pydantic validation
# utils → Helper functions (hash password etc.)
from auth import models, schemas, utils

# Database connection function
from auth.auth_database import get_db

# JWT functions
# jwt → create/decode token
# JWTError → catch invalid token errors
from jose import jwt, JWTError

# Time handling for token expiry
from datetime import datetime, timedelta

# Login form support
# OAuth2PasswordRequestForm → receives username/password
# OAuth2PasswordBearer → extracts Bearer Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer



# ==============================
# JWT SETTINGS
# ==============================

# Secret key used to sign token
# Never expose publicly
SECRET_KEY = "YOUR_SECRET_KEY"

# Encryption algorithm
ALGORITHM = "HS256"

# Token validity
ACCESS_TOKEN_EXPIRE_MINUTES = 30



# ==============================
# CREATE JWT TOKEN
# ==============================

def create_access_token(data: dict):

    # Create copy so original data not change
    to_encode = data.copy()

    # Current time + 30 min
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiration inside payload
    to_encode.update({
        "exp": expire
    })

    # Convert payload → JWT string
    encode_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encode_jwt



# Create FastAPI app
app = FastAPI()



# ==============================
# SIGNUP
# ==============================

@app.post("/signup")

def register_user(
        user: schemas.UserCreate,
        db: session = Depends(get_db)
):

    # Check username exists
    existing_user = (
        db.query(models.User)
        .filter(
            models.User.username == user.username
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username Already Exists"
        )

    # Convert password → encrypted
    hashed_pass = utils.hash_password(
        user.password
    )

    # Create database object
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pass,
        role=user.role
    )

    # Save into DB
    db.add(new_user)
    db.commit()

    # Reload data after save
    db.refresh(new_user)

    return {
        "message": "User Added Successfully",
        "data": new_user
    }



# ==============================
# LOGIN
# ==============================

@app.post("/login")

def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: session = Depends(get_db)
):

    # Find user
    user = (
        db.query(models.User)
        .filter(
            models.User.username ==
            form_data.username
        )
        .first()
    )

    # Username wrong
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Username"
        )

    # Password wrong
    if not utils.verify_password(
            form_data.password,
            user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    # Data inside token
    token_data = {
        "sub": user.username,
        "role": user.role
    }

    # Generate JWT
    token = create_access_token(
        token_data
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }



# ==============================
# TOKEN EXTRACTION
# ==============================

# Reads:
# Authorization: Bearer TOKEN
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)



# ==============================
# VERIFY TOKEN
# ==============================

def get_current_user(
        token: str =
        Depends(oauth2_scheme)
):

    # Error object
    credential_exception = (
        HTTPException(
            status_code=401,
            detail="Could not validate credential",
            headers={
                "WWW-Authenticate":
                "Bearer"
            }
        )
    )

    try:

        # Decode token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )

        # Extract username
        username = payload.get("sub")

        # Extract role
        role = payload.get("role")

        # Missing data
        if (
                username is None
                or role is None
        ):
            raise credential_exception

    except JWTError:
        raise credential_exception

    return {
        "username": username,
        "role": role
    }



# ==============================
# PROTECTED ROUTE
# ==============================

@app.get("/protected")

def protected_route(
        current_user:
        dict =
        Depends(
            get_current_user
        )
):

    return {
        "message":
            f"Hello "
            f"{current_user['username']}"
    }



# ==============================
# ROLE AUTHORIZATION
# ==============================

def require_roles(
        allowed_roles:
        list[str]
):

    def role_checker(
            current_user=
            Depends(
                get_current_user
            )
    ):

        user_role = (
            current_user
            .get("role")
        )

        # Block access
        if (
                user_role
                not in allowed_roles
        ):
            raise HTTPException(
                status_code=403,
                detail=
                "Permission denied"
            )

        return current_user

    return role_checker



# ==============================
# USER + ADMIN
# ==============================

@app.get("/profile")

def profile(
        current_user=
        Depends(
            require_roles(
                [
                    "user",
                    "admin"
                ]
            )
        )
):

    return {
        "message":
            f"profile "
            f"{current_user['username']}"
    }



# ==============================
# USER ONLY
# ==============================

@app.get(
"/user/dashboard"
)

def user_dashboard(
        current_user=
        Depends(
            require_roles(
                ["user"]
            )
        )
):

    return {
        "message":
        "Welcome User"
    }



# ==============================
# ADMIN ONLY
# ==============================

@app.get(
"/admin/dashboard"
)

def admin_dashboard(
        current_user=
        Depends(
            require_roles(
                ["admin"]
            )
        )
):

    return {
        "message":
        "Welcome Admin"
    }











# from fastapi import FastAPI,Depends,HTTPException, status
# from sqlalchemy.orm import session
# import models,schemas,utils
# from auth_database import get_db
# from jose import jwt,JWTError
# from datetime import datetime,timedelta
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# SECRET_KEY = "YP1ZhvfrQ27MERUdtNKGEibseZzS3tz6Jn67cHfDEfo"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Helper function that takes user data
# def create_access_token(data:dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({'exp':expire})
#     encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encode_jwt

# app = FastAPI()

# @app.post("/signup")
# def register_user(user:schemas.UserCreate, db: session = Depends(get_db)):
#     # Check the user exit or not
#     exisiting_user = db.query(models.User).filter(models.User.username == user.username).first()
#     if exisiting_user:
#         raise HTTPException(status_code=400,detail="Username Alerady Exists !!")
    
#     # Hash the password
#     hashed_pass = utils.hash_password(user.password)

#     # Create new user instance
#     new_user = models.User(
#         username = user.username,
#         email = user.email,
#         hashed_password = hashed_pass,
#         role = user.role
#     )

#     # Save user to database
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     # Return the value ( excluding password )
#     return {"message":"User Addded Successfully" , "data":new_user}

# @app.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db:session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.username == form_data.username).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")
    
#     if not utils.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
#     token_data = {'sub':user.username,'role':user.role}
#     token = create_access_token(token_data)
#     return {"access_token":token, "token_type":"bearer"}


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credential",headers={"WWW-Authenticate":"Bearer"})

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
#         username: str = payload.get("sub")
#         role: str = payload.get("role")
#         if username is None or role is None:
#             raise credential_exception

#     except JWTError:
#         raise credential_exception
    
#     return {"username":username,"role":role}

# @app.get("/protected")
# def protected_route(current_user:dict = Depends(get_current_user)):
#     return {"Messege":f"Hello, {current_user['username']} | You accessed a protected Route"}

# def require_roles(allowed_roles:list[str]):
#     def role_checker(current_user:dict = Depends(get_current_user)):
#         user_role = current_user.get("role")
#         if user_role not in allowed_roles:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permsission")
        
#         return current_user
#     return role_checker

# @app.get("/profile")
# def profile(current_user: dict = Depends(require_roles(["user","admin"]))):
#     return {"messege":f"profile of {current_user['username']} ({current_user['role']})"}

# @app.get("/user/dashboard")
# def user_dashboard(current_user: dict = Depends(require_roles(['user']))):
#     return {"message":"Welcome to user Dashboard"}

# @app.get("/admin/dashboard")
# def user_dashboard(current_user: dict = Depends(require_roles(['admin']))):
#     return {"message":"Welcome to admin Dashboard"}
























