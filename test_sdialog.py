from sdialog import Context
from sdialog.agents import Agent
from sdialog.personas import Persona
from sdialog.orchestrators import SimpleReflexOrchestrator
from .config import arrancar, DICT_MAJORS
import json

arrancar()


# TOOLS --------------------------------------------------------
def entry_incidents(path = "incidents.json"):
    "Abrir el .json de incidentes"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data



def trgger_tool(path="dialog_session_0.json",tool = "get_phq9_questions",    verbose=False):
    "Abrir el .json de la transcripción guardada de la sesión"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for evento in data["events"]:
        if evento["action"] == "tool" and evento["actionLabel"]=="call":
            if evento["content"]["name"]==tool:
                evento_f = json.dumps(evento, indent=2, ensure_ascii=True)
                if verbose:
                    print(f"Evento: {evento_f}")
                return evento_f
    return None







# PERSONAS --------------------------------------------------------

paciente = Persona(
    name="Fernando Leon", 
    age=24,
    race="Latino",
    language="español",
    background=(
        "estudiante de ingeniería de inteligencia artificial en la universidad iberoamericana "
        "de 5to semestre, apasionado por la tecnología y los videojuegos"
    ),
    gender="masculino",
    role="paciente", 
    personality="curioso",
    rules="Habla solo en español",
    circumstances=(
        "Está en una sesión de terapia por primera vez y se siente un poco nervioso "
        "y tiene síntomas de depresión"
    ),
)

psicologo = Persona(
    name="Valeria", 
    age=30,
    race="Latina",
    language="español",
    background="psicóloga con 5 años de experiencia en terapia cognitivo-conductual",
    gender="femenino",
    role="psicóloga", 
    personality="curiosa empática",
    rules="Habla solo en español",
    circumstances="Está conduciendo una sesión de terapia con un nuevo paciente",
)




# CONTEXTOS --------------------------------------------------------

contexto = Context(
  location="Consultorio de psicología",
  environment="silencioso, una luz suave entra por la ventana",
  circumstances="Sesión un viernes por la tarde noche",
  objects=["escritorio con laptop", "sillas cómodas", "cuadros relajantes en las paredes"],
)


# TOOLS --------------------------------------------------------

def get_phq9_questions(item: str) -> dict:
    """Herramienta PHQ-9; escala 0-3 (0 = nunca, 3 = casi todos los días)."""
    list_preguntas = [
        "1/10 | Durante las últimas 2 semanas, ¿qué tan seguido has tenido molestias debido a los siguientes problemas?",
        "2/10 | Poco interés o placer en hacer cosas.",
        "3/10 | Sentirte decaído(a), deprimido(a) o sin esperanzas.",
        "4/10 | Tener dificultad para quedarte o permanecer dormido(a), o dormir demasiado.",
        "5/10 | Sentirte cansado(a) o con poca energía.",
        "6/10 | Tener poco apetito o comer en exceso.",
        "7/10 | Sentirte mal contigo mismo(a) — o sentir que eres un fracaso o que has quedado mal contigo mismo(a) o con tu familia.",
        "8/10 | Tener dificultad para concentrarte en cosas como leer el periódico o ver la televisión.",
        "9/10 | Moverte o hablar tan lento que otras personas podrían notarlo, o lo contrario: sentirte tan inquieto(a) o agitado(a) que te mueves mucho más de lo normal.",
        "10/10 | Pensamientos de que estarías mejor muerto(a) o de lastimarte de alguna manera.",
    ]
    return {"item": item, "preguntas": list_preguntas}


def symmary_session(item: str) -> dict:
    """Resumen estructurado de la sesión de terapia (estructura base)."""
    return {
        "item": item,
        "summary": (
            "Resumen de la sesión de terapia con los puntos clave discutidos y las "
            "recomendaciones para el paciente en la siguiente sesión. También incluye "
            "un plan de acción para el seguimiento como notas propias del psicólogo."
        ),
    }


# REFLEX: DETECCIÓN DE DEPRESIÓN ----------------------------------

