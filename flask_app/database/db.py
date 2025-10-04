from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, desc 
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
    avisos = session.query(AvisoAdopcion).order_by(desc(AvisoAdopcion.id))
    avisos_total=avisos.count()
    chosen_avisos=avisos.offset(offset_value).limit(page_size).all()
    #avisos = session.query(AvisoAdopcion).offset(offset_value).limit(page_size).all()
    session.close()
    return chosen_avisos,avisos_total

def get_aviso_by_id(id):
    session = SessionLocal()
    aviso = session.query(AvisoAdopcion).filter_by(id=id).first()
    session.close()
    return aviso

def get_fotos_by_user_id(aviso_id):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(aviso_id=aviso_id).all()
    session.close()
    return fotos

def get_contactos_by_user_id(aviso_id):
    session = SessionLocal()
    contactos = session.query(ContactarPor).filter_by(aviso_id=aviso_id).all()
    session.close()
    return contactos

def get_comuna_by_id(comuna_id):
    session = SessionLocal()
    contactos = session.query(Comuna).filter_by(id=comuna_id).first()
    session.close()
    return contactos

def get_comuna_by_nombre(nombre):
    session = SessionLocal()
    contactos = session.query(Comuna).filter_by(nombre=nombre).first()
    session.close()
    return contactos

def create_aviso(info_data):
    session = SessionLocal()
    print(info_data["fecha_ingreso"],info_data["comuna"],info_data["region"],info_data["sector"],info_data["nombre"],info_data["email"], 
                            info_data["celular"],info_data["tipo"],info_data["cantidad"],info_data["edad"],info_data["unidad_medida"],
                            info_data["fecha_entrega"],info_data["descripcion"]) #Comuna(info_data["comuna"],info_data["region"])
    new_aviso = AvisoAdopcion(fecha_ingreso=info_data["fecha_ingreso"], comuna_id=get_comuna_by_nombre(info_data["comuna"]).id, sector=info_data["sector"], nombre=info_data["nombre"], email=info_data["email"], 
                            celular=info_data["celular"], tipo=info_data["tipo"], cantidad=info_data["cantidad"], edad=info_data["edad"], unidad_medida=info_data["unidad_medida"],
                            fecha_entrega=info_data["fecha_entrega"], descripcion=info_data["descripcion"])
    session.add(new_aviso)
    session.commit()
    id_aviso=new_aviso.id
    session.close()
    return id_aviso

def create_foto(ruta_archivo, nombre_archivo, aviso_id):
    session = SessionLocal()
    new_foto = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, aviso_id=aviso_id)
    session.add(new_foto)
    session.commit()
    session.close()

def create_contactar_por(nombre, identificador, aviso_id):
    session = SessionLocal()
    new_foto = ContactarPor(nombre=nombre, identificador=identificador, aviso_id=aviso_id)
    session.add(new_foto)
    session.commit()
    session.close()