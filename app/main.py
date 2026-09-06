from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routers import alunos, professores, disciplinas, turmas, matriculas, notas, frequencias

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SchoolManager - API",
    description=(
        "API REST do sistema SchoolManager, para gerenciamento de alunos, professores, turmas, disciplinas, matrículas, notas e frequência."
    ),
    version="1.0.0",
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"erro": True, "mensagem": exc.detail},
    )
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"erro": True, "mensagem": "Dados inválidos", "detalhes": exc.errors()},
    )
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"erro": True, "mensagem": "Erro interno no servidor"},
    )

@app.get("/", tags=["Status"])
def status_api():
    return {"mensagem": "API do SchoolManager no ar", "docs": "/docs"}


app.include_router(alunos.router)
app.include_router(professores.router)
app.include_router(disciplinas.router)
app.include_router(turmas.router)
app.include_router(matriculas.router)
app.include_router(notas.router)
app.include_router(frequencias.router)
