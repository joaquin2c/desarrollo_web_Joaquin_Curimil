from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from utils.validations import validate_aviso, validate_comment
from database import db, models
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import datetime
from PIL import Image
import math
import time

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)


app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/nuevoAviso", methods=["GET","POST"])
def post_aviso():
    
    if request.method == "POST":
        error = ""
        info_data={
            "fecha_ingreso":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "comuna": request.form.get("comuna"),
            "region": request.form.get("region"),
            "sector": request.form.get("sector"),
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "celular": request.form.get("celular"),
            "tipo": request.form.get("tipo"),
            "cantidad": request.form.get("cantidad"),
            "edad": request.form.get("edad"),
            "unidad_medida": request.form.get("unidad"),
            "fecha_entrega": request.form.get("fecha"),
            "descripcion": request.form.get("descripcion"),
            "fotos": [request.files.get(f"foto{i}") for i in range(1,6) ],
            "select_contactos": [request.form.get(f"select-contact{i}") for i in range(1,6) ],
            "contactos": [request.form.get(f"contact{i}") for i in range(1,6) ]
        }
        error=validate_aviso(info_data)
        if not error:
            save_in_db(info_data)# Coumna id desde el de comuna?
            time.sleep(5) 
            return redirect(url_for("index"))
        info_data["error"]=error
        return render_template("/avisos/nuevoAviso.html", data=info_data)
  
    elif request.method == "GET":
        info_data={}
        return render_template("/avisos/nuevoAviso.html",data=info_data)


def save_in_db(info_data):
    id_aviso=db.create_aviso(info_data)
    for image in info_data["fotos"]:
        if image.filename:
        # 1. generate random name for img
            _filename = hashlib.sha256(
                secure_filename(image.filename) # nombre del archivo
                .encode("utf-8") # encodear a bytes
                ).hexdigest()
            _extension = filetype.guess(image).extension
            img_filename = f"{_filename}.{_extension}"

            # 2. save img as a file

    
            path_med="./static/uploads/medium/"
            path_mini="./static/uploads/mini/"
            image_PIL = Image.open(image)
            image_PIL.resize((800,600)).save(os.path.join(app.config["UPLOAD_FOLDER"],"medium",img_filename))
            image_PIL.resize((320,240)).save(os.path.join(app.config["UPLOAD_FOLDER"],"mini",img_filename))
            # 3. save confession in db
            db.create_foto(app.config["UPLOAD_FOLDER"], img_filename, id_aviso)

    for i in range(5):
        if info_data["select_contactos"][i] and info_data["contactos"][i]:
            db.create_contactar_por(info_data["select_contactos"][i], info_data["contactos"][i], id_aviso)


@app.route("/", methods=["GET"])
def index():
    # get last avisos 
    data = []

    avisos,_=db.get_avisos(offset_value=0,page_size=5)
    for conf in avisos:
        #foto = db.get_fotos_by_user_id(conf.user_id)
        #img_filename = f"{foto.ruta_archivo}/{foto.nombre_archivo}"
        if conf.unidad_medida=="a":
            u_m="años"
        sing_plu = 1 if conf.edad >1  else 0
        u_m = ["año","años"] if conf.unidad_medida == "a" else ["mes","meses"]
        add_s="s" if conf.cantidad >1  else ""
        info_foto=db.get_fotos_by_user_id(conf.id)[0]
        comuna=db.get_comuna_by_id(conf.comuna_id)
        path_foto=os.path.join(info_foto.ruta_archivo,"mini",info_foto.nombre_archivo)
        data.append({
            "fecha_ingreso":conf.fecha_ingreso,
            "comuna":comuna.nombre,
            "sector":conf.sector,
            "cantidad":conf.cantidad,
            "tipo":conf.tipo+add_s,
            "edad":conf.edad,
            "unidad_medida":u_m[sing_plu],
            "path_img":path_foto,
        })
    return render_template("index.html", data=data)

@app.route("/listado/", methods=["GET"])
def listado():
    # get last avisos
    page_size=5
    page=request.args.get('page')
    if page:
        page_num=int(page)
    else:
        page_num=1
    data = []
    avisos,size_db=db.get_avisos(offset_value=page_size*(page_num-1),page_size=page_size)
    current_page=math.ceil(size_db/page_size)
    all_info={"size_db":current_page,"page_num":page_num}
    for conf in avisos:
        #foto = db.get_fotos_by_user_id(conf.user_id)
        #img_filename = f"{foto.ruta_archivo}/{foto.nombre_archivo}"
        sing_plu = 1 if conf.edad >1  else 0
        u_m = ["año","años"] if conf.unidad_medida == "a" else ["mes","meses"]
        add_s="s" if conf.cantidad >1  else ""
        info_foto=db.get_fotos_by_user_id(conf.id)[0]
        path_img_mini=os.path.join("/",info_foto.ruta_archivo,"mini",info_foto.nombre_archivo)
        
        comuna=db.get_comuna_by_id(conf.comuna_id)
        path_foto=os.path.join("/",info_foto.ruta_archivo,"mini",info_foto.nombre_archivo)
        data.append({
            "id":conf.id,
            "fecha_ingreso":conf.fecha_ingreso,
            "fecha_entrega":conf.fecha_entrega,
            "comuna":comuna.nombre,
            "sector":conf.sector,
            "cantidad":conf.cantidad,
            "tipo":conf.tipo+add_s,
            "edad":conf.edad,
            "unidad_medida":u_m[sing_plu],
            "nombre":conf.nombre,
            "path_img_mini":path_img_mini
        })
    all_info["data"]=data
    return render_template("listado.html", all_info=all_info)

