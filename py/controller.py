from flask import request, session,redirect,render_template
from datetime import datetime 
from model import *
from appConfig import config
import os
from uuid import uuid4

def getRequest(diResult):
    if request.method=='POST':
        for name in request.form.to_dict().keys():
            li=request.form.getlist(name)
            if len(li)>1:
                diResult[name]=request.form.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""
    elif request.method=='GET':  
        for name in request.args.to_dict().keys():
            li=request.args.getlist(name)
            if len(li)>1:
                diResult[name]=request.args.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""    

def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif','.jpeg']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            
            
            f = request.files[key] 
            if f.filename!="":     
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
 
                except:
                        pass
            else:
                diResult[key]={}


def cargarSesion(dicUsuario):
    session['id_usuario'] = dicUsuario['id']
    session['nombre']     = dicUsuario['nombre']
    session['apellido']   = dicUsuario['apellido']
    session['username']   = dicUsuario['usuario'] 
    session['mail']=dicUsuario['email']
    session['id_tipo_usuario']=dicUsuario['id_tipo_usuario']
    session['tipo_usuario']=dicUsuario['tipo_usuario']  

def crearSesion(request):
    sesionValida=False
    mirequest={}
    try: 
        getRequest(mirequest)
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("userid"),mirequest.get("userpassword")):
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def haySesion():  
    return session.get("username")!=None

def cerrarSesion():
    try:    
        session.clear()
    except:
        pass

def esAdministrador():
    return session.get("tipo_usuario") == "admin"


def ingresoUsuarioValido(param,request):
    if crearSesion(request):
        res=paginaPrincipal()
    else:
        
        res= render_template("login.html", errorVar="Usuario o contraseña incorrectos. Por favor, intentelo de nuevo")
    return res

def noticia(param):
    mireq = {}
    getRequest(mireq)

    noticia_id = mireq.get("id")

    if request.method == 'POST' and haySesion() and noticia_id:
        texto = mireq.get("comentario", "").strip()
        if texto != "":
            texto = texto[:300]
            dic = {
                "id_usuario": session.get("id_usuario"),
                "id_noticia": int(noticia_id),
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "contenido": texto,
                "id_estado": 1
            }
            insertarComentario(dic)
        return redirect(f"/noticia?id={noticia_id}")

    param['page-header'] = ""
    obtenerDatosDeLasNoticias(request, param)
    noticia = param.get('noticia')

    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    otras_noticias = []
    if noticia_id:
        sSql = """
            SELECT n.id, n.titulo
            FROM noticias n
            WHERE n.id_estado = 1 AND n.id <> %s
            ORDER BY n.fecha_hora DESC
        """
        otras_noticias = selectDB(BASE, sSql, (noticia_id,)) or []
    else:
        sSql = """
            SELECT n.id, n.titulo
            FROM noticias n
            WHERE n.id_estado = 1
            ORDER BY n.fecha_hora DESC
        """
        otras_noticias = selectDB(BASE, sSql) or []

    comentarios_param = {}
    if noticia_id:
        obtenerComentariosPorNoticia(int(noticia_id), comentarios_param)
    comentarios = comentarios_param.get('comentarios', [])

    return render_template(
        'noticia.html',
        noticia=noticia,
        otras_noticias=otras_noticias,
        comentarios=comentarios,
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )


def borrarComentario(request):
    if not haySesion() or not esAdministrador():
        return redirect('/login')

    mireq = {}
    getRequest(mireq)
    comentario_id = mireq.get("comentario_id")
    noticia_id = mireq.get("noticia_id")

    if comentario_id:
        try:
            borrarComentarioPorId(int(comentario_id))
        except:
            pass

    # Volver a la noticia de origen si tenemos el id
    if noticia_id:
        return redirect(f"/noticia?id={noticia_id}")
    return redirect('/')


def borrarNoticia(request):
    """Borra una noticia por id, solo si hay sesión de administrador."""
    if not haySesion() or not esAdministrador():
        return redirect('/login')

    mireq = {}
    getRequest(mireq)
    noticia_id = mireq.get("noticia_id")

    if noticia_id:
        try:
            borrarNoticiaPorId(int(noticia_id))
        except:
            pass

    # Después de borrar, volvemos a la home o a la lista de noticias admin
    return redirect('/')

def mostrarFormularioNuevaNoticia():
    if not haySesion():
        return redirect('/login')

    param = {}
    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "noticiaNueva.html",
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )


def subirNoticiaAlSistema(dicDatos, request):
    if not haySesion():
        return redirect('/login')

    mirequest = {}
    getRequest(mirequest)
    
    # Subida de imagen
    files_info = {}
    img_path = None
    try:
        upload_file(files_info)
        if "imagen" in files_info and not files_info["imagen"].get("file_error", False):
            img_path = "uploads/" + files_info["imagen"]["file_name_new"]
    except Exception:
        # Si hay error al subir la imagen, seguimos sin bloquear el alta de la noticia
        img_path = None

    # Construir diccionario para insertar en la tabla noticias
    dicDatos = {}
    dicDatos["id_usuario"] = session.get("id_usuario")
    dicDatos["id_categoria"] = int(mirequest.get("id_categoria")) if mirequest.get("id_categoria") else None
    dicDatos["fecha_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dicDatos["titulo"] = mirequest.get("titulo")
    dicDatos["subtitulo"] = mirequest.get("subtitulo")
    dicDatos["cuerpo"] = mirequest.get("cuerpo")
    dicDatos["img"] = img_path
    dicDatos["id_estado"] = 2  # 2 = pendiente de aprobación

    res = insertarNoticias(dicDatos)

    if res:
        mensaje = "Tu noticia fue enviada y quedará pendiente de aprobación por un administrador."
    else:
        mensaje = "Ocurrió un error al enviar tu noticia. Intentalo nuevamente."

    param = {}
    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "noticiaNueva.html",
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado,
        mensaje=mensaje
    )


