# estudante_a.py — Módulo do Estudante A (mínimo viável)

from datetime import datetime

# Lista global de eventos (apenas em memória)
_eventos = []
_next_id = 1


def adicionarEvento(listaEventos, nome, data, local, categoria):
    global _next_id
    evento = {
        "id": _next_id,
        "nome": nome,
        "data": data,
        "local": local,
        "categoria": categoria,
        "participado": False
    }
    listaEventos.append(evento)
    _next_id += 1


def listarEventos(listaEventos):
    if not listaEventos:
        print("(nenhum evento cadastrado)")
    else:
        for ev in listaEventos:
            print(
                f"ID: {ev['id']} | Nome: {ev['nome']} | Data: {ev['data']} | "
                f"Local: {ev['local']} | Categoria: {ev['categoria']} | "
                f"Participado: {ev.get('participado', False)}"
            )


def procurarEventoPorNome(listaEventos, nome):
    resultados = [
        ev for ev in listaEventos if nome.lower() in ev["nome"].lower()
    ]
    return resultados


def deletarEvento(listaEventos, id):
    for ev in listaEventos:
        if ev["id"] == id:
            listaEventos.remove(ev)
            return True
    return False


def validarData(dataStr):
    try:
        datetime.strptime(dataStr, "%d-%m-%Y")
        return True
    except ValueError:
        return False
