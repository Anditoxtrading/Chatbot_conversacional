from flask import Flask, render_template, request, jsonify, session
import random
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'chat_motivacional_secret_key_2024'  # Necesario para sessions

# Sistema de memoria por sesión
conversacion_historial = {}

# Mensajes más naturales y variados con validación emocional
MENSAJES_MOTIVACIONALES = {
    'bienvenida': [
        {
            'respuesta': "¡Hola! 😊 Me da mucho gusto verte por aquí. Soy tu compañero de apoyo emocional.",
            'seguimiento': "Cuéntame, ¿cómo te sientes en este momento?"
        },
        {
            'respuesta': "¡Hey! 👋 Bienvenido/a. Estoy aquí para escucharte sin juzgar.",
            'seguimiento': "¿Qué tal ha estado tu día hasta ahora?"
        },
        {
            'respuesta': "Hola, qué bueno que estás aquí. Este es un espacio seguro para ti. 💙",
            'seguimiento': "¿Hay algo en particular que quieras compartir hoy?"
        },
    ],
    'tristeza': [
        {
            'validacion': "Lamento mucho que estés pasando por esto. 💙",
            'empatia': "Es completamente válido sentirse triste, no tienes que fingir estar bien.",
            'apoyo': "Las emociones difíciles son temporales, aunque en este momento no lo parezca.",
            'seguimiento': "¿Quieres contarme qué es lo que más te está afectando?"
        },
        {
            'validacion': "Entiendo que te sientas así, y está bien.",
            'empatia': "Los días oscuros existen, pero también existen para enseñarnos algo.",
            'apoyo': "Eres más fuerte de lo que crees, incluso en este momento de vulnerabilidad. 💪",
            'seguimiento': "¿Hay algo específico que te haya pasado hoy?"
        },
        {
            'validacion': "Te escucho y valido tu tristeza.",
            'empatia': "No estás solo/a en esto, aunque a veces así se sienta.",
            'apoyo': "Cada tormenta pasa, y esta también lo hará. 🌈",
            'seguimiento': "¿Te gustaría hablar sobre lo que sientes o prefieres algo que te anime?"
        },
    ],
    'ansiedad': [
        {
            'validacion': "Puedo sentir tu inquietud, y es totalmente comprensible.",
            'empatia': "La ansiedad puede ser abrumadora, pero estás dando un buen paso al reconocerla.",
            'apoyo': "Respira conmigo: inhala... exhala... Estás a salvo en este momento. 🌸",
            'seguimiento': "¿Hay algo específico que esté provocando esta ansiedad?"
        },
        {
            'validacion': "Entiendo lo difícil que es cuando la mente no para de pensar.",
            'empatia': "La ansiedad miente sobre muchas cosas. No todo lo que piensas es real.",
            'apoyo': "Toma las cosas paso a paso. No tienes que resolver todo ahora. 🦋",
            'seguimiento': "¿Qué es lo que más te preocupa en este momento?"
        },
        {
            'validacion': "Te comprendo, la ansiedad es muy real y difícil.",
            'empatia': "Tu cerebro está tratando de protegerte, pero a veces se excede.",
            'apoyo': "Estás haciendo lo mejor que puedes, y eso es más que suficiente. 💙",
            'seguimiento': "¿Te gustaría que te guíe en un ejercicio de respiración?"
        },
    ],
    'estres': [
        {
            'validacion': "Veo que estás llevando mucho peso en tus hombros.",
            'empatia': "El estrés es señal de que te importan las cosas, pero también necesitas cuidarte.",
            'apoyo': "No tienes que ser productivo/a todo el tiempo. Descansar también es progreso. 🌿",
            'seguimiento': "¿Es por trabajo, estudios, o algo más personal?"
        },
        {
            'validacion': "Comprendo que te sientas abrumado/a.",
            'empatia': "A veces queremos hacerlo todo perfecto, pero la perfección no existe.",
            'apoyo': "Prioriza lo importante, el resto puede esperar. Tú no puedes. 🎯",
            'seguimiento': "¿Qué es lo más urgente que te está estresando?"
        },
        {
            'validacion': "Entiendo que tengas mucha presión encima.",
            'empatia': "El autocuidado no es egoísta, es esencial para poder seguir adelante.",
            'apoyo': "Dale permiso a tu mente y cuerpo de descansar. Lo mereces. 🌙",
            'seguimiento': "¿Cuándo fue la última vez que hiciste algo solo para ti?"
        },
    ],
    'motivacion': [
        {
            'validacion': "Me encanta tu actitud de querer mejorar. 🚀",
            'empatia': "Buscar motivación ya es un acto de valentía en sí mismo.",
            'apoyo': "Tienes todo lo que necesitas dentro de ti. Solo necesitas creerlo.",
            'seguimiento': "¿Hay algún objetivo específico en el que estés trabajando?"
        },
        {
            'validacion': "Qué bueno que estés buscando ese impulso. ✨",
            'empatia': "Todos necesitamos un empujón de vez en cuando, es completamente normal.",
            'apoyo': "Cada pequeño paso cuenta. No subestimes tu progreso. 🌟",
            'seguimiento': "¿Qué es lo que quieres lograr?"
        },
        {
            'validacion': "Me gusta tu energía de querer avanzar. 💪",
            'empatia': "El simple hecho de buscar motivación significa que no te has rendido.",
            'apoyo': "Eres más capaz de lo que imaginas. Confía en tu proceso. 🦋",
            'seguimiento': "¿Hay algo que te esté frenando o solo necesitas ese recordatorio?"
        },
    ],
    'felicidad': [
        {
            'validacion': "¡Qué alegría escuchar eso! 😄",
            'empatia': "Me encanta cuando compartes tu felicidad, es contagiosa.",
            'apoyo': "Guarda este sentimiento, te servirá en los días difíciles. 💝",
            'seguimiento': "¿Qué fue lo que te puso de tan buen humor?"
        },
        {
            'validacion': "¡Eso es maravilloso! ☀️",
            'empatia': "Celebra cada momento de felicidad, te lo mereces.",
            'apoyo': "Sigue así, tu energía positiva ilumina. ✨",
            'seguimiento': "¿Quieres contarme qué te tiene tan contento/a?"
        },
        {
            'validacion': "¡Me alegro muchísimo por ti! 🎉",
            'empatia': "Tu felicidad importa y es válida, disfrútala plenamente.",
            'apoyo': "Esos momentos son los que hacen que todo valga la pena. 🌟",
            'seguimiento': "¿Hay alguien con quien quieras compartir esta alegría?"
        },
    ],
    'cansancio': [
        {
            'validacion': "Te escucho. El cansancio es real.",
            'empatia': "Tu cuerpo te está pidiendo descanso, y eso no es debilidad.",
            'apoyo': "Descansar no es rendirse, es recargarte para continuar. 😴",
            'seguimiento': "¿Has podido dormir bien últimamente?"
        },
        {
            'validacion': "Entiendo que te sientas agotado/a.",
            'empatia': "A veces el cansancio es emocional, no solo físico.",
            'apoyo': "Date permiso para descansar sin culpa. Lo necesitas. 🌙",
            'seguimiento': "¿Es cansancio físico o sientes que también es emocional?"
        },
    ],
    'confusion': [
        {
            'validacion': "Está bien no tener todas las respuestas.",
            'empatia': "La confusión es temporal, la claridad llegará.",
            'apoyo': "A veces perdernos nos lleva a mejores caminos. 🧭",
            'seguimiento': "¿Sobre qué te sientes confundido/a?"
        },
        {
            'validacion': "Comprendo esa sensación de no saber qué hacer.",
            'empatia': "No tener claridad inmediata no significa que estés haciendo algo mal.",
            'apoyo': "Confía en que encontrarás tu rumbo. 🗺️",
            'seguimiento': "¿Es sobre una decisión específica o sobre tu vida en general?"
        },
    ],
    'agradecimiento': [
        {
            'respuesta': "¡De nada! Es un placer poder acompañarte. 💙",
            'seguimiento': "Estaré aquí siempre que me necesites. ¿Hay algo más en lo que pueda ayudarte?"
        },
        {
            'respuesta': "Para eso estoy aquí, me alegra haberte ayudado. 😊",
            'seguimiento': "No dudes en volver cuando lo necesites. ¿Cómo te sientes ahora?"
        },
    ],
    'default': [
        {
            'respuesta': "Estoy aquí para escucharte sin juzgar.",
            'seguimiento': "Cuéntame más, ¿qué está pasando en tu mente?"
        },
        {
            'respuesta': "Te escucho. A veces solo necesitamos expresar lo que sentimos.",
            'seguimiento': "¿Hay algo específico que quieras compartir?"
        },
    ]
}

