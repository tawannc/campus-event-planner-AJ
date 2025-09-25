import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

Evento = Dict[str, Any]

def validarData(dataStr: str) -> bool:
    try:
        datetime.strptime(dataStr, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def adicionarEvento(listaEventos: List[Evento], nome: str, data: str, local: str, categoria: str) -> None:
    next_id = max([ev.get("id", 0) for ev in listaEventos], default=0) + 1
    evento = {
        "id": next_id,
        "nome": nome,
        "data": data,
        "local": local,
        "categoria": categoria,
        "participado": False
    }
    listaEventos.append(evento)

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

def gerarRelatorio(listaEventos: List[Evento]) -> Dict[str, Any]:
    total = len(listaEventos)

    cont_categoria = {}
    for ev in listaEventos:
        cat = str(ev.get("categoria", "Sem categoria")).strip() or "Sem categoria"
        cont_categoria[cat] = cont_categoria.get(cat, 0) + 1

    participados = sum(1 for ev in listaEventos if ev.get("participado", False))
    percentual = (participados / total * 100) if total > 0 else 0.0

    return {
        "total": total,
        "por_categoria": cont_categoria,
        "participados": participados,
        "percentual": percentual
    }

if "eventos" not in st.session_state:
    st.session_state.eventos = []

st.title("🎓 Planejador de Eventos do Campus")

menu_options = ["Adicionar Evento", "Ver Todos os Eventos", "Filtrar por Categoria", "Marcar Evento como Participado", "Gerar Relatório"]
selected_option = st.sidebar.selectbox("Escolha uma opção:", menu_options)

if selected_option == "Adicionar Evento":
    st.header("📝 Adicionar Evento")

    with st.form("add_event_form"):
        nome = st.text_input("Nome do evento:")
        data = st.text_input("Data (DD-MM-YYYY):")
        local = st.text_input("Local:")
        categoria = st.text_input("Categoria:")

        submitted = st.form_submit_button("Adicionar Evento")

        if submitted:
            if not nome or not data or not local or not categoria:
                st.error("Todos os campos são obrigatórios.")
            elif not validarData(data):
                st.error("Data inválida. Use o formato DD-MM-YYYY.")
            else:
                adicionarEvento(st.session_state.eventos, nome, data, local, categoria)
                st.success("Evento adicionado com sucesso!")
                st.rerun()

elif selected_option == "Ver Todos os Eventos":
    st.header("📅 Todos os Eventos")

    if not st.session_state.eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        df = pd.DataFrame(st.session_state.eventos)
        df["participado"] = df["participado"].apply(lambda x: "Sim" if x else "Não")
        st.dataframe(df, use_container_width=True)

elif selected_option == "Filtrar por Categoria":
    st.header("🔍 Filtrar por Categoria")

    if not st.session_state.eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        categorias = list(set(ev.get("categoria", "") for ev in st.session_state.eventos))
        categoria_selecionada = st.selectbox("Selecione uma categoria:", categorias)

        if categoria_selecionada:
            eventos_filtrados = filtrarEventosPorCategoria(st.session_state.eventos, categoria_selecionada)

            if not eventos_filtrados:
                st.info(f"Nenhum evento encontrado na categoria '{categoria_selecionada}'.")
            else:
                st.write(f"**Eventos na categoria: {categoria_selecionada}**")
                df = pd.DataFrame(eventos_filtrados)
                df["participado"] = df["participado"].apply(lambda x: "Sim" if x else "Não")
                st.dataframe(df, use_container_width=True)

elif selected_option == "Marcar Evento como Participado":
    st.header("✅ Marcar Evento como Participado")

    if not st.session_state.eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        eventos_nao_participados = [ev for ev in st.session_state.eventos if not ev.get("participado", False)]

        if not eventos_nao_participados:
            st.info("Todos os eventos já foram marcados como participados.")
        else:
            evento_opcoes = {f"{ev['id']} - {ev['nome']}": ev['id'] for ev in eventos_nao_participados}
            evento_selecionado = st.selectbox("Selecione um evento:", list(evento_opcoes.keys()))

            if st.button("Marcar como Participado"):
                id_evento = evento_opcoes[evento_selecionado]
                if marcarEventoAtendido(st.session_state.eventos, id_evento):
                    st.success("Evento marcado como participado!")
                    st.rerun()
                else:
                    st.error("Erro ao marcar evento.")

elif selected_option == "Gerar Relatório":
    st.header("📊 Relatório de Eventos")

    if not st.session_state.eventos:
        st.info("Nenhum evento cadastrado.")
    else:
        relatorio = gerarRelatorio(st.session_state.eventos)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de Eventos", relatorio["total"])

        with col2:
            st.metric("Eventos Participados", relatorio["participados"])

        with col3:
            st.metric("Percentual Participado", f"{relatorio['percentual']:.0f}%")

        st.subheader("Eventos por Categoria")
        if relatorio["por_categoria"]:
            df_cat = pd.DataFrame(list(relatorio["por_categoria"].items()), columns=["Categoria", "Quantidade"])
            st.bar_chart(df_cat.set_index("Categoria"))
        else:
            st.info("Nenhuma categoria encontrada.")

st.sidebar.markdown("---")
st.sidebar.info(f"Total de eventos: {len(st.session_state.eventos)}")