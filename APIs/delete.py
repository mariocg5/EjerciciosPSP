def verificar_bd():
    with app.app_context():
        try:
            # Intenta acceder a una de las nuevas columnas
            db.session.execute("SELECT intentos_fallidos FROM usuario LIMIT 1")
            print("✅ La base de datos ya tiene las columnas necesarias.")
        except Exception:
            print("⚠️ La base de datos no tiene las columnas correctas. Se recreará...")
            if os.path.exists("usuarios.db"):
                os.remove("usuarios.db")  # Elimina la base de datos
                print("❌ Base de datos eliminada.")

            db.create_all()  # Recrea la base de datos
            print("✅ Base de datos recreada con nuevas columnas.")


# 📌 Ejecutar la verificación antes de iniciar la aplicación
verificar_bd()