# Palabras clave mejoradas
PALABRAS_CLAVE = {
    'tristeza': ['triste', 'deprimido', 'solo', 'sola', 'mal', 'llorar', 'lloro', 'lloré', 'dolor', 'pena', 'melancolía', 'deprimente', 'horrible', 'fatal', 'destruido', 'roto'],
    'ansiedad': ['ansiedad', 'ansioso', 'ansiosa', 'nervioso', 'nerviosa', 'preocupado', 'preocupada', 'miedo', 'pánico', 'inquieto', 'inquieta', 'agobiado', 'agobiada', 'temor', 'aterrado'],
    'estres': ['estrés', 'estresado', 'estresada', 'agobiado', 'agobiada', 'presión', 'trabajo', 'abrumado', 'abrumada', 'sobrecargado', 'sobrecargada', 'colapso', 'saturado'],
    'felicidad': ['feliz', 'alegre', 'contento', 'contenta', 'bien', 'genial', 'excelente', 'maravilloso', 'increíble', 'emocionado', 'emocionada', 'fantástico', 'perfecto', 'súper'],
    'cansancio': ['cansado', 'cansada', 'agotado', 'agotada', 'exhausto', 'exhausta', 'fatiga', 'sueño', 'dormido', 'dormida', 'rendido'],
    'confusion': ['confundido', 'confundida', 'perdido', 'perdida', 'no sé', 'duda', 'indeciso', 'indecisa', 'desorientado', 'dudoso'],
    'motivacion': ['motivación', 'motivar', 'inspirar', 'objetivo', 'meta', 'logro', 'éxito', 'conseguir', 'alcanzar', 'progresar', 'crecer'],
    'agradecimiento': ['gracias', 'agradezco', 'agradecido', 'agradecida', 'thank', 'thanks'],
}

