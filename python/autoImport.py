import mysql.connector
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from datetime import datetime
import pandas as pd
import os

# Função para obter o ID do usuário com base no nome de usuário
def get_user_id(username, cursor):
    try:
        cursor.execute("SELECT id FROM y4kaq_users WHERE username = %s", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        return None

# Função para obter o asset_id da categoria ou componente
def get_parent_asset_id(catid, cursor):
    # Primeiro, tenta encontrar o asset_id da categoria
    cursor.execute("SELECT asset_id FROM y4kaq_categories WHERE id = %s", (catid,))
    category_asset = cursor.fetchone()
    if category_asset:
        return category_asset[0]
    
    # Se não encontrar, usa o asset_id do componente com_content (pode variar, geralmente é 1 ou outro valor fixo)
    cursor.execute("SELECT id FROM y4kaq_assets WHERE name = 'com_content'")
    component_asset = cursor.fetchone()
    return component_asset[0] if component_asset else 1  # Valor padrão, ajuste se necessário

# Função para publicar um único artigo com asset_id automático e created ajustado
def publicar_artigo(event=None):
    try:
        db = mysql.connector.connect(
            host="mysql07.centrointernacional.tv",  # Substitua pelo host do seu banco, ex.: "localhost"
            user="centrointernac6",  # Substitua pelo seu usuário do MySQL
            password="hOE21xm88X5",  # Substitua pela sua senha do MySQL
            database="centrointernac6"  # Substitua pelo nome do seu banco de dados
        )
        cursor = db.cursor()

        title = entry_title.get()
        introtext = entry_intro.get("1.0", tk.END).strip()
        fulltext = entry_full.get("1.0", tk.END).strip()
        username = entry_username.get()

        author_id = get_user_id(username, cursor)
        if not author_id:
            messagebox.showerror("Erro", f"Usuário '{username}' não encontrado no banco de dados!")
            return

        alias = title.lower().replace(" ", "-").replace("[^a-z0-9-]", "")
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Inserir o artigo em y4kaq_content com created igual a publish_up
        sql_content = """
            INSERT INTO `y4kaq_content` (`title`, `alias`, `introtext`, `fulltext`, `state`, `catid`, `created_by`, `access`, `language`, `images`, `urls`, `attribs`, `metadata`, `publish_up`, `created`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores_content = (
            title,
            alias,
            introtext,
            fulltext,
            1,  # state = 1 (publicado)
            28,  # catid fixo para a categoria "Notícias"
            author_id,
            2,  # access = 2 (registrado)
            "*",  # language = "*" (todos os idiomas)
            '{"image_intro":"","image_intro_alt":"","image_intro_caption":"","float_intro":"","image_fulltext":"","image_fulltext_alt":"","image_fulltext_caption":"","float_fulltext":""}',
            '{"urla":false,"urlatext":"","targeta":"","urlb":false,"urlbtext":"","targetb":"","urlc":false,"urlctext":"","targetc":""}',
            '{}',
            '{}',
            current_date,  # publish_up
            current_date  # created, mesmo valor de publish_up
        )

        cursor.execute(sql_content, valores_content)
        db.commit()

        # Pegar o ID do artigo recém-inserido
        article_id = cursor.lastrowid

        # Obter o parent_asset_id (da categoria 28 ou com_content)
        parent_asset_id = get_parent_asset_id(28, cursor)

        # Inserir na tabela y4kaq_assets
        sql_assets = """
            INSERT INTO `y4kaq_assets` (`name`, `parent_id`, `title`, `rules`)
            VALUES (%s, %s, %s, %s)
        """
        asset_name = f"com_content.article.{article_id}"
        asset_rules = '{"core.delete":[],"core.edit":[],"core.edit.state":[]}'  # Regras padrão, ajuste conforme necessário
        valores_assets = (asset_name, parent_asset_id, title, asset_rules)

        cursor.execute(sql_assets, valores_assets)
        db.commit()

        # Atualizar o asset_id no artigo
        asset_id = cursor.lastrowid
        sql_update_content = """
            UPDATE `y4kaq_content` SET `asset_id` = %s WHERE `id` = %s
        """
        cursor.execute(sql_update_content, (asset_id, article_id))
        db.commit()

        messagebox.showinfo("Sucesso", f"Artigo '{title}' publicado com asset_id {asset_id}!")
        entry_title.delete(0, tk.END)
        entry_intro.delete("1.0", tk.END)
        entry_full.delete("1.0", tk.END)
        entry_username.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao publicar: {str(e)}")
    finally:
        db.close()

# Função para criar e salvar um template de planilha (mantido como antes)
def criar_template():
    template_data = {
        'Título': ['Exemplo de Título 1', 'Exemplo de Título 2'],
        'Introdução': ['Breve introdução aqui...', 'Outra introdução aqui...'],
        'Texto Completo': ['Texto completo do artigo 1...', 'Texto completo do artigo 2...'],
        'Usuário': ['admin', 'user1']
    }
    df = pd.DataFrame(template_data)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    if file_path:
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False, encoding='utf-8')
        else:
            df.to_excel(file_path, index=False)
        messagebox.showinfo("Sucesso", f"Template salvo em: {file_path}")

# Função para importar e mapear planilha com asset_id e created ajustado
def importar_planilha():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            df = pd.read_excel(file_path)

        # Cria uma janela para mapear colunas com o mesmo tema escuro
        map_window = tk.Toplevel(janela)
        map_window.title("Mapear Colunas da Planilha")
        map_window.geometry("300x350")
        map_window.configure(background=DARK_BACKGROUND)  # Fundo escuro na janela

        # Frame para organizar os elementos com o mesmo estilo
        map_frame = ttk.Frame(map_window, padding="10", style="TFrame")
        map_frame.pack(fill="both", expand=True)

        # Estilização dos elementos na janela de mapeamento
        ttk.Label(map_frame, text="Selecione as colunas da planilha:", background=DARK_BACKGROUND, font=("Helvetica", 11, "bold"), foreground=TEXT_COLOR).pack(pady=10)

        columns = df.columns.tolist()
        title_var = tk.StringVar()
        intro_var = tk.StringVar()
        fulltext_var = tk.StringVar()
        username_var = tk.StringVar()

        ttk.Combobox(map_frame, textvariable=title_var, values=columns, state="readonly", style="TCombobox").pack(pady=5)
        ttk.Label(map_frame, text="Título:", background=DARK_BACKGROUND, font=("Helvetica", 10, "bold"), foreground=TEXT_COLOR).pack()
        ttk.Combobox(map_frame, textvariable=intro_var, values=columns, state="readonly", style="TCombobox").pack(pady=5)
        ttk.Label(map_frame, text="Introdução:", background=DARK_BACKGROUND, font=("Helvetica", 10, "bold"), foreground=TEXT_COLOR).pack()
        ttk.Combobox(map_frame, textvariable=fulltext_var, values=columns, state="readonly", style="TCombobox").pack(pady=5)
        ttk.Label(map_frame, text="Texto Completo:", background=DARK_BACKGROUND, font=("Helvetica", 10, "bold"), foreground=TEXT_COLOR).pack()
        ttk.Combobox(map_frame, textvariable=username_var, values=columns, state="readonly", style="TCombobox").pack(pady=5)
        ttk.Label(map_frame, text="Usuário:", background=DARK_BACKGROUND, font=("Helvetica", 10, "bold"), foreground=TEXT_COLOR).pack()

        def confirmar_mapeamento():
            title_col = title_var.get()
            intro_col = intro_var.get()
            fulltext_col = fulltext_var.get()
            username_col = username_var.get()

            if not all([title_col, intro_col, fulltext_col, username_col]):
                messagebox.showerror("Erro", "Por favor, selecione todas as colunas!")
                return

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="centrointernac6"
            )
            cursor = db.cursor()

            total_artigos = 0
            for index, row in df.iterrows():
                title = str(row[title_col]) if title_col in row else ""
                introtext = str(row[intro_col]) if intro_col in row else ""
                fulltext = str(row[fulltext_col]) if fulltext_col in row else ""
                username = str(row[username_col]) if username_col in row else ""

                author_id = get_user_id(username, cursor)
                if not author_id:
                    messagebox.showwarning("Aviso", f"Usuário '{username}' não encontrado para o artigo '{title}'. Pulando...")
                    continue

                alias = title.lower().replace(" ", "-").replace("[^a-z0-9-]", "")
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Inserir o artigo em y4kaq_content com created igual a publish_up
                sql_content = """
                    INSERT INTO `y4kaq_content` (`title`, `alias`, `introtext`, `fulltext`, `state`, `catid`, `created_by`, `access`, `language`, `images`, `urls`, `attribs`, `metadata`, `publish_up`, `created`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores_content = (
                    title,
                    alias,
                    introtext,
                    fulltext,
                    1,
                    28,
                    author_id,
                    2,
                    "*",
                    '{"image_intro":"","image_intro_alt":"","image_intro_caption":"","float_intro":"","image_fulltext":"","image_fulltext_alt":"","image_fulltext_caption":"","float_fulltext":""}',
                    '{"urla":false,"urlatext":"","targeta":"","urlb":false,"urlbtext":"","targetb":"","urlc":false,"urlctext":"","targetc":""}',
                    '{}',
                    '{}',
                    current_date,
                    current_date
                )

                cursor.execute(sql_content, valores_content)
                db.commit()

                # Pegar o ID do artigo recém-inserido
                article_id = cursor.lastrowid

                # Obter o parent_asset_id (da categoria 28 ou com_content)
                parent_asset_id = get_parent_asset_id(28, cursor)

                # Inserir na tabela y4kaq_assets
                sql_assets = """
                    INSERT INTO `y4kaq_content` (`name`, `parent_id`, `title`, `rules`)
                    VALUES (%s, %s, %s, %s)
                """
                asset_name = f"com_content.article.{article_id}"
                asset_rules = '{"core.delete":[],"core.edit":[],"core.edit.state":[]}'  # Regras padrão, ajuste conforme necessário
                valores_assets = (asset_name, parent_asset_id, title, asset_rules)

                cursor.execute(sql_assets, valores_assets)
                db.commit()

                # Atualizar o asset_id no artigo
                asset_id = cursor.lastrowid
                sql_update_content = """
                    UPDATE `y4kaq_content` SET `asset_id` = %s WHERE `id` = %s
                """
                cursor.execute(sql_update_content, (asset_id, article_id))
                db.commit()

                total_artigos += 1

            db.commit()
            messagebox.showinfo("Sucesso", f"Importados e publicados {total_artigos} artigos com sucesso!")
            map_window.destroy()

        # Ajuste no botão "Confirmar" para tamanho e texto visível
        confirm_button = ttk.Button(map_frame, text="Confirmar", command=confirmar_mapeamento, style="TButton", width=15)  # Aumentei a largura para 15
        confirm_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar planilha: {str(e)}")

# Criação da janela com estilo personalizado
janela = tk.Tk()
janela.title("Publicador de Artigos Joomla 3")
janela.geometry("600x800")  # Aumentei o tamanho para melhor layout

# Estilo personalizado com tema escuro usando #4682B4 (SteelBlue)
style = ttk.Style()
style.theme_use("clam")  # Usa o tema Clam para melhor personalização

# Configuração de cores e fontes para tema escuro
DARK_BACKGROUND = "#2C3E50"  # Cinza-azulado escuro (fundo uniforme)
PRIMARY_COLOR = "#4682B4"  # SteelBlue
TEXT_COLOR = "#FFFFFF"  # Branco para contraste
INPUT_BG = "#465C71"  # Cor para campos de entrada escura
INPUT_FG = "#FFFFFF"  # Texto branco nos campos de entrada

style.configure("TFrame", background=DARK_BACKGROUND)
style.configure("TLabel", background=DARK_BACKGROUND, font=("Helvetica", 11, "bold"), foreground=TEXT_COLOR)
style.configure("TButton", background=PRIMARY_COLOR, font=("Helvetica", 10, "bold"), foreground=TEXT_COLOR, padding=12, relief="flat")
style.configure("TEntry", fieldbackground=INPUT_BG, font=("Helvetica", 10), foreground=INPUT_FG, background=INPUT_BG)
style.configure("TText", fieldbackground=INPUT_BG, font=("Helvetica", 10), foreground=INPUT_FG, background=INPUT_BG)
style.configure("TCombobox", fieldbackground=INPUT_BG, font=("Helvetica", 10), foreground=INPUT_FG, background=INPUT_BG)
style.configure("TLabelframe", background=DARK_BACKGROUND)  # Fundo do LabelFrame agora é o mesmo que DARK_BACKGROUND
style.configure("TLabelframe.Label", background=DARK_BACKGROUND, font=("Helvetica", 12, "bold"), foreground=PRIMARY_COLOR)

# Mapear estados para animações visuais nos botões (tons mais escuros no tema escuro)
style.map("TButton", background=[('active', '#356EA9'), ('pressed', '#2A5A8E')], relief=[('pressed', 'sunken')])

# Frame principal com borda sutil
main_frame = ttk.Frame(janela, padding="15", style="TFrame")
main_frame.pack(fill="both", expand=True)

# Título da aplicação
title_label = ttk.Label(main_frame, text="Publicador de Artigos Joomla 3", font=("Helvetica", 16, "bold"), background=DARK_BACKGROUND, foreground=PRIMARY_COLOR)
title_label.pack(pady=(0, 15))

# Frame para entrada manual com borda arredondada (usando LabelFrame com estilo)
input_frame = ttk.LabelFrame(main_frame, text="Insira os Detalhes do Artigo", padding="10", style="TLabelframe")
input_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Campos de entrada com estilo
ttk.Label(input_frame, text="Título:").pack(pady=5)
entry_title = ttk.Entry(input_frame, width=50, style="TEntry")
entry_title.pack(pady=5, padx=5, fill="x")

ttk.Label(input_frame, text="Introdução:").pack(pady=5)
entry_intro = tk.Text(input_frame, height=5, width=50, font=("Helvetica", 10), bg=INPUT_BG, fg=INPUT_FG, bd=1, relief="solid")
entry_intro.pack(pady=5, padx=5, fill="x")

ttk.Label(input_frame, text="Texto Completo:").pack(pady=5)
entry_full = tk.Text(input_frame, height=10, width=50, font=("Helvetica", 10), bg=INPUT_BG, fg=INPUT_FG, bd=1, relief="solid")
entry_full.pack(pady=5, padx=5, fill="x")

ttk.Label(input_frame, text="Usuário do Site:").pack(pady=5)
entry_username = ttk.Entry(input_frame, width=30, style="TEntry")
entry_username.pack(pady=5, padx=5, fill="x")
entry_username.bind("<Return>", publicar_artigo)

# Frame para botões com layout horizontal
button_frame = ttk.Frame(main_frame, padding="10", style="TFrame")
button_frame.pack(fill="x", pady=10)

# Botões estilizados com ícones simples (usando texto como placeholder para ícones)
btn_publicar = ttk.Button(button_frame, text="📝 Publicar Artigo", command=publicar_artigo, style="TButton")
btn_publicar.pack(side="left", padx=5, pady=5)

btn_importar = ttk.Button(button_frame, text="📤 Importar Planilha", command=importar_planilha, style="TButton")
btn_importar.pack(side="left", padx=5, pady=5)

btn_template = ttk.Button(button_frame, text="📥 Baixar Template", command=criar_template, style="TButton")
btn_template.pack(side="left", padx=5, pady=5)

# Configura o fundo da janela
janela.configure(background=DARK_BACKGROUND)

# Inicia a interface
janela.mainloop()