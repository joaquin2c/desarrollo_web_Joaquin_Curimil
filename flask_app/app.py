from flask import Flask, request, render_template, redirect, url_for, session
from utils.validations import validate_login_user, validate_register_user, validate_confession
from database import db, models
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)


app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/post-aviso", methods=["POST"])
def post_aviso():

    fecha_ingreso = Column(DateTime, nullable=False)
    #comunda_id = Column(Integer, nullable=False)
    #comuna = request.form.get("comuna")
    sector = request.form.get("sector")
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    celular = request.form.get("celular")
    tipo = request.form.get("tipo")
    cantidad = request.form.get("cantidad")
    edad = request.form.get("edad")
    unidad_medida = request.form.get("unidad")
    fecha_entrega = request.form.get("fecha")
    descripcion = request.form.get("descripcion")

    fotos=[request.file.get(f"foto{i}") for i in range(1,6) ]
    select_contactos=[request.form.get(f"select-contact{i}") for i in range(1,6) ]
    contactos=[request.form.get(f"contact{i}") for i in range(1,6) ]

    if validate_aviso(comuna, sector,nombre,email,celular,tipo,cantidad,edad,unidad_medida,fecha_entrega,descripcion,fotos,contactos):
        
        # Coumna id desde el de comuna?
        fecha_ingreso=DateTime()  #Fecha en formato pedido
        id_aviso=db.create_aviso(fecha_ingreso,comuna, sector,nombre,email,celular,tipo,cantidad,edad,unidad_medida,fecha_entrega,descripcion)
        for image in fotos:
            # 1. generate random name for img
            _filename = hashlib.sha256(
                secure_filename(image.filename) # nombre del archivo
                .encode("utf-8") # encodear a bytes
                ).hexdigest()
            _extension = filetype.guess(image).extension
            img_filename = f"{_filename}.{_extension}"

            # 2. save img as a file
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

            # 3. save confession in db
            db.create_foto(app.config["UPLOAD_FOLDER"], img_filename, id_aviso)

        for i in range(5):
            db.create_contactar_por(select_contactos[i], contactos[i], id_aviso)
    return redirect(url_for("index"))

@app.route("/post-conf", methods=["POST"])
def post_conf():
    username = session.get("user", None)
    if username is None:
        return redirect(url_for("login"))

    conf_text = request.form.get("conf-text")
    conf_img = request.files.get("conf-img")

    if validate_confession(conf_text, conf_img):
        # 1. generate random name for img
        _filename = hashlib.sha256(
            secure_filename(conf_img.filename) # nombre del archivo
            .encode("utf-8") # encodear a bytes
            ).hexdigest()
        _extension = filetype.guess(conf_img).extension
        img_filename = f"{_filename}.{_extension}"

        # 2. save img as a file
        conf_img.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

        # 3. save confession in db
        user = db.get_user_by_username(username)
        db.create_confession(conf_text, img_filename, user.id)

    return redirect(url_for("index"))

@app.route("/", methods=["GET"])
def index():
    # get last avisos 
    data = []
    for conf in db.get_avisos(offset_value=0,page_size=5):
        #foto = db.get_fotos_by_user_id(conf.user_id)
        #img_filename = f"{foto.ruta_archivo}/{foto.nombre_archivo}"
        if conf.unidad_medida=="a":
            u_m="años"
        sing_plu = 1 if conf.edad >1  else 0
        u_m = ["año","años"] if conf.unidad_medida == "a" else ["mes","meses"]
        add_s="s" if conf.cantidad >1  else ""
        info_foto=db.get_fotos_by_user_id(conf.id)[0]
        path_foto=os.path.join(info_foto.ruta_archivo,"mini",info_foto.nombre_archivo)
        
        data.append({
            "fecha_ingreso":conf.fecha_ingreso,
            "comuna":conf.comuna.nombre,
            "sector":conf.sector,
            "cantidad":conf.cantidad,
            "tipo":conf.tipo+add_s,
            "edad":conf.edad,
            "unidad_medida":u_m[sing_plu],
            "path_img":path_foto,
        })
    return render_template("index.html", data=data)

@app.route("/listado.html", methods=["GET"])
def listado():
    # get last avisos 
    data = []
    for conf in db.get_avisos(offset_value=0,page_size=5):
        #foto = db.get_fotos_by_user_id(conf.user_id)
        #img_filename = f"{foto.ruta_archivo}/{foto.nombre_archivo}"
        sing_plu = 1 if conf.edad >1  else 0
        u_m = ["año","años"] if conf.unidad_medida == "a" else ["mes","meses"]
        add_s="s" if conf.cantidad >1  else ""
        info_foto=db.get_fotos_by_user_id(conf.id)[0]
        path_img_mini=os.path.join(info_foto.ruta_archivo,"mini",info_foto.nombre_archivo)
        
        data.append({
            "id":conf.id,
            "fecha_ingreso":conf.fecha_ingreso,
            "fecha_entrega":conf.fecha_entrega,
            "comuna":conf.comuna.nombre,
            "sector":conf.sector,
            "cantidad":conf.cantidad,
            "tipo":conf.tipo+add_s,
            "edad":conf.edad,
            "unidad_medida":u_m[sing_plu],
            "nombre":conf.nombre,
            "path_img_mini":path_img_mini,
        })
    return render_template("listado.html", data=data)

@app.route('/listado/<int:id>')
def aviso(id):
    info=db.get_aviso_by_id(id)

    sing_plu = 1 if info.edad >1  else 0
    u_m = ["año","años"] if info.unidad_medida == "a" else ["mes","meses"]
    add_s="s" if info.cantidad >1  else ""

    info_fotos=db.get_fotos_by_user_id(info.id)
    total_fotos=len(info_fotos)
    nombre_archivo=info_fotos[0].nombre_archivo 
    ruta_archivo=info_fotos[0].ruta_archivo

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
        "total_fotos":total_fotos,
        "ruta_archivo":ruta_archivo,
        "nombre_archivo":nombre_archivo
    }
    return render_template('aviso.html', data_aviso=data_aviso)


@app.route('/listado/<int:id>/imgs')
def fotos(id):
    info_fotos = db.get_fotos_by_user_id(id)
    id_img = int(request.args.get('id'))
    if len(info_fotos)==0:
      return redirect(url_for("listado")) 
    elif len(info_fotos)<=id_img:
      return redirect(f"/listado/{id}/imgs?id=0")

    nombre_archivo=info_fotos[id_img].nombre_archivo 
    ruta_archivo=info_fotos[id_img].ruta_archivo

    data_foto={
        "ruta_archivo":ruta_archivo,
        "nombre_archivo":nombre_archivo,
        "id_aviso":id
    }
    return render_template('zoomImg.html', data_foto=data_foto)

@app.route('/estadistica.html', methods=["GET"])
def estadisticas():
    return render_template(f"estadistica.html")

if __name__ == "__main__":
    app.run(debug=True)