# Herramientas de bienestar
HERRAMIENTAS = {
    'respiracion': {
        'titulo': 'Ejercicio de Respiración 4-7-8',
        'intro': 'Perfecto, vamos a calmarnos juntos. 🧘',
        'descripcion': '1. Inhala profundamente por la nariz contando hasta 4\n2. Mantén el aire en tus pulmones contando hasta 7\n3. Exhala lentamente por la boca contando hasta 8\n4. Repite este ciclo 4 veces',
        'cierre': 'Tómate tu tiempo. Cuando termines, cuéntame cómo te sientes. 💙'
    },
    'afirmaciones': [
        'Soy capaz de superar cualquier desafío que se presente en mi camino',
        'Merezco amor, respeto y felicidad en todas las áreas de mi vida',
        'Cada día estoy creciendo y convirtiéndome en una mejor versión de mí mismo/a',
        'Confío plenamente en mi capacidad para tomar buenas decisiones',
        'Soy suficiente tal como soy, no necesito la aprobación de nadie más',
        'Mi pasado no define mi futuro, tengo el poder de cambiar',
        'Tengo el poder de crear cambios positivos en mi vida y en la de otros',
        'Acepto todas mis emociones y aprendo de cada una de ellas',
        'Soy resiliente y puedo adaptarme a cualquier situación',
        'Mi valor no depende de mi productividad, soy valioso/a por existir',
    ],
    'consejos': [
        '💧 Toma un vaso de agua ahora mismo - La hidratación afecta directamente tu estado de ánimo y concentración',
        '🚶 Sal a caminar 10-15 minutos sin teléfono - El movimiento libera endorfinas y el aire fresco aclara la mente',
        '📱 Desconéctate de redes sociales por 30 minutos - Tu mente necesita un respiro de la sobreestimulación',
        '🎵 Escucha tu canción favorita a todo volumen - La música tiene poder terapéutico comprobado',
        '📝 Escribe 3 cosas por las que estás agradecido/a hoy, por pequeñas que sean',
        '☀️ Busca luz natural, abre las cortinas o sal unos minutos - La vitamina D mejora el ánimo significativamente',
        '🤗 Llama o escribe a alguien que te importa - La conexión humana es sanadora',
        '🎨 Haz algo creativo sin juzgarte: dibuja, colorea, escribe, cocina - La creatividad es terapia',
        '🛁 Date una ducha o baño relajante - El agua tibia reduce el estrés físico y mental',
        '🍎 Come algo nutritivo - El cerebro necesita glucosa para funcionar bien emocionalmente',
    ]
}

def detectar_nombre(mensaje):
    """Detecta si el usuario menciona su nombre"""
    patrones = [
        r'me llamo (\w+)',
        r'mi nombre es (\w+)',
        r'soy (\w+)',
        r'mi nombre: (\w+)',
        r'llamo (\w+)',
        r'^(\w+)$',  # Si solo escribe una palabra (probablemente su nombre)
    ]
    for patron in patrones:
        match = re.search(patron, mensaje.lower())
        if match:
            nombre = match.group(1).capitalize()
            # Filtrar palabras comunes que no son nombres
            palabras_excluir = ['hola', 'hey', 'bien', 'mal', 'si', 'no', 'ok', 'vale', 'gracias', 'ayuda']
            if nombre.lower() not in palabras_excluir:
                return nombre
    return None

