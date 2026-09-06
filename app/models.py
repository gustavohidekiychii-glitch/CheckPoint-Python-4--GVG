from datetime import date, datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    data_nascimento = Column(Date, nullable=True)

    matriculas = relationship(
        "Matricula", back_populates="aluno", cascade="all, delete-orphan"
    )
    notas = relationship("Nota", back_populates="aluno", cascade="all, delete-orphan")
    frequencias = relationship(
        "Frequencia", back_populates="aluno", cascade="all, delete-orphan"
    )


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)

    turmas = relationship("Turma", back_populates="professor")


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    carga_horaria = Column(Integer, nullable=True)

    turmas = relationship("Turma", back_populates="disciplina")
    notas = relationship("Nota", back_populates="disciplina")


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=True)

    disciplina = relationship("Disciplina", back_populates="turmas")
    professor = relationship("Professor", back_populates="turmas")
    matriculas = relationship(
        "Matricula", back_populates="turma", cascade="all, delete-orphan"
    )
    frequencias = relationship(
        "Frequencia", back_populates="turma", cascade="all, delete-orphan"
    )


class Matricula(Base):
    __tablename__ = "matriculas"
    __table_args__ = (
        UniqueConstraint("aluno_id", "turma_id", name="uq_matricula_aluno_turma"),
    )

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    data_matricula = Column(DateTime, default=datetime.utcnow)

    aluno = relationship("Aluno", back_populates="matriculas")
    turma = relationship("Turma", back_populates="matriculas")

class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    valor = Column(Float, nullable=False)

    aluno = relationship("Aluno", back_populates="notas")
    disciplina = relationship("Disciplina", back_populates="notas")

class Frequencia(Base):
    __tablename__ = "frequencias"
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    data = Column(Date, default=date.today, nullable=False)
    presente = Column(Boolean, nullable=False, default=True)
    aluno = relationship("Aluno", back_populates="frequencias")
    turma = relationship("Turma", back_populates="frequencias")
