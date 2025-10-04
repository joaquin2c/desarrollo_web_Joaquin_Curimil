from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum, Text

Base = declarative_base()

# --- Models ---

class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    #comunda_id = Column(Integer, nullable=False)
    comuna_id = Column(BigInteger, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    tipo = Column(Enum("gato","perro"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum("a","m"), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(String(500), nullable=False)

    comuna = relationship("Comuna", foreign_keys=[comuna_id],lazy='subquery' )

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(BigInteger, ForeignKey('region.id'), nullable=False)

    comuna = relationship("Region", foreign_keys=[region_id],lazy='subquery' )


class Region(Base):
    __tablename__ = 'region'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)



class Foto(Base):
    __tablename__ = 'foto'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    aviso_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'), nullable=False)



class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp','telegram','X','instagram','tiktok','otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    aviso_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'), nullable=False)
