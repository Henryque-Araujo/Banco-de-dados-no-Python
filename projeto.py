import sqlite3
import tkinter as tk
from tkinter import messagebox

# Configuração do banco de dados
db_name = "alunos.db"
table_name = "registros"

# Criação do banco de dados e tabela (se não existirem)
def setup_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            matricula INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para inserir um aluno no banco de dados
def incluir_aluno():
    matricula = entry_matricula.get()
    nome = entry_nome.get()

    if not matricula or not nome:
        label_status["text"] = "Preencha todos os campos!"
        return

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Verifica se a matrícula já existe
        cursor.execute(f"SELECT * FROM {table_name} WHERE matricula = ?", (matricula,))
        if cursor.fetchone():
            label_status["text"] = "Matrícula já Cadastrada"
        else:
            # Insere o registro no banco de dados
            cursor.execute(f"INSERT INTO {table_name} (matricula, nome) VALUES (?, ?)", (matricula, nome))
            conn.commit()
            label_status["text"] = "Aluno Cadastrado com Sucesso!!!"

            # Exibe a lista de alunos cadastrados no console
            cursor.execute(f"SELECT * FROM {table_name}")
            alunos = cursor.fetchall()
            print("Lista de Alunos Cadastrados:")
            for aluno in alunos:
                print(f"Matrícula: {aluno[0]}, Nome: {aluno[1]}")
    except sqlite3.Error as e:
        label_status["text"] = "Erro ao acessar o banco de dados."
        print(f"Erro: {e}")
    finally:
        conn.close()

# Configuração da interface gráfica
def criar_interface():
    global entry_matricula, entry_nome, label_status

    janela = tk.Tk()
    janela.title("Inclusão de Alunos")

    # Label e Entry para Matrícula
    tk.Label(janela, text="Matrícula:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_matricula = tk.Entry(janela, font=("Arial", 12))
    entry_matricula.grid(row=0, column=1, padx=10, pady=5)

    # Label e Entry para Nome do Aluno
    tk.Label(janela, text="Nome do Aluno:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = tk.Entry(janela, font=("Arial", 12))
    entry_nome.grid(row=1, column=1, padx=10, pady=5)

    # Botão para incluir aluno no banco de dados
    botao_incluir = tk.Button(janela, text="Incluir Aluno no Banco de Dados", font=("Arial", 12), command=incluir_aluno)
    botao_incluir.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Label para exibir mensagens de status
    label_status = tk.Label(janela, text="", font=("Arial", 12), fg="white", bg="gray")
    label_status.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    # Iniciar o loop da interface gráfica
    janela.mainloop()

# Configuração inicial
if __name__ == "__main__":
    setup_database()
    criar_interface()
