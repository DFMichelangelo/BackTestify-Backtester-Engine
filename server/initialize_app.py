
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from routes import backtest, strategy, optimization
from logger.std_logger import init_std_logger
from logger import Logger
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
# INFO - Initialize STD Logger
init_std_logger()


logger = Logger("Initialize App", "green")
logExceptions = Logger("Exceptions", "red")


app = FastAPI()

# INFO - Routes
app.include_router(
    backtest.router,
    prefix="/backtest",
    tags=["Backtest"])
app.include_router(
    strategy.router,
    tags=["Strategy"])
app.include_router(
    optimization.router,
    prefix="/optimization",
    tags=["Optimization"])


# INFO - Validation Error Exception Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logExceptions.error(f"{request}: {exc_str}")
    return JSONResponse(content=exc_str, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logExceptions.error(f"{request.url} - {str(exc.detail)}")
    return JSONResponse(content=str(exc.detail), status_code=exc.status_code)

origins = [
    "https://localhost:3000",
    os.getenv('FRONTEND_URL')
]

# INFO - CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("App Initialized")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    html_content = f'''
    <html>
        <head>
            <title>BackTestiPy Backend</title >
        </head>
        <body>
            <h1> BackTestiPy Backend </h1>
            <a href = {str(request.url)+"docs"}> <h2> API Documentation in Swagger </h2> </a>
            <a href = {str(request.url)+"redoc"}> <h2> API Documentation in Redoc </h2> </a>
         </body>
     </html>
     '''
    return HTMLResponse(content=html_content, status_code=200)
