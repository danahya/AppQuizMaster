import sqlite3

# Crear la conexión a la base de datos SQLite
conn = sqlite3.connect('AppQuizMaster.db')
cursor = conn.cursor()


# Crear tablas para el modelo relacional
def crear_tablas():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        IdUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
        NombreUsuario TEXT NOT NULL,
        CorreoElectronico TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pregunta (
        IdPregunta INTEGER PRIMARY KEY AUTOINCREMENT,
        TextoPregunta TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Respuesta (
        IdRespuesta INTEGER PRIMARY KEY AUTOINCREMENT,
        TextoRespuesta TEXT NOT NULL,
        EsCorrecta BOOLEAN NOT NULL,
        IdPregunta INTEGER,
        FOREIGN KEY(IdPregunta) REFERENCES Pregunta(IdPregunta)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Quiz (
        IdQuiz INTEGER PRIMARY KEY AUTOINCREMENT,
        NombreQuiz TEXT NOT NULL,
        DescripcionQuiz TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS QuizPregunta (
        IdQuiz INTEGER,
        IdPregunta INTEGER,
        PRIMARY KEY (IdQuiz, IdPregunta),
        FOREIGN KEY(IdQuiz) REFERENCES Quiz(IdQuiz),
        FOREIGN KEY(IdPregunta) REFERENCES Pregunta(IdPregunta)
    )
    ''')

    conn.commit()
    print("Tablas creadas con éxito.")


# Insertar un usuario
def insertar_usuario(nombre, correo):
    cursor.execute('''
    INSERT INTO Usuario (NombreUsuario, CorreoElectronico)
    VALUES (?, ?)''', (nombre, correo))
    conn.commit()


# Insertar una pregunta
def insertar_pregunta(texto):
    cursor.execute('''
    INSERT INTO Pregunta (TextoPregunta)
    VALUES (?)''', (texto,))
    conn.commit()


# Insertar una respuesta para una pregunta
def insertar_respuesta(texto, es_correcta, id_pregunta):
    cursor.execute('''
    INSERT INTO Respuesta (TextoRespuesta, EsCorrecta, IdPregunta)
    VALUES (?, ?, ?)''', (texto, es_correcta, id_pregunta))
    conn.commit()


# Insertar un quiz
def insertar_quiz(nombre, descripcion):
    cursor.execute('''
    INSERT INTO Quiz (NombreQuiz, DescripcionQuiz)
    VALUES (?, ?)''', (nombre, descripcion))
    conn.commit()


# Vincular pregunta con quiz
def vincular_pregunta_quiz(id_quiz, id_pregunta):
    cursor.execute('''
    INSERT INTO QuizPregunta (IdQuiz, IdPregunta)
    VALUES (?, ?)''', (id_quiz, id_pregunta))
    conn.commit()


# Función para obtener las preguntas de un quiz
def obtener_preguntas_quiz(id_quiz):
    cursor.execute('''
    SELECT P.IdPregunta, P.TextoPregunta
    FROM Pregunta P
    JOIN QuizPregunta QP ON P.IdPregunta = QP.IdPregunta
    WHERE QP.IdQuiz = ?
    ''', (id_quiz,))
    return cursor.fetchall()


# Función para obtener las respuestas de una pregunta
def obtener_respuestas_pregunta(id_pregunta):
    cursor.execute('''
    SELECT IdRespuesta, TextoRespuesta, EsCorrecta
    FROM Respuesta
    WHERE IdPregunta = ?
    ''', (id_pregunta,))
    return cursor.fetchall()


# Función para realizar el quiz interactivo
def realizar_quiz(id_quiz):
    preguntas = obtener_preguntas_quiz(id_quiz)
    puntuacion = 0
    total_preguntas = len(preguntas)

    for pregunta in preguntas:
        print("\nPregunta:", pregunta[1])  # Mostrar la pregunta
        respuestas = obtener_respuestas_pregunta(pregunta[0])

        for idx, respuesta in enumerate(respuestas):
            print(f"{idx + 1}. {respuesta[1]}")  # Mostrar las opciones de respuesta

        respuesta_usuario = input("Tu respuesta (elige el número de opción): ")

        try:
            respuesta_elegida = respuestas[int(respuesta_usuario) - 1]
            if respuesta_elegida[2]:  # Verificar si la respuesta es correcta
                print("¡Correcto!")
                puntuacion += 1
            else:
                print("Incorrecto.")
        except (IndexError, ValueError):
            print("Opción inválida.")

    print(f"\nHas terminado el quiz. Puntuación: {puntuacion}/{total_preguntas}")


# Crear las tablas
crear_tablas()

# Inserciones de ejemplo
insertar_usuario("Pedro", "pedro@example.com")
insertar_pregunta("¿Cuál es el planeta más cercano al sol?")
insertar_respuesta("Mercurio", True, 1)
insertar_respuesta("Venus", False, 1)
insertar_quiz("Astronomía", "Preguntas sobre el sistema solar")
vincular_pregunta_quiz(1, 1)

# Realizar el quiz interactivo
realizar_quiz(1)

# Cerrar la conexión
conn.close()