def detectar_emocion(mensaje):
    """Detecta la emoción predominante en el mensaje del usuario"""
    mensaje_lower = mensaje.lower()

    # Saludos iniciales
    if any(saludo in mensaje_lower for saludo in ['hola', 'buenos', 'buenas', 'hey', 'saludos', 'qué tal']):
        return 'bienvenida'

    # Contar coincidencias por categoría
    coincidencias = {}
    for emocion, palabras in PALABRAS_CLAVE.items():
        count = sum(1 for palabra in palabras if palabra in mensaje_lower)
        if count > 0:
            coincidencias[emocion] = count

    # Devolver la emoción con más coincidencias
    if coincidencias:
        return max(coincidencias, key=coincidencias.get)

    return 'default'

def generar_respuesta_natural(mensaje, emocion, session_id):
    """Genera una respuesta natural y contextual"""

    # Obtener o crear historial de conversación
    if session_id not in conversacion_historial:
        conversacion_historial[session_id] = {
            'mensajes': [],
            'emociones_previas': [],
            'nombre': None,
            'contador_mensajes': 0
        }

    historial = conversacion_historial[session_id]
    historial['mensajes'].append(mensaje)
    historial['emociones_previas'].append(emocion)
    historial['contador_mensajes'] += 1

    # Detectar nombre si es mencionado
    nombre_detectado = detectar_nombre(mensaje)
    nombre_recien_detectado = False
    if nombre_detectado and not historial['nombre']:
        # Primera vez que detectamos el nombre
        historial['nombre'] = nombre_detectado
        nombre_recien_detectado = True
    elif nombre_detectado:
        historial['nombre'] = nombre_detectado

    # Si acabamos de detectar el nombre, dar respuesta especial de bienvenida
    if nombre_recien_detectado:
        respuestas_nombre = [
            f"¡{historial['nombre']}! Qué nombre tan bonito. 😊 Es un placer conocerte.",
            f"Encantado de conocerte, {historial['nombre']}. 💙 Me gusta tu nombre.",
            f"¡Hola {historial['nombre']}! Me alegra mucho conocerte. 🌟",
            f"{historial['nombre']}, es un gusto tenerte aquí. 😊",
        ]
        respuesta_base = random.choice(respuestas_nombre)

        # Agregar pregunta de seguimiento
        seguimientos = [
            f"\n\n{historial['nombre']}, ¿cómo te sientes hoy?",
            f"\n\nCuéntame {historial['nombre']}, ¿qué tal ha estado tu día?",
            f"\n\n¿Hay algo en tu mente hoy, {historial['nombre']}?",
            f"\n\nDime {historial['nombre']}, ¿cómo puedo apoyarte hoy?",
        ]
        return respuesta_base + random.choice(seguimientos)

    # Seleccionar mensaje base
    mensajes_emocion = MENSAJES_MOTIVACIONALES.get(emocion, MENSAJES_MOTIVACIONALES['default'])
    mensaje_seleccionado = random.choice(mensajes_emocion)

    # Construir respuesta natural
    partes_respuesta = []

    # Usar nombre si lo tenemos
    saludo_personal = ""
    if historial['nombre'] and historial['contador_mensajes'] > 1:
        if random.random() > 0.7:  # 30% del tiempo usa el nombre
            saludo_personal = f"{historial['nombre']}, "

    # Si es un mensaje con validación, empatía, apoyo (estructura completa)
    if 'validacion' in mensaje_seleccionado:
        if saludo_personal:
            partes_respuesta.append(saludo_personal + mensaje_seleccionado['validacion'].lower())
        else:
            partes_respuesta.append(mensaje_seleccionado['validacion'])

        partes_respuesta.append(mensaje_seleccionado['empatia'])
        partes_respuesta.append(mensaje_seleccionado['apoyo'])

        # Agregar contexto si hay emociones previas
        if len(historial['emociones_previas']) > 2:
            emocion_anterior = historial['emociones_previas'][-2]
            if emocion_anterior != emocion and emocion_anterior in ['tristeza', 'ansiedad', 'estres']:
                partes_respuesta.append(f"\n\nHe notado que has estado pasando por momentos difíciles. Quiero que sepas que está bien sentir todo esto.")

        partes_respuesta.append("\n\n" + mensaje_seleccionado['seguimiento'])

        respuesta_final = "\n\n".join(partes_respuesta)
    else:
        # Mensaje simple (bienvenida, agradecimiento, default)
        if saludo_personal:
            respuesta_final = saludo_personal + mensaje_seleccionado['respuesta'].lower()
        else:
            respuesta_final = mensaje_seleccionado['respuesta']

        if 'seguimiento' in mensaje_seleccionado:
            respuesta_final += "\n\n" + mensaje_seleccionado['seguimiento']

    # Sugerencias adicionales contextuales
    if emocion == 'ansiedad' and 'respiración' not in mensaje.lower():
        respuesta_final += "\n\n💙 Tip: Si quieres, puedo guiarte en un ejercicio de respiración. Solo escribe 'respiración'."
    elif emocion == 'tristeza' and historial['contador_mensajes'] > 2:
        respuesta_final += "\n\n✨ ¿Te gustaría una afirmación positiva? Escribe 'afirmación'."
    elif emocion == 'estres':
        respuesta_final += "\n\n🌿 Tengo consejos prácticos de bienestar si los necesitas. Escribe 'consejo'."

    return respuesta_final

