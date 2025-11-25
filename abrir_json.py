import json
from config import DICT_MAJORS

def create_entry_incidents(path:str, reset_data: bool):
    "Abrir o crear el .json de incidentes"
    global indent
    indent = 4
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("Archivo existente cargado.")
    except FileNotFoundError:
        data = {"incidents": {key: 0 for key in DICT_MAJORS.keys()}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=True)
        print("Archivo no encontrado. Creando uno nuevo.")
        return data

    if "incidents" not in data:
        data["incidents"] = {}

    modified = False

    for key in DICT_MAJORS.keys():
        if key not in data["incidents"] or reset_data:
            print(f"Inicializando incidente para {key}")
            data["incidents"][key] = 0
            modified = True

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=True)

    return data


    
        
    
    

def entry_incidents(reset_data: bool = False, path="incidents.json", major: str = "IIA"):
    "Registrar un incidente en el .json"
    data = create_entry_incidents(reset_data=reset_data, path=path)

    data["incidents"][major] += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
        return json.dumps(data, indent=indent, ensure_ascii=False)
    return None

def trgger_tool(path_dialog:str ="dialog_session_0.json",path_incidents:str="incidents.json",tool:str = "get_phq9_questions", verbose:bool=False):
    "Abrir el .json de la transcripción guardada de la sesión"
    with open(path_dialog, "r") as f:
        data = json.load(f)
    for evento in data["events"]:
        if evento["action"] == "tool" and evento["actionLabel"]=="call":
            if evento["content"]["name"]==tool:
                major = "IIA" # TODO: Obtener el major desde el context llamado
                data = entry_incidents(reset_data=False, path=path_incidents, major=major)
                evento_f = json.dumps(evento, indent=indent, ensure_ascii=True)
                if verbose:
                    if data:
                        print(f"Incidente registrado para el major {major}")
                    print(f"Incidentes actuales: {data}")
                    print(f"Evento: {evento_f}")
                return evento_f
    return None
    

if __name__ == "__main__":
    se_encontro = trgger_tool(
        path_dialog="dialog_session_0.json",
        path_incidents="incidents.json",
        tool="get_phq9_questions", 
        verbose=True
    )

    print(f"Se encontro el evento: {se_encontro is not None}")