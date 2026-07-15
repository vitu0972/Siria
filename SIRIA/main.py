"""
Risk Analyzer  —  Avaliação de Riscos com IA
Ponto de entrada. UX redesenhada com sidebar iOS Dark.
"""
import tkinter as tk

from interface.cadastro   import criar_aba_cadastro
from interface.resultados import criar_aba_resultados, atualizar_tabela
from interface.relatorio  import criar_aba_relatorio
from theme import (
    BG, SURFACE, SURFACE2, BORDER, ACCENT, ACCENT_H,
    TEXT, TEXT_DIM,
    F_DISPLAY, F_SMALL_B, F_SMALL, F_BOLD,
    PAD, PAD_S, PAD_L,
)

# ── Itens da barra lateral ────────────────────────────────────────────────────
_NAV = [
    ("⊕", "Cadastro",     0),
    ("≡", "Resultados",   1),
    ("◳", "Relatório IA", 2),
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Risk Analyzer")
        self.geometry("1000x660")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self.resizable(True, True)

        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass

        self._aba_atual = -1
        self._btns: list[tk.Label] = []
        self._frames: list[tk.Frame] = []

        self._build()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self):
        sidebar = tk.Frame(self, bg=SURFACE, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Frame(self, bg=BORDER, width=1).pack(side="left", fill="y")

        content = tk.Frame(self, bg=BG)
        content.pack(side="left", fill="both", expand=True)

        self._build_sidebar(sidebar)
        self._build_pages(content)
        self._navegar(0)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, sb: tk.Frame):
        logo = tk.Frame(sb, bg=SURFACE, pady=PAD_L)
        logo.pack(fill="x")

        top_bar = tk.Frame(sb, bg=ACCENT, height=2)
        top_bar.pack(fill="x")

        tk.Label(logo, text="RISK", font=(*F_DISPLAY[:2], "bold"),
                 bg=SURFACE, fg=ACCENT).pack(padx=PAD_L, anchor="w")
        tk.Label(logo, text="ANALYZER", font=(*F_DISPLAY[:2], "bold"),
                 bg=SURFACE, fg=TEXT).pack(padx=PAD_L, anchor="w")
        tk.Label(logo, text="//  Avaliação com IA", font=F_SMALL,
                 bg=SURFACE, fg=TEXT_DIM).pack(padx=PAD_L, anchor="w", pady=(2, 0))

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x")

        tk.Label(sb, text="MENU", font=F_SMALL_B, bg=SURFACE, fg=TEXT_DIM,
                 anchor="w").pack(fill="x", padx=PAD_L, pady=(PAD, PAD_S // 2))

        for idx, (icone, nome, _) in enumerate(_NAV):
            btn = tk.Label(
                sb,
                text=f"  {icone}   {nome}",
                font=F_SMALL_B,
                bg=SURFACE, fg=TEXT_DIM,
                anchor="w", cursor="hand2", pady=10,
            )
            btn.pack(fill="x", padx=PAD_S)
            btn.bind("<Button-1>", lambda _, i=idx: self._navegar(i))
            btn.bind("<Enter>",    lambda e, b=btn, i=idx: self._btn_hover(b, i))
            btn.bind("<Leave>",    lambda e, b=btn, i=idx: self._btn_leave(b, i))
            self._btns.append(btn)

        tk.Label(sb, text="v2.3.0", font=F_SMALL, bg=SURFACE, fg=TEXT_DIM
                 ).pack(side="bottom", pady=PAD)

    def _btn_hover(self, btn: tk.Label, idx: int):
        if idx != self._aba_atual:
            btn.configure(bg=SURFACE2)

    def _btn_leave(self, btn: tk.Label, idx: int):
        if idx != self._aba_atual:
            btn.configure(bg=SURFACE)

    # ── Páginas ───────────────────────────────────────────────────────────────
    def _build_pages(self, content: tk.Frame):
        builders = [
            criar_aba_cadastro,
            criar_aba_resultados,
            criar_aba_relatorio,
        ]
        for builder in builders:
            f = tk.Frame(content, bg=BG)
            builder(f)
            self._frames.append(f)

    # ── Navegação ─────────────────────────────────────────────────────────────
    def _navegar(self, idx: int):
        if idx == self._aba_atual:
            return

        for f in self._frames:
            f.pack_forget()
        self._frames[idx].pack(fill="both", expand=True)
        self._aba_atual = idx

        for i, btn in enumerate(self._btns):
            if i == idx:
                btn.configure(bg=BG, fg=ACCENT)
            else:
                btn.configure(bg=SURFACE, fg=TEXT_DIM)

        if idx == 1:
            atualizar_tabela()


if __name__ == "__main__":
    App().mainloop()
