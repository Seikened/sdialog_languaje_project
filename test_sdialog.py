import sdialog
from sdialog import Context
from sdialog.agents import Agent
from sdialog.personas import Persona
from sdialog.orchestrators import SimpleReflexOrchestrator
from dotenv import load_dotenv


"""
llm:
  model: gemma3:27b
  temperature: null  # model's default
  seed: 13
  max_tokens: null
  top_p: null
  frequency_penalty: null
  presence_penalty: null
"""

# sdialog.config.llm("ollama:gemma3:1b", temperature=0.7)


load_dotenv()

print("Listo")
sdialog.config.llm("openai:gpt-4o-mini", temperature=0.9)
print("cargado")





paciente = Persona(
    name="Fernando Leon", 
    age=24,
    race="Latino",
    language="español",
    background="estudiante de ingeniería de intenligencia artificial en la universidad iberoamericana de 5to semestre, apasionado por la tecnología y los videojuegos",
    gender="masculino",
    role="paciente", 
    personality="curioso",
    rules="Habla solo en español",
    circumstances="Está en una sesión de terapia por primera vez y se siente un poco nervioso y tiene sintomas de depresión"
    )


psicologo   = Persona(
    name="Valeria", 
    age=30,
    race="Latina",
    language="español",
    background="psicóloga con 5 años de experiencia en terapia cognitivo-conductual",
    gender="femenino",
    role="psicóloga", 
    personality="curiosa empática",
    rules="Habla solo en español",
    circumstances="Está conduciendo una sesión de terapia con un nuevo paciente"
    )



contexto = Context(
  location="Consultorio de psicología",
  environment="silencioso, una luz suave entra por la ventana",
  circumstances="Sesión un viernes por la tarde noche",
  objects=["escritorio con laptop", "sillas cómodas", "cuadros relajantes en las paredes"]
)

def get_phq9_questions(item: str) -> dict:
    " Herramientas de psicología PHQ-9  y siempre debe ser escala del 0 al 3  siendo 0 nunca y 3 casi todos los días "
    list_preguntas=[
        "Durante las últimas 2 semanas, ¿qué tan seguido has tenido molestias debido a los siguientes problemas?",
        "Poco interés o placer en hacer cosas.",
        "Sentirte decaído(a), deprimido(a) o sin esperanzas.",
        "Tener dificultad para quedarte o permanecer dormido(a), o dormir demasiado.",
        "Sentirte cansado(a) o con poca energía.",
        "Tener poco apetito o comer en exceso.",
        "Sentirte mal contigo mismo(a) — o sentir que eres un fracaso o que has quedado mal contigo mismo(a) o con tu familia.",
        "Tener dificultad para concentrarte en cosas como leer el periódico o ver la televisión.",
        "Moverte o hablar tan lento que otras personas podrían notarlo, o lo contrario: sentirte tan inquieto(a) o agitado(a) que te mueves mucho más de lo normal.",
        "Pensamientos de que estarías mejor muerto(a) o de lastimarte de alguna manera."
    ]
    return {"item": item, "preguntas": list_preguntas}




depression_keywords = [
    "deprimido", "deprimida", "sin ganas", "ya no quiero nada",
    "triste", "no vale la pena", "cansado de todo", "vacío",
    "no quiero vivir", "me quiero morir", "sin esperanza",
    "agotado", "sin energía", "no puedo más", "me siento mal conmigo mismo",
    "fracaso", "no sirvo para nada", "me siento inútil"
]

def depression_condition(utt: str) -> bool:
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
    event_label="phq9_screening"
)



numero_de_sesiones = 1





for ix in range(numero_de_sesiones):
    primera_intervencion = f"Hola Fernando, Toma asiento por favor. ¿Cómo te sientes hoy al estar aquí? en esta que es nuestra sesión número {ix + 1}."
    fernando_paciente = Agent(persona=paciente)
    valeria_psicologo = Agent(persona=psicologo, first_utterance=primera_intervencion,) #tools=[get_phq9_questions])
    
    valeria_psicologo = valeria_psicologo | phq9_reflex
    dialog = valeria_psicologo.dialog_with(fernando_paciente, context=contexto,) #max_turns=40)
    dialog.print(orchestration=True)
    memoria = valeria_psicologo.memory_dump()
    print(memoria)
    dialog.to_file(f"dialog_{ix}.json")
    
    