import json
from sdialog.personas import Persona


def pacientes() -> list[tuple[Persona, str]]:
    with open("personas.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    pacientes_list = []
    for persona in data:
        paciente = Persona(
            name=persona["name"],
            age=persona["age"],
            race=persona["race"],
            language=persona["language"],
            background=(persona["background"]),
            gender=persona["gender"],
            role=persona["role"], 
            personality=persona["personality"],
            rules=persona["rules"],
            circumstances=persona["circumstances"],
        )
        pacientes_list.append((paciente, persona["major"]))
    return pacientes_list



if __name__ == "__main__":
    lista_pacientes = pacientes()
    for paciente, major in lista_pacientes:
        print(f"\n [{major}] {paciente.name}")