def depression_condition(utt: str) -> bool:
    depression_keywords = [
        "deprimido", "deprimida", "sin ganas", "ya no quiero nada",
        "triste", "no vale la pena", "cansado de todo", "vacío",
        "no quiero vivir", "me quiero morir", "sin esperanza",
        "agotado", "sin energía", "no puedo más", "me siento mal conmigo mismo",
        "fracaso", "no sirvo para nada", "me siento inútil",
    ]
    text = utt.lower()
    return any(word in text for word in depression_keywords)


phq9_reflex = SimpleReflexOrchestrator(
    condition=depression_condition,
    instruction=(
        "Has detectado posibles síntomas de depresión en lo que el paciente dijo. "
        "Explícale brevemente que existe un cuestionario llamado PHQ-9 que sirve para "
        "explorar cómo se ha sentido en las últimas dos semanas. "
        "Pregúntale si está de acuerdo en responderlo. "
        "Si acepta, usa la herramienta get_phq9_questions('phq9') para obtener la lista "
        "de preguntas y hazlas una por una, pidiéndole que responda con un número del 0 al 3, "
        "donde 0 es 'nunca' y 3 es 'casi todos los días'. "
        "Aclara que esto NO sustituye una evaluación profesional completa."
    ),
    persistent=False,
    event_label="phq9_screening",
)


# REFLEX: DETECCIÓN DE CIERRE DE SESIÓN Y RESUMEN -----------------

def summary_reflex_condition(utt: str) -> bool:
    ending_keywords = [
        "gracias por tu ayuda",
        "hemos terminado",
        "eso es todo por hoy",
        "nos vemos la próxima sesión",
        "nos vemos en la próxima sesión",
        "hasta luego",
        "¡hasta luego!",
        "¡hasta la próxima!",
        "adiós",
        "me despido",
        "terminamos aquí",
        "eso es todo",
        "gracias por todo",
        "muchas gracias por todo",
        "gracias por escucharme",
        "por hoy está bien",
        "creo que por hoy es suficiente",
        "podemos dejarlo hasta aquí",
        "lo dejamos hasta aquí",
        "nos vemos la próxima vez",
        "nos vemos en la siguiente sesión",
        "de nada",
    ]
    text = utt.lower()
    return any(phrase in text for phrase in ending_keywords)


summary_reflex = SimpleReflexOrchestrator(
    condition=summary_reflex_condition,
    instruction=(
        "La sesión de terapia acaba de concluir. "
        "1) Llama primero a la herramienta symmary_session('session_summary') para "
        "estructurar los puntos clave de la sesión. "
        "2) Después de recibir la salida de la herramienta, redacta un resumen clínico "
        "breve en texto natural, dirigido al psicólogo (no al paciente), incluyendo: "
        "motivo de consulta, síntomas principales, impresión general según las respuestas "
        "del PHQ-9, hipótesis clínicas iniciales y plan para la siguiente sesión. "
        "No inicies una nueva conversación con el paciente; solo cierra la sesión con este resumen."
    ),
    persistent=False,
    event_label="session_summary",
)


# LOOP DE SESIONES ------------------------------------------------

numero_de_sesiones = 1



for ix in range(numero_de_sesiones):
    primera_intervencion = (
        f"Hola Fernando, toma asiento por favor. ¿Cómo te sientes hoy al estar aquí "
        f"en esta que es nuestra sesión número {ix + 1}?"
    )

    fernando_paciente = Agent(persona=paciente)


    valeria_psicologo = Agent(
        persona=psicologo,
        first_utterance=primera_intervencion,
        tools=[get_phq9_questions, symmary_session],
    )

    # Encadenamos los reflex sobre Valeria
    valeria_psicologo = valeria_psicologo | phq9_reflex | summary_reflex

    # Un solo diálogo: Valeria ↔ Fernando
    dialog = valeria_psicologo.dialog_with(
        fernando_paciente,
        context=contexto,
    )
    dialog.print(orchestrator=True)


    dialog.to_file(f"dialog_session_{ix}.json", human_readable=True)
    


