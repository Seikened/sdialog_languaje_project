import json

def trgger_tool(path="dialog_session_0.json",tool = "get_phq9_questions",    verbose=False):
    "Abrir el .json de la transcripción guardada de la sesión"
    with open(path, "r") as f:
        data = json.load(f)
    for evento in data["events"]:
        if evento["action"] == "tool" and evento["actionLabel"]=="call":
            if evento["content"]["name"]==tool:        
                
                evento_f = json.dumps(evento, indent=2, ensure_ascii=True)
                if verbose:
                    print(f"Evento: {evento_f}")
                return evento_f
    return None
    


se_encontro = trgger_tool(tool="get_phq9_questions", verbose=True)

print(f"Se encontro el evento: {se_encontro is not None}")