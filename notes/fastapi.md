Absolutely — here are **20 genuinely useful FastAPI snippets** that are great for **interviews, backend design rounds, and real services**, plus a section on **making third-party HTTP requests** cleanly.

I’m keeping these **copy-pasteable** and close to production style.

---

# 1. APIRouter for modular APIs

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]
```

```python
from fastapi import FastAPI
from app.routers.users import router as users_router

app = FastAPI()
app.include_router(users_router)
```

---

# 2. Pydantic request + response models

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users", response_model=UserOut)
async def create_user(payload: UserCreate):
    return {
        "id": 123,
        "name": payload.name,
        "email": payload.email,
    }
```

---

# 3. Dependency injection for shared services

```python
from fastapi import Depends, FastAPI

app = FastAPI()

class Settings:
    app_name = "My API"

def get_settings() -> Settings:
    return Settings()

@app.get("/info")
async def get_info(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}
```

---

# 4. Query params with validation

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def list_items(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return {"page": page, "page_size": page_size}
```

---

# 5. Path params with enums

```python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class Environment(str, Enum):
    dev = "dev"
    prod = "prod"

@app.get("/config/{env}")
async def get_config(env: Environment):
    return {"environment": env}
```

---

# 6. Centralized error handling with HTTPException

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

FAKE_DB = {1: {"id": 1, "name": "Alice"}}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = FAKE_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

# 7. Custom exception + global handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class ExternalServiceError(Exception):
    def __init__(self, service: str, message: str):
        self.service = service
        self.message = message

@app.exception_handler(ExternalServiceError)
async def external_service_error_handler(request: Request, exc: ExternalServiceError):
    return JSONResponse(
        status_code=502,
        content={
            "error": "external_service_error",
            "service": exc.service,
            "message": exc.message,
        },
    )

@app.get("/demo-error")
async def demo_error():
    raise ExternalServiceError("billing-api", "Timed out")
```

---

# 8. Middleware for request timing

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.6f}"
    return response
```

---

# 9. Simple request logging middleware

```python
import logging
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Incoming request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("Response status: %s", response.status_code)
    return response
```

---

# 10. BackgroundTasks for non-blocking side work

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def send_welcome_email(email: str) -> None:
    print(f"Sending welcome email to {email}")

@app.post("/signup")
async def signup(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_welcome_email, email)
    return {"message": "User created, email scheduled"}
```

---

# 11. File upload endpoint

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
    }
```

---

# 12. StreamingResponse for chunked output

```python
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_stream():
    for i in range(5):
        yield f"chunk-{i}\n"
        await asyncio.sleep(0.2)

@app.get("/stream")
async def stream():
    return StreamingResponse(event_stream(), media_type="text/plain")
```

---

# 13. Pagination pattern

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

DATA = [{"id": i, "name": f"user-{i}"} for i in range(1, 501)]

@app.get("/users")
async def list_users(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return {
        "items": DATA[offset : offset + limit],
        "offset": offset,
        "limit": limit,
        "total": len(DATA),
    }
```

---

# 14. Header extraction

```python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/whoami")
async def whoami(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}
```

---

# 15. API key auth via header

```python
from typing import Annotated
from fastapi import FastAPI, Header, HTTPException, status, Depends

app = FastAPI()

EXPECTED_API_KEY = "super-secret"

async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key

@app.get("/protected")
async def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Authorized"}
```

---

# 16. OAuth2 bearer token extraction

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/profile")
async def profile(token: str = Depends(oauth2_scheme)):
    return {"access_token": token}
```

---

# 17. SQLAlchemy session dependency pattern

```python
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/health/db")
async def db_healthcheck(db: Session = Depends(get_db)):
    db.execute("SELECT 1")
    return {"status": "ok"}
