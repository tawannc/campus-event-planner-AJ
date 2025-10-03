import datetime
from typing import List, Dict, Any

Evento = Dict[str, Any]

def validar_data(data_str: str) -> bool:
    try:
        datetime.datetime.strptime(data_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def adicionar_evento(lista_eventos: List[Evento], nome: str, data: str, local: str, categoria: str) -> None:
    novo_id = max([ev.get("id", 0) for ev in lista_eventos], default=0) + 1
    evento = {
        "id": novo_id,
        "nome": nome,
        "data": data,
        "local": local,
        "categoria": categoria,
        "participado": False
    }
    lista_eventos.append(evento)

def listar_eventos(lista_eventos: List[Evento]) -> None:
    for ev in lista_eventos:
        status = "Sim" if ev.get('participado', False) else "Não"
        print(
            f"ID: {ev.get('id')} | Nome: {ev.get('nome')} | Data: {ev.get('data')} | "
            f"Participou: {status}"
        )

def procurar_evento_por_nome(lista_eventos: List[Evento], nome: str) -> List[Evento]:
    termo = nome.strip().lower()
    return [
        ev for ev in lista_eventos
        if termo in ev.get("nome", "").lower()
    ]

def deletar_evento(lista_eventos: List[Evento], id_evento: int) -> bool:
    for i, ev in enumerate(lista_eventos):
        if ev.get("id") == id_evento:
            del lista_eventos[i]
            return True
    return False

def display_menu() -> None:
    print("\n=== Planejador de Eventos do Campus ===")
    print("1. Adicionar Evento")
    print("2. Ver Todos os Eventos")
    print("3. Filtrar por Categoria")
    print("4. Marcar Evento como Participado")
    print("5. Gerar Relatório")
    print("6. Deletar Evento")
    print("7. Buscar Evento por Nome")
    print("0. Sair")

def get_escolha_do_usuario() -> int:
    escolha = input("\nEscolha uma opção: ")
    return int(escolha) if escolha in {"0", "1", "2", "3", "4", "5", "6", "7"} else -1

def filtrar_eventos_por_categoria(lista_eventos: List[Evento], categoria: str) -> List[Evento]:
    return [
        ev for ev in lista_eventos
        if str(ev.get("categoria", "")).strip().lower() == categoria.strip().lower()
    ]

def marcar_evento_atendido(lista_eventos: List[Evento], id_evento: int) -> bool:
    for ev in lista_eventos:
        if ev.get("id") == id_evento:
            ev["participado"] = True
            return True
    return False

def _contar_por_categoria(lista_eventos: List[Evento]) -> Dict[str, int]:
    cont: Dict[str, int] = {}
    for ev in lista_eventos:
        cat = str(ev.get("categoria", "Sem categoria")).strip() or "Sem categoria"
        cont[cat] = cont.get(cat, 0) + 1
    return cont

def gerar_relatorio(lista_eventos: List[Evento]) -> None:
    total = len(lista_eventos)
    por_categoria = _contar_por_categoria(lista_eventos)
    participados = sum(1 for ev in lista_eventos if ev.get("participado", False))
    percentual = (participados / total * 100) if total > 0 else 0.0

    print("\n--- RELATÓRIO DE EVENTOS ---")
    print(f"Total de Eventos: {total}")
    print(f"Por Categoria: {por_categoria}")
    print(f"Participados: {percentual:.0f}% ({participados}/{total})")

def _pausar():
    input("\nPressione Enter para continuar...")

def _entrada_evento(lista_eventos: List[Evento]) -> None:
    print("\n== Adicionar Evento ==")
    nome = input("Nome do evento: ").strip()
    data = input("Data (DD-MM-YYYY): ").strip()
    local = input("Local: ").strip()
    categoria = input("Categoria: ").strip()

    if not all([nome, data, local, categoria]):
        print("\n[!] Todos os campos são obrigatórios."); _pausar(); return
    if not validar_data(data):
        print("\n[!] Data inválida. Use o formato DD-MM-YYYY."); _pausar(); return

    adicionar_evento(lista_eventos, nome, data, local, categoria)
    print("\nEvento adicionado com sucesso!")
    _pausar()

def _mostrar_todos(lista_eventos: List[Evento]) -> None:
    print("\n== Todos os Eventos ==")
    if not lista_eventos:
        print("(vazio)")
    else:
        listar_eventos(lista_eventos)
    _pausar()

def _filtrar_por_categoria(lista_eventos: List[Evento]) -> None:
    categoria = input("\nCategoria para filtrar: ").strip()
    resultados = filtrar_eventos_por_categoria(lista_eventos, categoria)

    print(f"\n== Eventos na Categoria: {categoria} ==")
    if not resultados:
        print("(nenhum evento encontrado)")
    else:
        listar_eventos(resultados)
    _pausar()

def _marcar_participado(lista_eventos: List[Evento]) -> None:
    print("\n== Marcar Evento como Participado ==")
    try:
        id_evento = int(input("ID do evento: ").strip())
        if marcar_evento_atendido(lista_eventos, id_evento):
            print("Evento marcado como participado!")
        else:
            print("[!] Evento não encontrado.")
    except ValueError:
        print("[!] ID inválido")
    _pausar()

def _deletar_evento(lista_eventos: List[Evento]) -> None:
    print("\n== Deletar Evento ==")
    try:
        id_evento = int(input("ID do evento a ser deletado: ").strip())
        if deletar_evento(lista_eventos, id_evento):
            print("Evento deletado com sucesso!")
        else:
            print("[!] Evento não encontrado.")
    except ValueError:
        print("[!] ID inválido")
    _pausar()

def _buscar_por_nome(lista_eventos: List[Evento]) -> None:
    nome = input("\nNome para buscar: ").strip()
    resultados = procurar_evento_por_nome(lista_eventos, nome)

    print(f"\n== Resultados para: {nome} ==")
    if not resultados:
        print("(nenhum evento encontrado)")
    else:
        listar_eventos(resultados)
    _pausar()

def _gerar_relatorio(lista_eventos: List[Evento]) -> None:
    gerar_relatorio(lista_eventos)
    _pausar()

def main():
    lista_de_eventos: List[Evento] = []
    
    while True:
        display_menu()
        opc = get_escolha_do_usuario()

        if opc == 1: _entrada_evento(lista_de_eventos)
        elif opc == 2: _mostrar_todos(lista_de_eventos)
        elif opc == 3: _filtrar_por_categoria(lista_de_eventos)
        elif opc == 4: _marcar_participado(lista_de_eventos)
        elif opc == 5: _gerar_relatorio(lista_de_eventos)
        elif opc == 6: _deletar_evento(lista_de_eventos)
        elif opc == 7: _buscar_por_nome(lista_de_eventos)
        elif opc == 0: print("Saindo... Até mais!"); break
        else: print("\n[!] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()