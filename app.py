from datetime import datetime
from sqlite3 import connect
from flask import Flask, redirect , render_template, request, url_for, flash,url_for
from flask_mysqldb import MySQL
import os
from flask import send_from_directory

app= Flask(__name__)
app.secret_key = 'many random bytes'

#inicio: coneccion
app.config['MYSQL_HOST'] = 'sql10.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql10523549'
app.config['MYSQL_PASSWORD'] = 'bmk23Xvsk7'
app.config['MYSQL_DB'] = 'sql10523549'

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#Mostrar imagnes en la vista
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

mysql =MySQL(app)
@app.route('/')
def iniciar():
    cursor =mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos')
    data = cursor.fetchall()
    cursor.close()
    return render_template('products/product_list.html', productos=data)

##INICIO: EMPLEADO
@app.route('/empleado')
def mostrarEmpleados():
    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM empleado')
    data = cursor.fetchall()
    cursor.close()
    print(f'hay empleados:{len(data)}')
    return render_template('employes/employe_list.html',empleados=data)

@app.route('/form')
def mostrarFormEmploye():
    return render_template('employes/employe_form.html')

@app.route('/nuevoEmpleado', methods=['POST'])
def insertarEmpleado():
    if request.method=="POST":
        
        flash("Empleado insertado exitosamente")
        _dni= request.form['dni']
        _nombre=request.form['nombre']
        _correo=request.form['email']
        _foto= request.files['foto']
        now= datetime.now()
        tiempo=now.strftime("%Y%H%M%S")
        if _foto.filename != '':
            nuevoNombreFoto = tiempo +_foto.filename
            _foto.save("uploads/"+nuevoNombreFoto)

        datos= (_dni,_nombre,_correo, nuevoNombreFoto)
        sql = "INSERT INTO `ventas`.`empleado`(`DNI`,`NOMBRE`,`CORREO`,`FOTO`)VALUES(%s, %s, %s, %s)"
        cursor= mysql.connection.cursor()
        cursor.execute(sql, datos)
        mysql.connection.commit()
        return redirect('/empleado')

@app.route('/eliminarEmpleado/<string:dni>', methods=['GET'])
def eliminarEmpleado(dni):
    flash('Se elimino exitosamente el registro')
    cursor=mysql.connection.cursor()
    cursor.execute("DELETE FROM empleado  WHERE DNI = %s", (dni,))
    mysql.connection.commit()
    return redirect('/empleado')

@app.route('/actualizarEmpleado' , methods=['POST'])
def actualizarEmpleado():
    if request.method=='POST':
        dni= request.form['dni']
        nombre=request.form['nombre']
        correo=request.form['email']
        foto=request.files['foto']
        cursor= mysql.connection.cursor()
        now= datetime.now()
        tiempo=now.strftime("%Y%H%M%S")
        if foto.filename != '':
            nuevoNombreFoto = tiempo +foto.filename
            foto.save("uploads/{}".format(nuevoNombreFoto))
            cursor.execute('SELECT foto FROM empleado WHERE dni={}'.format(dni))
            fila =cursor.fetchall()
            os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
            cursor.execute('UPDATE empleado SET foto=%s WHERE dni=%s',(nuevoNombreFoto,dni))
            mysql.connection.commit()
        cursor.execute("UPDATE empleado SET  nombre=%s, correo=%s  WHERE dni=%s",(nombre,correo,dni))
        mysql.connection.commit()
        flash('Datos actualizados correctamente')
        return redirect('/empleado')
##FIN: EMPLEADO
##INICIO: PRODUCTOS




if __name__ == '__main__':
    app.run(debug=True)

# DESDE LA TERMINAL

## EJECUTAR
# pip install flask_mysqldb
# 
# 
# ##