```

---

# 18. Lifespan startup/shutdown pattern

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

class FakeClient:
    async def aclose(self):
        print("closing client")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.external_client = FakeClient()
    print("startup complete")
    yield
    await app.state.external_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

This is the clean modern way to initialize shared clients like:

* `httpx.AsyncClient`
* Redis
* database pools
* vector DB clients

---

# 19. Simple in-memory rate limiter

```python
import time
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Request, status

app = FastAPI()

REQUEST_LOG: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 5
WINDOW_SECONDS = 60

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    REQUEST_LOG[client_ip] = [
        ts for ts in REQUEST_LOG[client_ip]
        if now - ts < WINDOW_SECONDS
    ]

    if len(REQUEST_LOG[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )

    REQUEST_LOG[client_ip].append(now)
    return await call_next(request)
```

For production, you’d usually use Redis or an API gateway instead of in-memory state.

---

# 20. Basic response caching decorator pattern

```python
import time
from functools import wraps
from fastapi import FastAPI

app = FastAPI()
CACHE: dict[str, tuple[float, dict]] = {}

def cache_response(ttl_seconds: int):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            key = f"{fn.__name__}:{args}:{kwargs}"
            now = time.time()

            if key in CACHE:
                expires_at, value = CACHE[key]
                if now < expires_at:
                    return value

            value = await fn(*args, **kwargs)
            CACHE[key] = (now + ttl_seconds, value)
            return value
        return wrapper
    return decorator

@app.get("/expensive")
@cache_response(ttl_seconds=30)
async def expensive_call():
    return {"data": "cached-result"}
```

---

# Third-party requests in FastAPI

This is a big one in interviews.

Senior interviewers often want to see that you know:

* how to call another service
* how to set timeouts
* how to reuse clients
* how to handle retries/errors
* how to avoid blocking the event loop

## 21. Simple third-party GET with `httpx`

```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        response.raise_for_status()
        return response.json()
```

This works, but creating a new client per request is not ideal for high traffic.

---

## 22. Reusable shared `httpx.AsyncClient`

```python
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(5.0, connect=2.0),
    )
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    response = await app.state.http_client.get(
        f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    )
    response.raise_for_status()
    return response.json()
```

This is much better for production.

---

## 23. Third-party POST request

```python
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/proxy-login")
async def proxy_login(username: str, password: str):
    payload = {"username": username, "password": password}

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(
                "https://example.com/api/login",
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Upstream returned error: {exc.response.text}",
            )
```

---

## 24. Add headers/auth to external requests

```python
import httpx
from fastapi import FastAPI

app = FastAPI()

API_TOKEN = "my-token"

@app.get("/external-profile")
async def external_profile():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get("https://example.com/api/me", headers=headers)
        response.raise_for_status()
        return response.json()
```

---

## 25. Dependency-injected external client

```python
import httpx
from fastapi import Depends, FastAPI, Request

app = FastAPI()

def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

@app.get("/weather")
async def weather(client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get("https://example.com/weather")
    response.raise_for_status()
    return response.json()
```

This pattern is nicer for testing and cleaner architecture.

---

## 26. Graceful timeout handling

```python
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/slow-upstream")
async def slow_upstream():
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(3.0, connect=1.0)) as client:
            response = await client.get("https://example.com/slow")
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Upstream service timed out")
```

---

## 27. Map upstream failures to 502

```python
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/billing-summary")
async def billing_summary():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://example.com/billing/summary")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "upstream_http_error",
                "upstream_status": exc.response.status_code,
            },
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not reach upstream billing service",
        )
```

---

## 28. Retry wrapper for flaky upstreams

```python
import asyncio
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

async def get_with_retries(
    client: httpx.AsyncClient,
    url: str,
    retries: int = 3,
    delay_seconds: float = 0.5,
) -> dict:
    last_error = None

    for attempt in range(retries):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            last_error = exc
            if attempt < retries - 1:
                await asyncio.sleep(delay_seconds)

    raise HTTPException(status_code=502, detail=f"Upstream failed after retries: {last_error}")

@app.get("/resilient")
async def resilient():
    async with httpx.AsyncClient(timeout=5.0) as client:
        return await get_with_retries(client, "https://example.com/api/data")
