from __mysql__db import *
from flask import request, session, redirect, render_template


#para obtener los datos del usuario/administrador que inicio sesion
def obtenerUsuarioXEmailPass(result,email,password):
    res=False
    sSql="""SELECT u.id, u.nombre, u.apellido, u.usuario, u.email, u.pass, u.id_tipo_usuario, t.tipo
    FROM usuario u 
    INNER JOIN tipo_usuario t ON u.id_tipo_usuario = t.id
    WHERE u.email=%s and u.pass=%s;"""
    val=(email,password)
    fila=selectDB(BASE,sSql,val)
    if fila!=[]:
        res=True
        result['id']=fila[0][0]
        result['nombre']=fila[0][1]
        result['apellido']=fila[0][2]
        result['usuario']=fila[0][3] 
        result['email']=fila[0][4]
        result['pass']=fila[0][5]
        result['id_tipo_usuario']=fila[0][6]
        result['tipo_usuario']=fila[0][7]
    return res


#para insertar en la tabla 'usuario' un nuevo registro
def insertarRegistro(dicDatos):
    """Inserta un nuevo usuario con tipo por defecto 1 (usuario común)."""

    sQuery = """ 
        INSERT INTO usuario
        (id, nombre, apellido, usuario, email, pass, id_tipo_usuario)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s);
    """

    # 1 = usuario común, 2 = admin (según tu tabla tipo_usuario)
    TIPO_USUARIO_COMUN = 1

    val = (
        None,
        dicDatos.get("nombre"),
        dicDatos.get("apellido"),
        dicDatos.get("usuario"),
        dicDatos.get("email"),
        dicDatos.get("pass"),
        TIPO_USUARIO_COMUN,
    )

    try:
                resul_insert = insertDB(BASE, sQuery, val)
    except:
                resul_insert = 0
    return resul_insert


#para insertar en la tabla 'noticias' un nuevo evento
def insertarNoticias(dicDatos):
   
  sQuery=""" 
    INSERT INTO noticias
    (id,id_usuario,id_categoria,fecha_hora,titulo,subtitulo,cuerpo,img,id_estado)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s);
  """

  val=(None,dicDatos.get("id_usuario"),dicDatos.get("id_categoria"), dicDatos.get("fecha_hora"), dicDatos.get("titulo"), dicDatos.get("subtitulo"), dicDatos.get("cuerpo"), dicDatos.get("img"), dicDatos.get("id_estado"))
  resul_insert=insertDB(BASE,sQuery,val)
  return resul_insert


#para obtener las noticias publicadas (id_estado=1) para mostrar en administración
def obtenerNoticiasPorID(param):
    sSql = """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE n.id_estado = 1
        ORDER BY n.fecha_hora DESC
    """
    
    noticias = selectDB(BASE, sSql)
    param['noticias'] = noticias if noticias else []


#para obtener los datos de una noticia específica
def obtenerDatosDeLasNoticias(request, param):
    from flask import request as flask_request
    
    noticia_id = flask_request.args.get('id')
    
    if noticia_id:
        sSql = """
            SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
            FROM noticias n 
            INNER JOIN categoria c ON n.id_categoria = c.id 
            INNER JOIN usuario u ON n.id_usuario = u.id 
            WHERE n.id = %s AND n.id_estado = 1
        """
        
        noticia = selectDB(BASE, sSql, (noticia_id,))
        param['noticia'] = noticia[0] if noticia else None
    else:
        param['noticia'] = None


def obtenerCategorias(param):
    sSql = "SELECT id, nombre FROM categoria ORDER BY id"
    categorias = selectDB(BASE, sSql)
    param['categorias'] = categorias if categorias else []


def obtenerNoticiasPendientes(param):
    sSql = """
        SELECT n.*, c.nombre as categoria_nombre, u.nombre as autor_nombre 
        FROM noticias n 
        INNER JOIN categoria c ON n.id_categoria = c.id 
        INNER JOIN usuario u ON n.id_usuario = u.id 
        WHERE n.id_estado = 2
        ORDER BY n.fecha_hora DESC
    """
    
    noticias_pendientes = selectDB(BASE, sSql)
    param['noticias_pendientes'] = noticias_pendientes if noticias_pendientes else []


def actualizarEstadoNoticia(noticia_id, nuevo_estado):
    try:
        sSql = "UPDATE noticias SET id_estado = %s WHERE id = %s"
        updateDB(BASE, sSql, (nuevo_estado, noticia_id))
        return True
    except:
        return False


# insertar un nuevo comentario
def insertarComentario(dicDatos):
    sQuery=""" 
        INSERT INTO comentario
        (id,id_usuario,id_noticia,fecha_hora,contenido,id_estado)
        VALUES
        (%s,%s,%s,%s,%s,%s);
    """

    val=(
        None,
        dicDatos.get("id_usuario"),
        dicDatos.get("id_noticia"),
        dicDatos.get("fecha_hora"),
        dicDatos.get("contenido"),
        dicDatos.get("id_estado")
    )
    return insertDB(BASE,sQuery,val)


# obtener comentarios publicados de una noticia
def obtenerComentariosPorNoticia(noticia_id, param):
    sSql = """
        SELECT c.id, c.contenido, c.fecha_hora, u.usuario
        FROM comentario c
        INNER JOIN usuario u ON c.id_usuario = u.id
        WHERE c.id_noticia = %s AND c.id_estado = 1
        ORDER BY c.fecha_hora DESC
    """
    comentarios = selectDB(BASE, sSql, (noticia_id,))
    param['comentarios'] = comentarios if comentarios else []


# borrar (eliminar físicamente) un comentario por id
def borrarComentarioPorId(comentario_id):
    try:
        sSql = "DELETE FROM comentario WHERE id = %s"
        updateDB(BASE, sSql, (comentario_id,))
        return True
    except:
        return False


def obtenerComentariosParaAdmin(param):
    sSql = """
        SELECT c.id, c.id_noticia, n.titulo, c.contenido, c.fecha_hora, u.usuario, c.id_estado
        FROM comentario c
        INNER JOIN usuario u ON c.id_usuario = u.id
        INNER JOIN noticias n ON c.id_noticia = n.id
        WHERE c.id_estado = 2
        ORDER BY c.id_noticia, c.fecha_hora DESC
    """
    comentarios = selectDB(BASE, sSql)
    param['comentarios_admin'] = comentarios if comentarios else []


def actualizarEstadoComentario(comentario_id, nuevo_estado):
    try:
        sSql = "UPDATE comentario SET id_estado = %s WHERE id = %s"
        updateDB(BASE, sSql, (nuevo_estado, comentario_id))
        return True
    except:
        return False


# borrar (eliminar físicamente) una noticia por id
def borrarNoticiaPorId(noticia_id):
    try:
        sSql = "DELETE FROM noticias WHERE id = %s"
        updateDB(BASE, sSql, (noticia_id,))
        return True
    except:
        return False

