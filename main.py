# Estudante B: Módulo de Interação com Usuário e Relatórios

# Implemente a interface com o usuário e os recursos de relatórios:

#     Construa uma interface de menu no console (usando while + input).
#     Permita que os usuários:
#         Adicionem um evento (chamando a função do Estudante A).
#         Visualizem todos os eventos.
#         Filtragem de eventos por categoria (ex.: “Acadêmico”, “Social”, “Esportes”).
#         Marquem eventos como “participados” (adicione um campo booleano ao evento).
#         Visualizem um relatório resumido: total de eventos, eventos por categoria, % participados.

#     ✅ Funções que o Estudante B deve implementar:

#         displayMenu() → exibe as opções
#         getEscolhaDoUsuario() → retorna a escolha como inteiro
#         filtrarEventosPorCategoria(listaEventos, categiria)
#         marcarEventoAtendido(listaEventos, id)
#         gerarRelatorio(listaEventos) → imprime estatísticas



from typing import List, Dict, Any

from estudante_a import (
    adicionarEvento,
    listarEventos,
    procurarEventoPorNome,
    deletarEvento,
    validarData,
)

Evento = Dict[str, Any]


def displayMenu() -> None:
    print("\n=== Planejador de Eventos do Campus ===")
    print("1. Adicionar Evento")
    print("2. Ver Todos os Eventos")
    print("3. Filtrar por Categoria")
    print("4. Marcar Evento como Participado")
    print("5. Gerar Relatório")
    print("6. Sair")


def getEscolhaDoUsuario() -> int:
    escolha = input("\nEscolha uma opção: ")
    if escolha not in {"1", "2", "3", "4", "5", "6"}:
        return -1
    else:
        return int(escolha)



def filtrarEventosPorCategoria(listaEventos: List[Evento], categoria: str) -> List[Evento]:
    return [
        ev for ev in listaEventos
        if str(ev.get("categoria", "")).strip().lower() == categoria.strip().lower()
    ]


def marcarEventoAtendido(listaEventos: List[Evento], id_evento: int) -> bool:
    for ev in listaEventos:
        if ev.get("id") == id_evento:
            ev["participado"] = True
            return True
    return False


def _contar_por_categoria(listaEventos: List[Evento]) -> Dict[str, int]:
    cont: Dict[str, int] = {}
    for ev in listaEventos:
        cat = str(ev.get("categoria", "Sem categoria")).strip() or "Sem categoria"
        cont[cat] = cont.get(cat, 0) + 1
    return cont


def gerarRelatorio(listaEventos: List[Evento]) -> None:
    total = len(listaEventos)
    por_categoria = _contar_por_categoria(listaEventos)
    participados = sum(1 for ev in listaEventos if ev.get("participado", False))
    percentual = (participados / total * 100) if total > 0 else 0.0

    print("\n--- RELATÓRIO DE EVENTOS ---")
    print(f"Total de Eventos: {total}")
    print(f"Por Categoria: {por_categoria}")
    print(f"Participados: {percentual:.0f}% ({participados}/{total})")


def _pausar():
    input("\nPressione Enter para continuar...")


def _entrada_evento(listaEventos: List[Evento]) -> None:
    print("\n== Adicionar Evento ==")
    nome = input("Nome do evento: ").strip()
    data = input("Data (DD-MM-YYYY): ").strip()
    local = input("Local: ").strip()
    categoria = input("Categoria: ").strip()

    if not nome or not data or not local or not categoria:
        print("\n[!] Todos os campos são obrigatórios.")
        _pausar()
        return

    if not validarData(data):
        print("\n[!] Data inválida. Use o formato DD-MM-YYYY.")
        _pausar()
        return

    try:
        adicionarEvento(listaEventos, nome, data, local, categoria)
        print("\nEvento adicionado com sucesso!")
    except Exception as e:
        print(f"\n[!] Erro ao adicionar evento: {e}")

    _pausar()


def _mostrar_todos(listaEventos: List[Evento]) -> None:
    print("\n== Todos os Eventos ==")
    if not listaEventos:
        print("(vazio)")
        _pausar()
        return

    listarEventos(listaEventos)
    _pausar()


def _filtrar_por_categoria(listaEventos: List[Evento]) -> None:
    categoria = input("\nCategoria para filtrar: ").strip()
    resultados = filtrarEventosPorCategoria(listaEventos, categoria)

    print(f"\n== Eventos na Categoria: {categoria} ==")
    if not resultados:
        print("(nenhum evento encontrado)")
    else:
        for ev in resultados:
            print(
                f"ID: {ev.get('id')} | Nome: {ev.get('nome')} | Data: {ev.get('data')} | "
                f"Local: {ev.get('local')} | Participado: {ev.get('participado', False)}"
            )
    _pausar()


def _marcar_participado(listaEventos: List[Evento]) -> None:
    print("\n== Marcar Evento como Participado ==")
    try:
        id_str = input("ID do evento: ").strip()
        id_evento = int(id_str)
    except ValueError:
        print("[!] ID inválido")
        _pausar()
        return

    if marcarEventoAtendido(listaEventos, id_evento):
        print("Evento marcado como participado!")
    else:
        print("[!] Evento não encontrado.")
    _pausar()


def _gerar_relatorio(listaEventos: List[Evento]) -> None:
    gerarRelatorio(listaEventos)
    _pausar()


def main():
    listaEventos: List[Evento] = []

    while True:
        displayMenu()
        opc = getEscolhaDoUsuario()

        if opc == 1:
            _entrada_evento(listaEventos)
        if opc == 2:
            _mostrar_todos(listaEventos)
        if opc == 3:
            _filtrar_por_categoria(listaEventos)
        if opc == 4:
            _marcar_participado(listaEventos)
        if opc == 5:
            _gerar_relatorio(listaEventos)
        if opc == 6:
            print("Saindo... Até mais!")
            break
        else:
            print("\n[!] Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
