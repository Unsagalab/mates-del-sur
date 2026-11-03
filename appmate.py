from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def conectar_db():
    conexion = sqlite3.connect("mates.db")
    conexion.row_factory = sqlite3.Row
    return conexion


@app.route("/")
def inicio():
    return render_template("mate.html")


@app.route("/contacto", methods=["POST"])
def guardar_contacto():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    mensaje = request.form.get("mensaje")

    if not nombre or not email or not mensaje:
        return "Todos los campos son obligatorios", 400

    conexion = conectar_db()

    conexion.execute("""
        INSERT INTO contactos (
            nombre,
            email,
            mensaje
        )
        VALUES (?, ?, ?)
    """, (
        nombre,
        email,
        mensaje
    ))

    conexion.commit()
    conexion.close()

    return redirect(url_for("inicio"))


@app.route("/consultas")
def ver_consultas():
    conexion = conectar_db()

    contactos = conexion.execute("""
        SELECT *
        FROM contactos
        ORDER BY id DESC
    """).fetchall()

    conexion.close()

    return render_template(
        "consultas.html",
        contactos=contactos
    )


if __name__ == "__main__":
    app.run(debug=True)
