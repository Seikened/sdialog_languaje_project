import sdialog
from dotenv import load_dotenv
from typing import Literal

# Configuración del LLM ------------------------------------------------

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


companies = Literal["openai", "anthropic", "azure", "ollama"]

def arrancar(company: companies="openai", temperature: float=0.9):
    load_dotenv()
    print(f"Cargando LLM...{company}")
    match company:
        case "openai":
            sdialog.config.llm("openai:gpt-4o-mini", temperature=temperature)
        case "ollama":
            sdialog.config.llm("ollama:gemma3:1b", temperature=temperature)





# MAJORS ----------------------------------------------------
DICT_MAJORS: dict[str, dict[str, str]] = {
    # -------------------- ARQUITECTURA Y DISEÑO --------------------
    "ARQ": {
        "name": "Licenciatura en Arquitectura",
        "description": "Formación orientada al diseño, construcción y planeación de espacios arquitectónicos sustentables y funcionales.",
    },
    "DP": {
        "name": "Licenciatura en Diseño de Producto",
        "description": "Centrado en la creación de productos innovadores que integran funcionalidad, estética y viabilidad técnica.",
    },
    "DDI": {
        "name": "Licenciatura en Diseño Digital Interactivo",
        "description": "Enfoque en diseño multimedia, experiencias digitales y soluciones interactivas basadas en tecnología.",
    },
    "DGI": {
        "name": "Licenciatura en Diseño Gráfico e Innovación",
        "description": "Explora comunicación visual, branding, creatividad y diseño para medios digitales e impresos.",
    },

    # -------------------- INGENIERÍAS --------------------
    "IC": {
        "name": "Ingeniería Civil",
        "description": "Preparación en diseño, construcción y supervisión de obras civiles, con énfasis en infraestructura sostenible.",
    },
    "IBT": {
        "name": "Ingeniería en Bionanotecnología",
        "description": "Programa que integra biología, química y nanotecnología para desarrollar soluciones científicas y biomédicas.",
    },
    "IIA": {
        "name": "Ingeniería en Inteligencia Artificial",
        "description": "Formación en aprendizaje automático, ciencia de datos, sistemas inteligentes y computación avanzada.",
    },
    "IND": {
        "name": "Ingeniería Industrial",
        "description": "Optimización de procesos, operaciones, logística y sistemas para mejorar productividad y eficiencia.",
    },
    "IME": {
        "name": "Ingeniería Mecánica y Eléctrica",
        "description": "Combina sistemas mecánicos, eléctricos y energéticos para diseñar y mantener maquinaria y tecnologías industriales.",
    },
    "IMC": {
        "name": "Ingeniería Mecatrónica",
        "description": "Integra mecánica, electrónica y control para desarrollar sistemas automatizados y robots inteligentes.",
    },

    # -------------------- C. ECONÓMICO-ADMINISTRATIVAS --------------------
    "ACE": {
        "name": "Licenciatura en Administración y Creación de Empresas",
        "description": "Desarrolla competencias para emprender, dirigir y gestionar organizaciones modernas y sostenibles.",
    },
    "CEI": {
        "name": "Licenciatura en Comercio Exterior y Logística Internacional",
        "description": "Enfocada en logística global, tratados comerciales y gestión de cadenas de suministro internacionales.",
    },
    "CEF": {
        "name": "Licenciatura en Contaduría y Estrategias Financieras",
        "description": "Preparación en contabilidad, auditoría, finanzas corporativas y análisis económico.",
    },
    "IDN": {
        "name": "Licenciatura en Inteligencia de Negocios",
        "description": "Enseña análisis de datos, visualización, procesos de decisión y estrategias basadas en información.",
    },
    "MP": {
        "name": "Licenciatura en Marketing y Publicidad",
        "description": "Diseño de campañas, estrategias de marca y comunicación comercial para mercados contemporáneos.",
    },

    # -------------------- C. SOCIALES Y HUMANIDADES --------------------
    "COM": {
        "name": "Licenciatura en Comunicación",
        "description": "Estudia medios, narrativa, comunicación estratégica y producción de contenido.",
    },
    "DER": {
        "name": "Licenciatura en Derecho",
        "description": "Formación jurídica sólida en leyes, litigación, derechos humanos y procesos normativos.",
    },
    "RI": {
        "name": "Licenciatura en Relaciones Internacionales",
        "description": "Análisis del sistema global, política exterior, diplomacia y cooperación internacional.",
    },

    # -------------------- C. DE LA SALUD --------------------
    "NUT": {
        "name": "Licenciatura en Nutrición y Ciencia de los Alimentos",
        "description": "Estudia salud alimentaria, metabolismo, dietología y desarrollo de alimentos.",
    },
    "PSI": {
        "name": "Licenciatura en Psicología",
        "description": "Formación en comportamiento humano, neurociencia, salud mental y psicoterapia.",
    },
}

