#route es el modulo que intercambia la información tomando los request y dando las responses
#tiene internamente las rutas que escribe el cliente en la url del navegador

from __mysql__db import * #importo las funciones que interaccionan con la base de datos
from controller import * #importo las funciones que cree en controller
from flask import render_template
#para renderizar las plantillas con jinja y crear paginas dinamicas
from flask import Flask,redirect, request, session  
from appConfig import config
import os

error = ""

def Route(aplicacion=Flask):

    @aplicacion.route("/GuardarDatosPerfil", methods=["POST"])
    def DeterminarValidez():
        ''' Info: 
          Recepciona la solicitud request que es enviada
          desde el formulario de login 
          retorna la pagina home en caso de exito 
          o la pagina login en caso de fracaso
        '''
        param={}
        return ingresoUsuarioValido(param,request)
    


    #para hacer disponible la variable usuario en todas las plantillas de manera automática
    @aplicacion.context_processor
    def inject_user():
        if session.get('username')!=None :
            return dict(usuario=session.get('username'))
        else:
            return dict(usuario="")

        

    @aplicacion.route("/logout")
    def logout():  
        ''' Info: 
          Cierra la sesión.
          retorna la redirección a la pagina home
        ''' 
        cerrarSesion()     
        return redirect('/')
    
    @aplicacion.route("/noticiasAdm")
    def noticias_admin():
        ''' Página de administración de noticias '''
        return paginaAdminNoticias()
    
    @aplicacion.route("/cambiar_estado_noticia", methods=["POST"])
    def cambiar_estado_noticia():
        ''' Procesa el cambio de estado de una noticia '''
        return procesarCambioEstadoNoticia(request)
    
    @aplicacion.route("/comentariosAdm")
    def comentarios_admin():
        return paginaAdminComentarios()


    @aplicacion.route("/cambiar_estado_comentario", methods=["POST"])
    def cambiar_estado_comentario():
        return procesarCambioEstadoComentario(request)
    
    @aplicacion.route("/borrar_noticia", methods=["POST"])
    def borrar_noticia_route():
        return borrarNoticia(request)
    


    @aplicacion.route("/")    
    @aplicacion.route("/home")
    def indice():
        return paginaPrincipal()


    @aplicacion.route('/login')
    def login():
        # Preparar datos comunes para el header
        param = {}
        obtenerCategorias(param)
        categorias = param.get('categorias', [])
        es_admin = esAdministrador()
        usuario_logueado = haySesion()

        return render_template(
            'login.html',
            categoria=categorias,
            es_admin=es_admin,
            usuario_logueado=usuario_logueado
        )
    @aplicacion.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            param = {}
            return subirRegistroAlSistema(param, request)

        # Preparar datos comunes para el header (GET)
        param = {}
        obtenerCategorias(param)
        categorias = param.get('categorias', [])
        es_admin = esAdministrador()
        usuario_logueado = haySesion()

        return render_template(
            'signup.html',
            categoria=categorias,
            es_admin=es_admin,
            usuario_logueado=usuario_logueado
        )
  
    @aplicacion.route("/noticia", methods=["GET","POST"])
    def noticia_route():
        param = {}
        # Usar la función de controller que arma noticia + otras_noticias + header y comentarios
        return noticia(param)

    @aplicacion.route("/nueva_noticia", methods=["GET", "POST"])
    def nueva_noticia():
        if request.method == "POST":
            param = {}
            return subirNoticiaAlSistema(param, request)

        return mostrarFormularioNuevaNoticia()
    

    
    @aplicacion.route("/checkout")
    def checkout():
        return render_template("checkout.html")
    
    
    @aplicacion.route("/economia")
    def economia():
        param = {}
        return obtenerNoticiasPorCategoria("Economía", param)
    
    
    @aplicacion.route("/deportes")
    def deportes():
        param = {}
        return obtenerNoticiasPorCategoria("Deportes", param)
    
    
    @aplicacion.route("/policiales")
    def policiales():
        param = {}
        return obtenerNoticiasPorCategoria("Policiales", param)
    
    
    @aplicacion.route("/politica")
    def politica():
        param = {}
        return obtenerNoticiasPorCategoria("Política", param)
    
    
    @aplicacion.route("/sociedad")
    def sociedad():
        param = {}
        return obtenerNoticiasPorCategoria("Sociedad", param)
    
    
    @aplicacion.route("/tecnologia")
    def tecnologia():
        param = {}
        return obtenerNoticiasPorCategoria("Tecnología", param)