def procesar_comandos(mensaje, session_id):
    """Procesa comandos especiales con respuestas más personales"""
    mensaje_lower = mensaje.lower()

    historial = conversacion_historial.get(session_id, {})
    nombre = historial.get('nombre', '')
    saludo = f"{nombre}, " if nombre else ""

    if 'respiración' in mensaje_lower or 'respiracion' in mensaje_lower or 'respira' in mensaje_lower:
        herramienta = HERRAMIENTAS['respiracion']
        respuesta = f"{saludo}{herramienta['intro']}\n\n"
        respuesta += f"🧘 **{herramienta['titulo']}**\n\n"
        respuesta += f"{herramienta['descripcion']}\n\n"
        respuesta += herramienta['cierre']
        return respuesta

    if 'afirmación' in mensaje_lower or 'afirmacion' in mensaje_lower:
        afirmacion = random.choice(HERRAMIENTAS['afirmaciones'])
        respuesta = f"{saludo}esta afirmación es especialmente para ti:\n\n"
        respuesta += f"✨ **\"{afirmacion}\"**\n\n"
        respuesta += "Repítela en voz alta. Siéntela. Créela. Es tuya. 💫\n\n"
        respuesta += "¿Cómo resuena esto contigo?"
        return respuesta

    if 'consejo' in mensaje_lower:
        consejo = random.choice(HERRAMIENTAS['consejos'])
        respuesta = f"{saludo}aquí va un consejo que puede ayudarte:\n\n"
        respuesta += f"💡 {consejo}\n\n"
        respuesta += "¿Qué te parece? ¿Es algo que puedas hacer ahora? 😊"
        return respuesta

    if 'ayuda' in mensaje_lower or 'help' in mensaje_lower or 'qué puedes hacer' in mensaje_lower:
        respuesta = f"{saludo}estoy aquí para apoyarte de muchas formas:\n\n"
        respuesta += "💬 **Puedo:**\n"
        respuesta += "• Escucharte sin juzgar y validar tus emociones\n"
        respuesta += "• Darte apoyo emocional personalizado\n"
        respuesta += "• Guiarte en ejercicios de respiración (escribe 'respiración')\n"
        respuesta += "• Compartir afirmaciones positivas (escribe 'afirmación')\n"
        respuesta += "• Darte consejos prácticos de bienestar (escribe 'consejo')\n"
        respuesta += "• Recordar tu nombre y el contexto de nuestra conversación\n\n"
        respuesta += "Solo háblame con confianza. Estoy aquí para ti. 💙"
        return respuesta

    return None

@app.route('/')
def index():
    # Generar ID de sesión único
    if 'session_id' not in session:
        import uuid
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensaje_usuario = data.get('mensaje', '')

        # Obtener session ID
        if 'session_id' not in session:
            import uuid
            session['session_id'] = str(uuid.uuid4())

        session_id = session['session_id']

        if not mensaje_usuario:
            return jsonify({'error': 'No se recibió mensaje'}), 400

        # Primero verificar si es un comando especial
        respuesta_comando = procesar_comandos(mensaje_usuario, session_id)
        if respuesta_comando:
            return jsonify({
                'respuesta': respuesta_comando,
                'emocion': 'herramienta',
                'timestamp': datetime.now().strftime('%H:%M')
            })

        # Detectar emoción y generar respuesta contextual
        emocion_detectada = detectar_emocion(mensaje_usuario)
        respuesta = generar_respuesta_natural(mensaje_usuario, emocion_detectada, session_id)

        return jsonify({
            'respuesta': respuesta,
            'emocion': emocion_detectada,
            'timestamp': datetime.now().strftime('%H:%M')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
