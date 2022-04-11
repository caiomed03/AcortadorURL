from flask import Flask, redirect
import mysql.connector as mariadb

app = Flask(__name__)


@app.route("/start")
def start():
    resA = asignarIDRedireccion()
    return "localhost:5000/"+str(resA[0][0])


def asignarIDRedireccion():
    mariadb_conexion = mariadb.connect(host='localhost', port='3306',
                                       user='root', password='', database='acortadorurls')
    cursor = mariadb_conexion.cursor()
    paginaWeb = input("Inserte la url de la página: ")
    sqlInsertarRegistro = f"INSERT INTO urls (acortado, entera) VALUES ('', '{paginaWeb}')"
    sqlBusqueda = f"SELECT acortado FROM urls WHERE entera='{paginaWeb}'"
    # A partir del cursor, ejecutamos la consulta SQL de inserción
    cursor.execute(sqlInsertarRegistro)
    cursor.execute(sqlBusqueda)
    resA = cursor.fetchall()
    mariadb_conexion.commit()
    cursor.close()
    mariadb_conexion.close()
    return resA


@app.route("/<id>")
def expand_to_long_url(id):
    link_target = redireccion(id)
    return redirect(link_target)


def redireccion(id):
    mariadb_conexion = mariadb.connect(host='localhost', port='3306',
                                       user='root', password='', database='acortadorurls')
    cursor = mariadb_conexion.cursor()
    sqlInsertarRegistro = f"SELECT entera FROM urls WHERE acortado={id} ORDER BY acortado DESC LIMIT 1"
    cursor.execute(sqlInsertarRegistro)
    resultadoSQL = cursor.fetchall()
    mariadb_conexion.commit()
    cursor.close()
    mariadb_conexion.close()
    link_target = f"https:\\\\{str(resultadoSQL[0][0])}"
    return link_target


app.run()