@app.route('/listado/aviso/<int:id>')
def aviso(id):
    info=db.get_aviso_by_id(id)

    sing_plu = 1 if info.edad >1  else 0
    u_m = ["año","años"] if info.unidad_medida == "a" else ["mes","meses"]
    add_s="s" if info.cantidad >1  else ""

    info_fotos=db.get_fotos_by_user_id(info.id)
    contactos=db.get_contactos_by_user_id(info.id)
    total_fotos=len(info_fotos)
    nombre_archivo=info_fotos[0].nombre_archivo 
    ruta_archivo=info_fotos[0].ruta_archivo
    session['page'] = 1
    data_aviso={
        "id":info.id,
        "fecha_ingreso":info.fecha_ingreso,
        "fecha_entrega":info.fecha_entrega,
        "comuna":info.comuna.nombre,
        "sector":info.sector,
        "cantidad":info.cantidad,
        "tipo":info.tipo+add_s,
        "edad":info.edad,
        "unidad_medida":u_m[sing_plu],
        "nombre":info.nombre,
        "email":info.email,
        "celular":info.celular,
        "descripcion":info.descripcion,
        "contactos":contactos,
        "total_fotos":total_fotos,
        "ruta_archivo":ruta_archivo,
        "nombre_archivo":nombre_archivo
    } 
    return render_template('avisos/aviso.html', data_aviso=data_aviso)


@app.route('/listado/aviso/<int:id>/imgs')
def fotos(id):
    info_fotos = db.get_fotos_by_user_id(id)
    id_img = int(request.args.get('id'))
    if len(info_fotos)==0:
      return redirect(url_for("listado")) 
    elif len(info_fotos)<=id_img:
      return redirect(f"/listado/aviso/{id}/imgs?id=0")
    elif id_img<0:
      return redirect(f"/listado/aviso/{id}/imgs?id={len(info_fotos)-1}")

    nombre_archivo=info_fotos[id_img].nombre_archivo 
    ruta_archivo=info_fotos[id_img].ruta_archivo
    
    data_foto={
        "ruta_archivo":ruta_archivo,
        "nombre_archivo":nombre_archivo,
        "id_aviso":id,
        "cant_imgs":len(info_fotos),
        "id_img":id_img
    }

    return render_template('avisos/zoomImg.html', data_foto=data_foto)

@app.route("/get-comentarios/", methods=["GET"])
def get_comentarios():
    page_size=5
    id_user=request.args.get('id')
    page=request.args.get('page')
    page_num=int(page)

    comentarios,size_db=db.get_comments_ad(id_user,offset_value=page_size*(page_num-1),page_size=page_size)
    if not comentarios:
        return jsonify({"status": "ok", "data": []})
    current_page=math.ceil(size_db/page_size)
    all_info={"size_db":current_page,"page_num":page_num}
    data_comentarios=[]
    for comentario in comentarios:
        data_comentarios.append({
            "nombre":comentario.nombre,
            "texto":comentario.texto,
            "fecha":comentario.fecha.strftime("%H:%M %d-%m-%Y"),
        })
    all_info["comentarios"]=data_comentarios
    return jsonify({"status": "ok", "data": all_info})

@app.route("/get-fechas/", methods=["GET"])
def get_fechas():
    fechas=db.get_count_fechas()
    if not fechas:
        return jsonify({"status": "ok", "data": []})

    return jsonify({"status": "ok", "data": fechas})

@app.route("/get-tipos/", methods=["GET"])
def get_tipos():
    tipos=db.get_count_types()
    if not tipos:
        return jsonify({"status": "ok", "data": []})
    return jsonify({"status": "ok", "data": tipos})


@app.route("/get-tipos-mes/", methods=["GET"])
def get_tipos_month():
    tipos_month=db.get_count_types_by_month()
    if not tipos_month:
        return jsonify({"status": "ok", "data": []})
    return jsonify({"status": "ok", "data": tipos_month})

@app.route("/post-comentario/", methods=["POST"])
def post_comentario():
    comment_dict = request.get_json()
    name=comment_dict["name"]
    comment=comment_dict["comment"]
    aviso_id=comment_dict["aviso_id"]
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error=validate_comment(name,comment,aviso_id)
    if(error):
        return jsonify({"valid": 0,"error":error})
    else:
        db.create_comentario(name,comment,time,aviso_id)
        return jsonify({"valid": 1,"time":time})

@app.route('/estadistica', methods=["GET"])
def estadisticas():
    return render_template(f"estadistica.html")


if __name__ == "__main__":
    app.run(debug=True)