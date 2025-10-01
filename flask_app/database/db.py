from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from .models import AvisoAdopcion, Comuna, Region, Foto, ContactarPor

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)


# --- Database Functions ---

def get_avisos(offset_value,page_size):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).offset(offset_value).limit(page_size).all()
    session.close()
    return avisos

def get_aviso_by_id(id):
    session = SessionLocal()
    aviso = session.query(AvisoAdopcion).filter_by(id=id).first()
    session.close()
    return aviso

def get_fotos_by_user_id(actividad_id):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(actividad_id=actividad_id).all()
    session.close()
    return fotos

def get_contactos_by_user_id(actividad_id):
    session = SessionLocal()
    contactos = session.query(ContactarPor).filter_by(actividad_id=actividad_id).all()
    session.close()
    return contactos

def create_aviso(fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    session = SessionLocal()
    new_aviso = AvisoAdopcion(fecha_ingreso=fecha_ingreso, comuna_id=comuna_id, sector=sector, nombre=nombre, email=email, 
                            celular=celular, tipo=tipo, cantidad=cantidad, edad=edad, unidad_medida=unidad_medida,
                            fecha_entrega=fecha_entrega, descripcion=descripcion)
    session.add(new_aviso)
    session.commit()
    id_aviso=new_aviso.id
    session.close()
    return id_aviso

def create_foto(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    new_foto = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, actividad_id=actividad_id)
    session.add(new_foto)
    session.commit()
    session.close()

def create_contactar_por(nombre, identificador, actividad_id):
    session = SessionLocal()
    new_foto = ContactarPor(nombre=nombre, identificador=identificador, actividad_id=actividad_id)
    session.add(new_foto)
    session.commit()
    session.close()