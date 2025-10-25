from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, desc, select
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from .models import AvisoAdopcion, Comuna, Region, Foto, ContactarPor, Comentario


import datetime


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)


# --- Database Functions ---

# --- Get Data ---
def get_avisos(offset_value,page_size):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).order_by(desc(AvisoAdopcion.id))
    avisos_total=avisos.count()
    chosen_avisos=avisos.offset(offset_value).limit(page_size).all()
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

def get_count_fechas():
    session = SessionLocal()
    statement = select(AvisoAdopcion.fecha_ingreso)
    fechas = session.scalars(statement).all()
    session.close()
    date_min=min(fechas).date()
    diff_max_min=max(fechas).date()-date_min
    date_count = {str(date_min + datetime.timedelta(days=idx)):0 for idx in range(diff_max_min.days+1)}
    for date in fechas:
      fecha_str=str(date.date())
      date_count[fecha_str]+=1
    return date_count


def get_count_types():
    session = SessionLocal()
    tipos = session.query(AvisoAdopcion.tipo).all()
    session.close()
    tipo_count = {"gato":0,"perro":0}
    for tipo in tipos:
      tipo_count[tipo[0]]+=1
    return tipo_count

def get_count_types_by_month():
    session = SessionLocal()
    tipos_mes = session.query(AvisoAdopcion.tipo,AvisoAdopcion.fecha_ingreso).all()
    session.close()
    mes=[]
    for tipo_mes in tipos_mes:
      mes.append(tipo_mes[1])

    all_months=range_months(min(mes),max(mes))
    for tipo_mes in tipos_mes:
        all_months[tipo_mes[0]][tipo_mes[1].strftime("%Y-%m")]+=1
    return all_months

def get_comments_ad(aviso_id,offset_value,page_size):
    session = SessionLocal()
    
    comentarios = session.query(Comentario).filter_by(aviso_id=aviso_id).order_by(desc(Comentario.id))
    chosen_comentarios_total=comentarios.count()
    chosen_comentarios=comentarios.offset(offset_value).limit(page_size).all()
    #comentarios = session.query(Comentario).filter_by(aviso_id=aviso_id).all()
    session.close()
    return chosen_comentarios,chosen_comentarios_total

# --- Create data ---
def create_aviso(info_data):
    session = SessionLocal()
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

def create_comentario(nombre,texto,fecha,aviso_id):
    session = SessionLocal()
    comentario = Comentario(nombre=nombre, texto=texto, fecha=fecha, aviso_id=aviso_id)
    session.add(comentario)
    session.commit()
    session.close()


# --- Utils DB ---
def range_months(min_month,max_month):
    month_min=min_month.month
    year_min=min_month.year
    total_months=(max_month.year - year_min) * 12 + max_month.month - month_min
    range_month_year={}
    for i in range(total_months+1):
      month_year=(datetime.datetime(year_min+((month_min+i-1)//12),(month_min+i-1)%12+1,1)).strftime("%Y-%m")
      range_month_year[month_year]=0
    return {"gato":range_month_year,"perro":range_month_year.copy()}