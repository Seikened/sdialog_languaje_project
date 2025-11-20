import sdialog
from sdialog import Context
from sdialog.agents import Agent
from sdialog.personas import Persona
from sdialog.orchestrators import SimpleReflexOrchestrator
from dotenv import load_dotenv

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
    circumstances="Está en una sesión de terapia por primera vez y se siente un poco nervioso"
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

def lookup_menu(item: str) -> dict:
    """Return menu info and current specials for the given cafe item."""
    return {"item": item, "specials": ["vanilla latte", "cold brew"]}


react = SimpleReflexOrchestrator(
    condition=lambda utt: "decaf" in utt.lower(),
    instruction="Explain decaf options and suggest one."
)


for ix in range(1):
    primera_intervencion = "Hola Fernando, es un gusto conocerte. Toma asiento por favor. ¿Cómo te sientes hoy al estar aquí?"
    fernando_paciente = Agent(persona=paciente, tools=[lookup_menu])
    valeria_psicologo = Agent(persona=psicologo, first_utterance=primera_intervencion)
    
    valeria_psicologo = valeria_psicologo | react
    dialog = valeria_psicologo.dialog_with(fernando_paciente, context=contexto)
    dialog.print(orchestration=True)
    dialog.to_file(f"dialog_{ix}.json")