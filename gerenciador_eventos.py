import datetime

def validar_data(data_str):
    try:
        datetime.datetime.strptime(data_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def adicionar_evento(lista_eventos, nome, data, local, categoria):
    if not all([nome, data, local, categoria]):
        print("Erro: Todos os campos devem ser preenchidos.")
        return None
    if not validar_data(data):
        print("Erro: Formato de data inválido. Use AAAA-MM-DD.")
        return None

    novo_id = lista_eventos[-1]['id'] + 1 if lista_eventos else 1
    evento = {
        "id": novo_id,
        "nome": nome,
        "data": data,
        "local": local,
        "categoria": categoria,
        "participado": False
    }
    lista_eventos.append(evento)
    print(f"✅ Evento '{nome}' (ID: {novo_id}) adicionado com sucesso.")
    return novo_id

def listar_eventos(lista_eventos):
    if not lista_eventos:
        print("\n--- Nenhum evento cadastrado ---")
        return

    print("\n--- Lista de Eventos ---")
    for evento in lista_eventos:
        status = "Sim" if evento['participado'] else "Não"
        print(f"ID: {evento['id']} | Nome: {evento['nome']} | Categoria: {evento['categoria']} | Data: {evento['data']} | Participou: {status}")
    print("------------------------\n")

def procurar_evento_por_nome(lista_eventos, termo_busca):
    termo = termo_busca.lower()
    resultados = [evento for evento in lista_eventos if termo in evento['nome'].lower() or termo in evento['categoria'].lower()]
    return resultados

def deletar_evento_por_id(lista_eventos, id_evento):
    for i, evento in enumerate(lista_eventos):
        if evento['id'] == id_evento:
            nome = evento['nome']
            del lista_eventos[i]
            print(f"🗑️ Evento '{nome}' (ID: {id_evento}) foi deletado com sucesso.")
            return True
    print(f"Erro: Evento com ID {id_evento} não encontrado.")
    return False

def deletar_evento_por_nome(lista_eventos, nome_evento):
    for i, evento in enumerate(lista_eventos):
        if evento['nome'].lower() == nome_evento.lower():
            del lista_eventos[i]
            print(f"🗑️ Evento '{nome_evento}' foi deletado com sucesso.")
            return True
    print(f"Erro: Evento com nome '{nome_evento}' não encontrado.")
    return False

# --- Bloco de Teste

if __name__ == "__main__":
    eventos = []
    print("🚀 Iniciando testes...\n")

    adicionar_evento(eventos, "Palestra de Python", "2025-10-20", "Auditório 1", "Tecnologia")
    adicionar_evento(eventos, "Feira de Startups", "2025-11-05", "Pavilhão", "Negócios")
    adicionar_evento(eventos, "Workshop de Design", "2025-10-22", "Sala 3", "Tecnologia")

    listar_eventos(eventos)

    print("\n--- Deletando por ID ---")
    deletar_evento_por_id(eventos, 2)
    listar_eventos(eventos)

    print("\n--- Deletando por Nome ---")
    deletar_evento_por_nome(eventos, "Workshop de Design")
    listar_eventos(eventos)

    print("\n--- Adicionando novo evento ---")
    adicionar_evento(eventos, "Meetup de IA", "2025-12-01", "Online", "Tecnologia")
    listar_eventos(eventos)

    print("\n--- Buscando por 'tecnologia' ---")
    resultados = procurar_evento_por_nome(eventos, "tecnologia")
    if resultados:
        print("Eventos encontrados:")
        listar_eventos(resultados)
    else:
        print("Nenhum evento encontrado.")

    print("\n✅ Testes concluídos!")