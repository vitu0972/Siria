import tkinter as tk
from tkinter import ttk
import json
import os

from theme import (
    BG, SURFACE, SURFACE2, BORDER, ACCENT, TEXT, TEXT_DIM,
    COR_RISCO,
    F_SMALL_B, F_SMALL, F_MONO, F_TITLE,
    PAD, PAD_S, PAD_L,
)

ARQUIVO = "riscos.json"
tabela  = None


def criar_aba_resultados(frame):
    global tabela
    frame.configure(bg=BG)

    # ── Cabeçalho ─────────────────────────────────────────────────────────────
    header = tk.Frame(frame, bg=SURFACE, pady=PAD_S)
    header.pack(fill="x")

    hrow = tk.Frame(header, bg=SURFACE)
    hrow.pack(fill="x", padx=PAD_L)

    tk.Label(hrow, text="// REGISTROS DE RISCO", font=F_TITLE,
             bg=SURFACE, fg=ACCENT, anchor="w").pack(side="left")

    tk.Button(
        hrow,
        text="↻ ATUALIZAR",
        command=atualizar_tabela,
        bg=SURFACE2, fg=TEXT_DIM,
        activebackground=BORDER, activeforeground=TEXT,
        font=F_SMALL_B, relief="flat", cursor="hand2",
        padx=PAD_S, pady=2,
    ).pack(side="right", pady=4)

    tk.Label(header, text="Histórico de avaliações cadastradas.", font=F_SMALL,
             bg=SURFACE, fg=TEXT_DIM, anchor="w").pack(padx=PAD_L, anchor="w")

    # ── Estilo tabela ──────────────────────────────────────────────────────────
    style = ttk.Style()
    style.configure("iOS.Treeview",
        background=SURFACE, foreground=TEXT, fieldbackground=SURFACE,
        rowheight=30, font=(F_MONO[0], F_MONO[1]), borderwidth=0)
    style.configure("iOS.Treeview.Heading",
        background=BG, foreground=ACCENT,
        font=(*F_SMALL_B,), relief="flat", padding=(PAD_S, 6))
    style.map("iOS.Treeview",
        background=[("selected", "#1f6feb")],
        foreground=[("selected", TEXT)])
    style.map("iOS.Treeview.Heading",
        background=[("active", BORDER)])
    style.layout("iOS.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    # ── Tabela ─────────────────────────────────────────────────────────────────
    tree_frame = tk.Frame(frame, bg=BG)
    tree_frame.pack(expand=True, fill="both", padx=PAD_L, pady=(PAD, PAD_L))

    vsb = tk.Scrollbar(tree_frame, orient="vertical", bg=SURFACE,
                        troughcolor=BG, activebackground=ACCENT,
                        relief="flat", width=6)
    vsb.pack(side="right", fill="y")

    tabela = ttk.Treeview(tree_frame, style="iOS.Treeview",
                           yscrollcommand=vsb.set, selectmode="browse")
    tabela.pack(fill="both", expand=True)
    vsb.config(command=tabela.yview)

    tabela["columns"] = ("setor", "ativo", "prob", "impacto", "risco", "classificacao")
    tabela.column("#0",            width=40,  anchor="center")
    tabela.column("setor",         width=140, anchor="w")
    tabela.column("ativo",         width=200, anchor="w")
    tabela.column("prob",          width=75,  anchor="center")
    tabela.column("impacto",       width=75,  anchor="center")
    tabela.column("risco",         width=75,  anchor="center")
    tabela.column("classificacao", width=110, anchor="center")

    tabela.heading("#0",            text="#")
    tabela.heading("setor",         text="SETOR")
    tabela.heading("ativo",         text="ATIVO")
    tabela.heading("prob",          text="PROB.")
    tabela.heading("impacto",       text="IMPACTO")
    tabela.heading("risco",         text="RISCO")
    tabela.heading("classificacao", text="CLASSIFICAÇÃO")

    for nome, cor in COR_RISCO.items():
        tabela.tag_configure(nome,       foreground=cor, background=SURFACE)
        tabela.tag_configure(nome+"_alt", foreground=cor, background=SURFACE2)

    atualizar_tabela()


def atualizar_tabela():
    global tabela
    if tabela is None:
        return

    for item in tabela.get_children():
        tabela.delete(item)

    if not os.path.exists(ARQUIVO):
        return

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        try:
            dados = json.load(f)
        except Exception:
            dados = []

    for i, item in enumerate(dados):
        classif = item.get("classificacao", "Indefinido")
        tag = (classif + "_alt") if i % 2 else classif
        tabela.insert("", "end",
            text=str(i + 1),
            values=(
                item["setor"],
                item["ativo_afetado"],
                item["probabilidade"],
                item["impacto"],
                item["calculo_risco"],
                classif,
            ),
            tags=(tag,),
        )
