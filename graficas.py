import json
import matplotlib.pyplot as plt



def graficar(dict_majors:dict, path_save:str="graficas_pacientes.png"):
    "Graficar la cantidad de pacientes por major"
    majors = list(dict_majors.keys())
    counts = list(dict_majors.values())

    plt.figure(figsize=(10, 6))
    plt.bar(majors, counts, color='skyblue')
    plt.xlabel('Majors')
    plt.ylabel('Cantidad de Pacientes')
    plt.title('Cantidad de Pacientes por Major')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path_save)
    plt.close()


def load_incidents(path="incidents.json"):
    "Cargar los incidentes desde el .json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["incidents"]



if __name__ == "__main__":
    incidentes = load_incidents()
    graficar(incidentes, path_save="graficas_pacientes.png")
        