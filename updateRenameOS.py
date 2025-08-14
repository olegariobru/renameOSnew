import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# lista com caminhos completos dos arquivos selecionados
arquivos_selecionados = []

# ====== Funções da aba Renomear ======
def selecionar_arquivos():
    global arquivos_selecionados
    files = filedialog.askopenfilenames(title="Selecione os arquivos para renomear")
    if files:
        arquivos_selecionados = list(files)
        refresh_lista()
        atualizar_contadores()

def refresh_lista():
    lista_arquivos.delete(0, tk.END)
    for caminho in arquivos_selecionados:
        lista_arquivos.insert(tk.END, os.path.basename(caminho))

def remover_arquivo():
    sel = lista_arquivos.curselection()
    if not sel:
        messagebox.showwarning("Atenção", "Selecione ao menos um arquivo para remover.")
        return
    for idx in reversed(sel):
        del arquivos_selecionados[idx]
        lista_arquivos.delete(idx)
    atualizar_contadores()

def preencher_com_nomes():
    nomes = [os.path.basename(p) for p in arquivos_selecionados]
    entrada_novos_nomes.delete("1.0", tk.END)
    if nomes:
        entrada_novos_nomes.insert(tk.END, "\n".join(nomes))
    atualizar_contadores()

def atualizar_contadores(event=None):
    qt_arquivos = len(arquivos_selecionados)
    texto = entrada_novos_nomes.get("1.0", tk.END).strip()
    linhas = [l for l in texto.splitlines() if l.strip() != ""]
    qt_novos = len(linhas)

    selecionados_var.set(f"Arquivos selecionados: {qt_arquivos}")
    novos_var.set(f"Novos nomes (não vazios): {qt_novos}")

    if qt_arquivos > 0 and qt_arquivos == qt_novos:
        btn_renomear.config(state=tk.NORMAL)
    else:
        btn_renomear.config(state=tk.DISABLED)

def executar_renomeacao():
    if not arquivos_selecionados:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        return

    texto = entrada_novos_nomes.get("1.0", tk.END).strip()
    novos = [l.strip() for l in texto.splitlines() if l.strip() != ""]

    if len(novos) != len(arquivos_selecionados):
        messagebox.showerror("Erro", "A quantidade de novos nomes não corresponde à quantidade de arquivos.")
        return

    resumo = f"{len(novos)} arquivos serão renomeados. Deseja continuar?"
    if not messagebox.askyesno("Confirmação", resumo):
        return

    conflitos = []
    pairs = []
    for i, old_path in enumerate(arquivos_selecionados):
        pasta = os.path.dirname(old_path)
        novo_nome = novos[i]
        base_old, ext_old = os.path.splitext(os.path.basename(old_path))
        if "." not in novo_nome:
            novo_nome = novo_nome + ext_old
        new_path = os.path.join(pasta, novo_nome)
        pairs.append((old_path, new_path))
        if os.path.exists(new_path):
            conflitos.append(new_path)

    if conflitos:
        msg = "Existem arquivos com os nomes destino já existentes:\n\n"
        msg += "\n".join(conflitos[:10])
        if len(conflitos) > 10:
            msg += f"\n... (+{len(conflitos)-10} outros)"
        msg += "\n\nRemova ou altere os nomes antes de prosseguir."
        messagebox.showerror("Conflitos detectados", msg)
        return

    erros = []
    for old, new in pairs:
        try:
            os.rename(old, new)
        except Exception as e:
            erros.append(f"{os.path.basename(old)} -> {os.path.basename(new)} : {e}")

    if erros:
        messagebox.showerror("Alguns erros ocorreram", "\n".join(erros[:10]))
    else:
        messagebox.showinfo("Sucesso", "Todos os arquivos foram renomeados com sucesso!")

    arquivos_selecionados.clear()
    refresh_lista()
    entrada_novos_nomes.delete("1.0", tk.END)
    atualizar_contadores()

# ====== GUI Principal ======
root = tk.Tk()
root.title("Menu de Scripts")
root.geometry("700x500")

notebook = ttk.Notebook(root)
frame_renomear = ttk.Frame(notebook)
frame_mover = ttk.Frame(notebook)
notebook.add(frame_renomear, text="Renomear")
notebook.add(frame_mover, text="Mover Arquivos")
notebook.pack(expand=True, fill="both")

# ====== Layout da aba Renomear ======
frame_esquerdo = ttk.Frame(frame_renomear)
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

ttk.Button(frame_esquerdo, text="Selecionar arquivos", command=selecionar_arquivos).pack(fill=tk.X, pady=5)
ttk.Button(frame_esquerdo, text="Remover selecionados", command=remover_arquivo).pack(fill=tk.X, pady=5)
ttk.Button(frame_esquerdo, text="Preencher com nomes atuais", command=preencher_com_nomes).pack(fill=tk.X, pady=5)

