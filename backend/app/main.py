from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.utils.config import settings

app = FastAPI(title="Sleepy Cat Books")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Did not find better way to do it
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    messages = []
    errs = exc.args[0]
    
    for err in errs:
        err_obj = {}
        if "loc" in err:
            err_obj["field"] = err["loc"][1]
        if "msg" in err:
            err_obj["msg"] = err["msg"]
        
        messages.append(err_obj)

    print("Validation error handler:", messages)

    return JSONResponse(status_code=400, content={"detail": messages})


app.include_router(api_router)