```

In production, add:

* exponential backoff
* jitter
* retry only for safe/idempotent cases
* circuit breaker if failures persist

---

## 29. Parallel third-party requests

```python
import asyncio
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/dashboard")
async def dashboard():
    async with httpx.AsyncClient(timeout=5.0) as client:
        users_task = client.get("https://example.com/users")
        orders_task = client.get("https://example.com/orders")
        inventory_task = client.get("https://example.com/inventory")

        users_resp, orders_resp, inventory_resp = await asyncio.gather(
            users_task,
            orders_task,
            inventory_task,
        )

        users_resp.raise_for_status()
        orders_resp.raise_for_status()
        inventory_resp.raise_for_status()

        return {
            "users": users_resp.json(),
            "orders": orders_resp.json(),
            "inventory": inventory_resp.json(),
        }
```

Great interview talking point: parallelizing I/O-bound upstream calls to reduce total latency.

---

## 30. Service class for external APIs

```python
import httpx

class BillingService:
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def get_invoice(self, invoice_id: str) -> dict:
        response = await self.client.get(f"{self.base_url}/invoices/{invoice_id}")
        response.raise_for_status()
        return response.json()
```

```python
from fastapi import Depends, FastAPI, Request

app = FastAPI()

def get_billing_service(request: Request) -> BillingService:
    client: httpx.AsyncClient = request.app.state.http_client
    return BillingService(client=client, base_url="https://example.com/api")

@app.get("/invoices/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    billing_service: BillingService = Depends(get_billing_service),
):
    return await billing_service.get_invoice(invoice_id)
```

This is the cleanest pattern when you want interviewers to see layered design.

---

# A realistic production-style example

This combines:

* FastAPI
* shared async client
* dependency injection
* upstream call
* timeout/error mapping

```python
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request

class UserService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def fetch_user(self, user_id: str) -> dict:
        try:
            response = await self.client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            raise HTTPException(status_code=504, detail="User service timeout") from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"User service error: {exc.response.status_code}",
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail="User service unavailable") from exc

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(5.0, connect=1.0)
    )
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

def get_user_service(request: Request) -> UserService:
    return UserService(request.app.state.http_client)

@app.get("/users/{user_id}")
async def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    return await user_service.fetch_user(user_id)
```

---

# What senior engineers usually say in interviews

When they ask about FastAPI + third-party requests, strong talking points are:

* Use `httpx.AsyncClient`, not blocking `requests`, inside async handlers.
* Reuse a shared client through app lifespan for connection pooling.
* Always set explicit timeouts.
* Separate transport concerns from route handlers with service classes.
* Map upstream failures to appropriate API errors like `502` or `504`.
* Use retries carefully, mainly for idempotent operations.
* Use `asyncio.gather()` for independent parallel upstream calls.
* For production, add observability: structured logs, tracing, metrics, request IDs.

---

# The 10 snippets I’d memorize first

If you only memorize a smaller set, make it these:

1. request/response models
2. `Depends(...)`
3. `APIRouter`
4. `HTTPException`
5. middleware
6. DB session dependency
7. lifespan/shared clients
8. `httpx.AsyncClient` third-party calls
9. timeout + upstream error mapping
10. parallel requests with `asyncio.gather()`

---

# Tiny cheat sheet

```python
# async route
@app.get("/x")
async def route():
    ...

# dependency
def get_service(): ...
@app.get("/x")
async def route(service = Depends(get_service)):
    ...

# upstream call
async with httpx.AsyncClient(timeout=5.0) as client:
    resp = await client.get("https://example.com")
    resp.raise_for_status()

# shared client
app.state.http_client = httpx.AsyncClient(...)

# error
raise HTTPException(status_code=404, detail="Not found")
```

I can turn this into a **single interview-ready FastAPI starter template** next — with folders like `routers/`, `services/`, `schemas/`, `dependencies/`, and `main.py`.