selecionados_var = tk.StringVar(value="Arquivos selecionados: 0")
novos_var = tk.StringVar(value="Novos nomes (não vazios): 0")
ttk.Label(frame_esquerdo, textvariable=selecionados_var).pack(pady=2)
ttk.Label(frame_esquerdo, textvariable=novos_var).pack(pady=2)

btn_renomear = ttk.Button(frame_esquerdo, text="Renomear arquivos", command=executar_renomeacao, state=tk.DISABLED)
btn_renomear.pack(fill=tk.X, pady=15)

frame_direito = ttk.Frame(frame_renomear)
frame_direito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
ttk.Label(frame_direito, text="Arquivos selecionados:").pack(anchor=tk.W)
lista_arquivos = tk.Listbox(frame_direito, selectmode=tk.EXTENDED)
lista_arquivos.pack(fill=tk.BOTH, expand=True)
ttk.Label(frame_direito, text="Novos nomes (um por linha):").pack(anchor=tk.W, pady=(10,0))
entrada_novos_nomes = tk.Text(frame_direito, height=10)
entrada_novos_nomes.pack(fill=tk.BOTH, expand=True)
entrada_novos_nomes.bind("<KeyRelease>", atualizar_contadores)

# ====== Layout da aba Mover Arquivos ======
pasta_origem = tk.StringVar()
pasta_destino = tk.StringVar()
arquivo_txt = tk.StringVar()  # NOVO: guarda o caminho do arquivo TXT

ttk.Label(frame_mover, text="Pasta de Origem:").pack(pady=2)
ttk.Entry(frame_mover, textvariable=pasta_origem, width=50).pack(pady=2)
ttk.Button(frame_mover, text="Selecionar", command=lambda: pasta_origem.set(filedialog.askdirectory(title="Selecione a pasta de origem"))).pack(pady=2)

ttk.Label(frame_mover, text="Pasta de Destino:").pack(pady=2)
ttk.Entry(frame_mover, textvariable=pasta_destino, width=50).pack(pady=2)
ttk.Button(frame_mover, text="Selecionar", command=lambda: pasta_destino.set(filedialog.askdirectory(title="Selecione a pasta de destino"))).pack(pady=2)

ttk.Label(frame_mover, text="Nome do arquivo (separado por vírgula):").pack(pady=2)
entry_nomes = ttk.Entry(frame_mover, width=50)
entry_nomes.pack(pady=2)

ttk.Label(frame_mover, text="ou quantidade de arquivos:").pack(pady=2)
entry_qtd = ttk.Entry(frame_mover, width=10)
entry_qtd.pack(pady=2)

# NOVO: Campo e botão para selecionar o TXT
ttk.Label(frame_mover, text="ou arquivo TXT com nomes (um por linha):").pack(pady=2)
ttk.Entry(frame_mover, textvariable=arquivo_txt, width=50).pack(pady=2)
ttk.Button(frame_mover, text="Selecionar TXT", command=lambda: arquivo_txt.set(filedialog.askopenfilename(title="Selecione o arquivo TXT", filetypes=[("Arquivos de texto", "*.txt")]))).pack(pady=2)

def mover_arquivos():
    origem = pasta_origem.get()
    destino = pasta_destino.get()
    quantidade = entry_qtd.get().strip()
    nomes = entry_nomes.get().strip()
    caminho_txt = arquivo_txt.get().strip()

    if not origem or not destino:
        messagebox.showerror("Erro", "Selecione as pastas de origem e destino.")
        return

    arquivos = os.listdir(origem)

    # PRIORIDADE: TXT > nomes digitados > quantidade
    if caminho_txt:
        try:
            with open(caminho_txt, "r", encoding="utf-8") as f:
                lista_txt = [linha.strip() for linha in f if linha.strip()]
            lista_arquivos_mover = [nome for nome in lista_txt if nome in arquivos]
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo TXT: {e}")
            return

    elif nomes:
        lista_arquivos_mover = [nome.strip() for nome in nomes.split(",") if nome.strip() in arquivos]

    elif quantidade.isdigit():
        lista_arquivos_mover = arquivos[:int(quantidade)]

    else:
        messagebox.showerror("Erro", "Informe um TXT, nomes ou quantidade de arquivos.")
        return

    if not lista_arquivos_mover:
        messagebox.showwarning("Aviso", "Nenhum arquivo encontrado para mover.")
        return

    movidos = 0
    for arquivo in lista_arquivos_mover:
        try:
            shutil.move(os.path.join(origem, arquivo), os.path.join(destino, arquivo))
            movidos += 1
        except Exception as e:
            print(f"Erro ao mover {arquivo}: {e}")

    messagebox.showinfo("Concluído", f"{movidos} arquivos movidos.")

ttk.Button(frame_mover, text="Mover Arquivos", command=mover_arquivos).pack(pady=10)

root.mainloop()