def subirRegistroAlSistema(dicDatos,request):
    mirequest={}
    dicDatos={}
    getRequest(mirequest)
    dicDatos["nombre"]=mirequest.get("name")
    dicDatos["apellido"]=mirequest.get("surname")
    dicDatos["usuario"]=mirequest.get("userid")
    dicDatos["email"]=mirequest.get("usermail")
    dicDatos["pass"]=mirequest.get("userpassword")
    res = insertarRegistro(dicDatos)
    if res:
        # Preparar datos comunes para el header
        param = {}
        obtenerCategorias(param)
        categorias = param.get('categorias', [])
        es_admin = esAdministrador()
        usuario_logueado = haySesion()

        return render_template(
            "signup_success.html",
            categoria=categorias,
            es_admin=es_admin,
            usuario_logueado=usuario_logueado
        )

    # Registro fallido (por ejemplo mail/usuario duplicado)
    param = {}
    obtenerCategorias(param)
    categorias = param.get('categorias', [])
    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "signup.html",
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado,
        error="El mail o usuario ya existen"
    )


def paginaPrincipal():
    param = {}
    obtenerNoticiasPorID(param)   # todas las noticias publicadas
    obtenerCategorias(param)      # todas las categorías
    todas_noticias = param.get('noticias', [])
    categorias = param.get('categorias', [])

    ultimas_por_categoria = {}
    for n in todas_noticias:
        cat_id = n[2]
        if cat_id not in ultimas_por_categoria:
            ultimas_por_categoria[cat_id] = n

    ultimas = []
    for cat in categorias:
        cid = cat[0]
        if cid in ultimas_por_categoria:
            ultimas.append({
                'categoria': cat,
                'noticia': ultimas_por_categoria[cid]
            })

    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
    "home.html",
    ultimas=ultimas,
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )

def obtenerNoticiasPorCategoria(nombre_categoria, param):
    fila = selectDB(BASE, "SELECT id, nombre FROM categoria WHERE nombre = %s", (nombre_categoria,))
    if not fila:
        return redirect("/")

    categoria_id = fila[0][0]

    return obtenerNoticiasPorCategoriaID(categoria_id, param)

def obtenerNoticiaIndividual(req, param):
    mireq={}
    getRequest(mireq)
    noticia = selectDB(BASE, """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE n.id = %s AND n.id_estado = 1
    """, (mireq.get("id"),))
    
    if noticia:
        noticia = noticia[0]
    
    return render_template("noticiatemp.html", param=param, noticia=noticia)


def obtenerNoticiasPorCategoriaID(categoria_id, param):
    noticias = selectDB(BASE, """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE c.id = %s AND n.id_estado = 1
        ORDER BY n.fecha_hora DESC
    """, (categoria_id,))
    obtenerCategorias(param)
    categorias = param.get('categorias', [])

    categoria_actual = None
    for c in categorias:
        if c[0] == int(categoria_id):
            categoria_actual = c
            break

    es_admin = esAdministrador()
    usuario_logueado = haySesion()

    return render_template(
        "categoria.html",
        categoria_actual=categoria_actual,
        noticias=noticias,
        categoria=categorias,
        es_admin=es_admin,
        usuario_logueado=usuario_logueado
    )


def paginaAdminNoticias():
    if not haySesion() or not esAdministrador():
        return redirect('/login')
    
    param = {}
    obtenerNoticiasPendientes(param)
    noticias_pendientes = param.get('noticias_pendientes', [])
    
    return render_template("perfilAdm.html", 
                          noticias_pendientes=noticias_pendientes,
                          es_admin=True,
                          usuario_logueado=True)


def procesarCambioEstadoNoticia(request):
    if not haySesion() or not esAdministrador():
        return redirect('/login')
    
    mireq = {}
    getRequest(mireq)
    
    noticia_id = mireq.get("noticia_id")
    nuevo_estado = mireq.get("nuevo_estado")
    
    if noticia_id and nuevo_estado:
        if nuevo_estado == "publicado":
            estado_num = 1
        elif nuevo_estado == "no-publicado":
            estado_num = 2
        else:
            estado_num = 3
            
        if actualizarEstadoNoticia(noticia_id, estado_num):
            return redirect('/noticiasAdm?success=1')
        else:
            return redirect('/noticiasAdm?error=1')
    
    return redirect('/noticiasAdm')


def paginaAdminComentarios():
    if not haySesion() or not esAdministrador():
        return redirect('/login')
    param = {}
    obtenerComentariosParaAdmin(param)
    comentarios = param.get('comentarios_admin', [])
    return render_template("comentariosAdm.html",
                          comentarios=comentarios,
                          es_admin=True,
                          usuario_logueado=True)


def procesarCambioEstadoComentario(request):
    if not haySesion() or not esAdministrador():
        return redirect('/login')

    mireq = {}
    getRequest(mireq)

    comentario_id = mireq.get("comentario_id")
    nuevo_estado = mireq.get("nuevo_estado")

    if comentario_id and nuevo_estado:
        if nuevo_estado == "publicado":
            estado_num = 1
        else:
            estado_num = 2

        actualizarEstadoComentario(comentario_id, estado_num)

    return redirect('/comentariosAdm')