import re
import filetype
import datetime
def validate_aviso(info_data):
  error_msg=[]
  if not validateText(info_data["region"],1,200,True):error_msg.append("Region")
  if not validateText(info_data["comuna"],1,200,True):error_msg.append("Comuna")
  if not validateText(info_data["sector"],0,100,False):error_msg.append("Sector")
  if not validateEmail(info_data["email"]):error_msg.append("Email")
  if not validateCelular(info_data["celular"]):error_msg.append("Celular")
  if not validateContacts(info_data["select_contactos"],info_data["contactos"]):error_msg.append("Contactos")
  if not validateText(info_data["tipo"],1,10,True):error_msg.append("Tipo")
  if not validateInt(info_data["cantidad"],1):error_msg.append("Cantidad")
  if not validateInt(info_data["edad"],1):error_msg.append("Edad")
  if not validateText(info_data["unidad_medida"],1,10,True):error_msg.append("Unidad de medida")
  if not validateFecha(info_data["fecha_ingreso"],info_data["fecha_entrega"]):error_msg.append("Fecha entrega")
  if not validateDescripcion(info_data["descripcion"]):error_msg.append("Descripción")
  if not validateFoto(info_data["fotos"][0],True):error_msg.append("Foto Obligatoria")
  if not validateFotos(info_data["fotos"][1:]):error_msg.append("Fotos Opcionales")



def validateText(value,min_size,max_size,required):
    largo=len(value)
    if (not required) and largo==0:
        return True 
    else:
        return value and largo <= max_size and largo >= min_size

def validateContacts(select_contactos,contactos):
    for i,select_contacto in enumerate(select_contactos):
        if not validateText(select_contacto,0,100,False) and not validateText(contactos[i],4,50,False):
            return False
    return True

def validateEmail(value):
    return "@" in value and "." in value


def validateCelular(phoneNumber):
    if (not phoneNumber): return True
    largo=len(phoneNumber)
    plus=phoneNumber[0] 
    return plus=="+" and "." in phoneNumber and largo>=8


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def validateInt(number,min_value):
    if (not is_number(number)):
        return False
    number_int=int(number)
    return number_int and min_value<=number_int



def is_date(date_text):
    try:
        datetime.datetime.fromisoformat(date_text)
        return True
    except ValueError:
        return False



def validateFecha(fecha_ingreso,fecha_entrega):
  if((not fecha_ingreso) or (not fecha_entrega)): return False
  if((not is_date(fecha_ingreso)) or (not is_date(fecha_entrega))): return False
  fecha_ingreso = datetime.datetime.fromisoformat(fecha_ingreso)
  fecha_entrega = datetime.datetime.fromisoformat(fecha_entrega)
  dif_time=fecha_entrega.hour-fecha_ingreso.hour
  return dif_time>=3

def validateDescripcion(descripcion):
  return True


def validateFotos(imgs):
    for img in imgs:
        if not validateFoto(img,False):
            return False
    return True

def validateFoto(conf_img,required):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if conf_img is None :
        if not required:
            return True
        return False

    # check if the browser submitted an empty file
    if conf_img.filename == "":
        if not required:
            return True
        return False
    
    # check file extension
    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True