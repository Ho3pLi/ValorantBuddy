import json
import os
import shutil
import tempfile
import urllib.request

import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

REPO_URL = "https://github.com/Ho3pLi/ValorantBuddy.git"
REPO_DIRNAME = "ValorantBuddy"
CONFIG_FILE = "config.json"
CONFIG_TEMPLATE = "config.json.example"
NODE_INSTALLER_URL = "https://nodejs.org/dist/v20.17.0/node-v20.17.0-x64.msi"


ACCENT_COLOR = "#ff4655"
BACKGROUND_COLOR = "#0f1923"
SURFACE_COLOR = "#141821"
SECONDARY_COLOR = "#1e2530"
TEXT_PRIMARY = "#f4f5f7"
TEXT_MUTED = "#9aa6b2"
SUCCESS_COLOR = "#3ddc97"
LOG_BACKGROUND = "#0b121b"


class InstallerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ValorantBuddy Setup")
        self.root.geometry("720x520")
        self.root.minsize(720, 520)
        self.process: subprocess.Popen[str] | None = None
        self.install_thread: threading.Thread | None = None
        self.repo_path: str | None = None
        self.log_queue: queue.Queue[str] = queue.Queue()

        self.path_var = tk.StringVar()
        self.token_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto")

        self.style = ttk.Style(self.root)
        self.setup_styles()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(100, self.flush_log_queue)

    def setup_styles(self) -> None:
        self.root.configure(bg=BACKGROUND_COLOR)
        try:
            self.style.theme_use("clam")
        except tk.TclError:  # pragma: no cover - fallback if theme missing
            pass

        self.root.option_add("*Font", ("Segoe UI", 11))
        self.root.option_add("*Foreground", TEXT_PRIMARY)

        self.style.configure("Main.TFrame", background=BACKGROUND_COLOR)
        self.style.configure("Card.TFrame", background=SURFACE_COLOR)
        self.style.configure("AccentBar.TFrame", background=ACCENT_COLOR)
        self.style.configure("Title.TLabel", background=SURFACE_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 20, "bold"))
        self.style.configure("Section.TLabel", background=SURFACE_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 12, "bold"))
        self.style.configure("Muted.TLabel", background=SURFACE_COLOR, foreground=TEXT_MUTED, font=("Segoe UI", 10))
        self.style.configure("Status.TLabel", background=SURFACE_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 12, "bold"))

        self.style.configure("Accent.TButton", background=ACCENT_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 11, "bold"), padding=10, borderwidth=0)
        self.style.map("Accent.TButton", background=[("active", "#ff6171"), ("disabled", "#4d2d34")], foreground=[("disabled", TEXT_MUTED)])

        self.style.configure("Secondary.TButton", background="#2a3340", foreground=TEXT_PRIMARY, font=("Segoe UI", 10), padding=10, borderwidth=0)
        self.style.map("Secondary.TButton", background=[("active", "#324050"), ("disabled", "#1f2732")], foreground=[("disabled", TEXT_MUTED)])

        self.style.configure("Start.TButton", background=SUCCESS_COLOR, foreground=BACKGROUND_COLOR, font=("Segoe UI", 11, "bold"), padding=10, borderwidth=0)
        self.style.map("Start.TButton", background=[("active", "#47e7a8"), ("disabled", "#28483a")], foreground=[("disabled", TEXT_MUTED)])

        self.style.configure("Stop.TButton", background=ACCENT_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 11, "bold"), padding=10, borderwidth=0)
        self.style.map("Stop.TButton", background=[("active", "#ff6171"), ("disabled", "#4d2d34")], foreground=[("disabled", TEXT_MUTED)])

        self.style.configure("Input.TEntry", fieldbackground=SECONDARY_COLOR, background=SECONDARY_COLOR, foreground=TEXT_PRIMARY, insertcolor=TEXT_PRIMARY, padding=6)
        self.style.map("Input.TEntry", fieldbackground=[("focus", "#23303f")])

        self.style.configure("Separator.TSeparator", background="#1f2733")
        self.style.configure("Modern.Vertical.TScrollbar", background=SURFACE_COLOR, troughcolor=BACKGROUND_COLOR, arrowcolor=TEXT_PRIMARY)

    def create_widgets(self) -> None:
        outer = ttk.Frame(self.root, style="Main.TFrame", padding=24)
        outer.pack(fill="both", expand=True)

        card = ttk.Frame(outer, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True)

        header = ttk.Frame(card, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 12))

        title_label = ttk.Label(header, text="ValorantBuddy Setup", style="Title.TLabel")
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header,
            text="Setup guidato per clonare, configurare e avviare il bot.",
            style="Muted.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        accent_bar = tk.Frame(card, bg=ACCENT_COLOR, height=3, bd=0, highlightthickness=0)
        accent_bar.pack(fill="x", pady=(0, 18))

        path_label = ttk.Label(card, text="Cartella di installazione", style="Section.TLabel")
        path_label.pack(anchor="w")

        path_row = ttk.Frame(card, style="Card.TFrame")
        path_row.pack(fill="x", pady=(6, 16))

        path_entry = ttk.Entry(path_row, textvariable=self.path_var, style="Input.TEntry")
        path_entry.pack(side="left", fill="x", expand=True)

        browse_button = ttk.Button(path_row, text="Sfoglia", command=self.browse_path, style="Secondary.TButton")
        browse_button.pack(side="left", padx=(12, 0))

        token_label = ttk.Label(card, text="Token del bot Discord", style="Section.TLabel")
        token_label.pack(anchor="w")

        token_entry = ttk.Entry(card, textvariable=self.token_var, show="*", style="Input.TEntry")
        token_entry.pack(fill="x", pady=(6, 18))

        actions_row = ttk.Frame(card, style="Card.TFrame")
        actions_row.pack(fill="x", pady=(0, 18))

        self.install_button = ttk.Button(
            actions_row,
            text="Installa / Aggiorna",
            command=self.start_install,
            style="Accent.TButton",
        )
        self.install_button.pack(side="left")

        self.start_button = ttk.Button(
            actions_row,
            text="Avvia bot",
            command=self.start_bot,
            state="disabled",
            style="Start.TButton",
        )
        self.start_button.pack(side="left", padx=(12, 0))

        self.stop_button = ttk.Button(
            actions_row,
            text="Ferma bot",
            command=self.stop_bot,
            state="disabled",
            style="Stop.TButton",
        )
        self.stop_button.pack(side="left", padx=(12, 0))

        ttk.Separator(card, orient="horizontal", style="Separator.TSeparator").pack(fill="x", pady=(0, 18))

        status_row = ttk.Frame(card, style="Card.TFrame")
        status_row.pack(fill="x", pady=(0, 12))

        status_caption = ttk.Label(status_row, text="Stato:", style="Muted.TLabel")
        status_caption.pack(side="left")

        self.status_label = ttk.Label(status_row, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(side="left", padx=(8, 0))

        log_container = ttk.Frame(card, style="Card.TFrame")
        log_container.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_container,
            height=15,
            state="disabled",
            wrap="word",
            bg=LOG_BACKGROUND,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground="#22303c",
            font=("Consolas", 10),
            padx=12,
            pady=12,
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        log_scroll = ttk.Scrollbar(log_container, style="Modern.Vertical.TScrollbar", command=self.log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scroll.set)

    def browse_path(self) -> None:
        selected = filedialog.askdirectory()
        if selected:
            self.path_var.set(selected)

    def start_install(self) -> None:
        if self.install_thread and self.install_thread.is_alive():
            messagebox.showinfo("Installazione in corso", "Attendi che l'installazione corrente finisca.")
            return

        install_path = self.path_var.get().strip()
        token = self.token_var.get().strip()

        if not install_path:
            messagebox.showerror("Percorso mancante", "Seleziona la cartella di installazione.")
            return

        if not token:
            messagebox.showerror("Token mancante", "Inserisci il token del bot Discord.")
            return

        if shutil.which("npm") is None:
            self.log("npm non trovato nel PATH. Avvio installazione di Node.js LTS...")
            self.set_status("Installazione Node.js...", "#d17f00")
            if not self.install_nodejs():
                messagebox.showerror("npm non trovato", "Installazione di Node.js non riuscita. Installa Node.js (che include npm) manualmente e assicurati che sia nel PATH.")
                self.set_status("npm non disponibile", "#b00020")
                return
            self.log("npm disponibile dopo l'installazione.")

        self.install_button.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.set_status("Installazione in corso...", "#d17f00")

        # Run install in background to keep UI responsive.
        self.install_thread = threading.Thread(
            target=self.install_bot,
            args=(install_path, token),
            daemon=True,
        )
        self.install_thread.start()

    def install_bot(self, install_path: str, token: str) -> None:
        try:
            self.log("Avvio installazione...")
            base_path = Path(install_path).expanduser()

            if base_path.name.lower() == REPO_DIRNAME.lower():
                repo_path = base_path.resolve()
                repo_parent = repo_path.parent
                repo_parent.mkdir(parents=True, exist_ok=True)
            else:
                base_path.mkdir(parents=True, exist_ok=True)
                repo_path = (base_path / REPO_DIRNAME).resolve()

            if repo_path.exists():
                git_dir = repo_path / ".git"
                if git_dir.exists():
                    self.log("Repository già presente, salto la clonazione.")
                elif any(repo_path.iterdir()):
                    raise RuntimeError(
                        f"La cartella {repo_path} esiste già e non è un repository git. Scegli un'altra posizione."
                    )
                else:
                    repo_path.rmdir()
                    self.run_command(["git", "clone", REPO_URL, str(repo_path)])
            else:
                self.run_command(["git", "clone", REPO_URL, str(repo_path)])

            config_template = repo_path / CONFIG_TEMPLATE
            if not config_template.exists():
                raise FileNotFoundError(f"File {CONFIG_TEMPLATE} non trovato nel repository clonato.")

            config_path = repo_path / CONFIG_FILE
            config_data = json.loads(config_template.read_text(encoding="utf-8"))
            config_data["token"] = token
            config_json = json.dumps(config_data, indent=2) + "\n"
            config_path.write_text(config_json, encoding="utf-8")
            self.log("config.json aggiornato con il token fornito.")

            self.run_command(["npm", "install"], cwd=str(repo_path))
            self.repo_path = str(repo_path)
            self.log("Installazione completata con successo.")
            self.root.after(0, lambda: self.set_status("Installazione completata", "#1b8a34"))
        except Exception as exc:  # noqa: BLE001
            self.log(f"Errore: {exc}")
            self.root.after(0, lambda: self.set_status("Errore durante l'installazione", "#b00020"))
        finally:
            self.root.after(0, self.update_buttons)
            self.root.after(0, lambda: self.install_button.configure(state="normal"))

    def run_command(self, command: list[str], cwd: str | None = None) -> None:
        display_command = ' '.join(command)
        resolved = shutil.which(command[0])
        if resolved:
            if resolved.lower().endswith((".cmd", ".bat")):
                actual_command = [os.environ.get("ComSpec", "cmd.exe"), "/c", resolved, *command[1:]]
            else:
                actual_command = [resolved, *command[1:]]
        else:
            actual_command = command

        self.log(f"Eseguo: {display_command}")
        if resolved and resolved != command[0]:
            self.log(f"Eseguibile risolto: {resolved}")
        try:
            process = subprocess.Popen(
                actual_command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as missing:
            raise RuntimeError(
                f"Comando '{command[0]}' non trovato. Assicurati che sia installato e raggiungibile dal PATH."
            ) from missing

        assert process.stdout is not None
        for line in process.stdout:
            self.log(line.rstrip())

        code = process.wait()
        if code != 0:
            raise RuntimeError(f"Il comando {display_command} � terminato con codice {code}.")


    def install_nodejs(self) -> bool:
        self.log("Tentativo di installazione automatica di Node.js LTS.")
        installers = [
            self.install_nodejs_via_winget,
            self.install_nodejs_via_download,
        ]
        for installer in installers:
            try:
                if installer():
                    self.try_append_node_to_path()
                    if shutil.which("npm") is not None:
                        self.log("Node.js installato correttamente.")
                        return True
            except Exception as exc:  # noqa: BLE001
                self.log(f"Installazione tramite {installer.__name__} non riuscita: {exc}")
        self.try_append_node_to_path()
        if shutil.which("npm") is None:
            self.log("npm ancora non disponibile dopo i tentativi automatici.")
            return False
        return True

    def install_nodejs_via_winget(self) -> bool:
        winget = shutil.which("winget")
        if winget is None:
            self.log("winget non disponibile, salto questo metodo di installazione.")
            return False
        self.log("Provo a installare Node.js tramite winget...")
        command = [
            winget,
            "install",
            "-e",
            "--id",
            "OpenJS.NodeJS.LTS",
            "--accept-package-agreements",
            "--accept-source-agreements",
            "--silent",
        ]
        try:
            self.run_command(command)
            return True
        except RuntimeError as exc:
            self.log(f"Installazione tramite winget fallita: {exc}")
            return False

    def install_nodejs_via_download(self) -> bool:
        self.log("Scarico Node.js LTS dal sito ufficiale...")
        try:
            with urllib.request.urlopen(NODE_INSTALLER_URL) as response:
                with tempfile.NamedTemporaryFile(suffix=".msi", delete=False) as tmp_file:
                    shutil.copyfileobj(response, tmp_file)
                    installer_path = Path(tmp_file.name)
        except Exception as exc:  # noqa: BLE001
            self.log(f"Download Node.js fallito: {exc}")
            return False

        self.log(f"Eseguo il programma di installazione: {installer_path}")
        try:
            result = subprocess.run(
                ["msiexec", "/i", str(installer_path), "/qn", "/norestart"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            self.log("msiexec non trovato. Impossibile installare Node.js automaticamente.")
            installer_path.unlink(missing_ok=True)
            return False
        except Exception as exc:  # noqa: BLE001
            self.log(f"Errore durante l'esecuzione di msiexec: {exc}")
            installer_path.unlink(missing_ok=True)
            return False

        output = (result.stdout or "").strip()
        if output:
            self.log(output)

        installer_path.unlink(missing_ok=True)

        if result.returncode != 0:
            self.log(f"msiexec ha restituito codice {result.returncode}")
            return False

        self.log("Installazione silenziosa completata.")
        return True

    def try_append_node_to_path(self) -> None:
        possible_dirs = []
        for env_var in ("ProgramFiles", "ProgramFiles(x86)"):
            base = os.environ.get(env_var)
            if base:
                possible_dirs.append(Path(base) / "nodejs")
        possible_dirs.append(Path.home() / "AppData" / "Roaming" / "npm")

        current_path = os.environ.get("PATH", "")
        for directory in possible_dirs:
            if directory and directory.exists():
                dir_str = str(directory)
                if dir_str not in current_path.split(os.pathsep):
                    os.environ["PATH"] = dir_str + os.pathsep + current_path
                    current_path = os.environ["PATH"]
                    self.log(f"Aggiunto {dir_str} al PATH corrente.")
                npm_cmd = directory / "npm.cmd"
                npm_exe = directory / "npm.exe"
                if npm_cmd.exists() or npm_exe.exists():
                    break

    def start_bot(self) -> None:
        if self.process and self.process.poll() is None:
            messagebox.showinfo("Bot già in esecuzione", "Il bot è già avviato.")
            return

        repo_path = self.resolve_repo_path()
        if not repo_path:
            messagebox.showerror("Repository non trovato", "Installa il bot o verifica il percorso indicato.")
            return

        self.log("Avvio del bot...")
        try:
            self.process = subprocess.Popen(
                ["node", "SkinPeek.js"],
                cwd=str(repo_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as missing:
            self.log("Node.js non trovato. Installa Node e riprova.")
            self.set_status("Node.js mancante", "#b00020")
            raise RuntimeError("Node.js non trovato") from missing

        assert self.process.stdout is not None
        threading.Thread(
            target=self.stream_process_output,
            args=(self.process,),
            daemon=True,
        ).start()
        self.set_status("Bot in esecuzione", "#1b8a34")
        self.update_buttons()

    def stop_bot(self) -> None:
        if not self.process or self.process.poll() is not None:
            self.set_status("Bot non in esecuzione", "#d17f00")
            self.update_buttons()
            return

        self.log("Arresto del bot...")
        self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.log("Terminazione forzata del bot.")
            self.process.kill()
            self.process.wait()

        self.log("Bot fermato.")
        self.process = None
        self.set_status("Bot fermato", "black")
        self.update_buttons()

    def stream_process_output(self, process: subprocess.Popen[str]) -> None:
        assert process.stdout is not None
        for line in process.stdout:
            self.log(line.rstrip())
        exit_code = process.wait()
        self.log(f"Processo terminato con codice {exit_code}.")
        self.root.after(0, lambda: self.set_status("Bot terminato", "#d17f00"))
        self.root.after(0, self.update_buttons)

    def resolve_repo_path(self) -> Path | None:
        if self.repo_path and Path(self.repo_path).exists():
            return Path(self.repo_path)

        install_input = self.path_var.get().strip()
        if not install_input:
            return None

        install_path = Path(install_input).expanduser()
        candidates = []
        if install_path.exists():
            candidates.append(install_path)
        candidates.append(install_path / REPO_DIRNAME)

        for candidate in candidates:
            package_file = candidate / "package.json"
            if package_file.exists():
                self.repo_path = str(candidate.resolve())
                return Path(self.repo_path)
        return None

    def flush_log_queue(self) -> None:
        while not self.log_queue.empty():
            message = self.log_queue.get_nowait()
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        self.root.after(100, self.flush_log_queue)

    def log(self, message: str) -> None:
        self.log_queue.put(message)

    def set_status(self, text: str, color: str) -> None:
        self.status_var.set(text)
        self.status_label.configure(foreground=color)

    def update_buttons(self) -> None:
        repo_available = self.resolve_repo_path() is not None
        process_running = self.process and self.process.poll() is None

        if process_running:
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
        else:
            self.start_button.configure(state="normal" if repo_available else "disabled")
            self.stop_button.configure(state="disabled")

    def on_close(self) -> None:
        if self.process and self.process.poll() is None:
            if messagebox.askyesno("Chiudi", "Il bot è in esecuzione. Vuoi fermarlo e uscire?"):
                self.stop_bot()
            else:
                return
        self.root.destroy()


def main() -> None:
    if sys.version_info < (3, 11):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Versione Python", "Serve Python 3.11 o superiore per eseguire questo installer.")
        root.destroy()
        return

    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
