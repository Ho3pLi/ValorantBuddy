# Installer GUI

Questa cartella contiene `setup_gui.py`, uno strumento grafico che automatizza il setup di ValorantBuddy/SkinPeek su Windows.

## Prerequisiti

- Windows 10 o superiore
- [Python 3.11+](https://www.python.org/downloads/windows/) con il modulo `tkinter` configurato
- [Git](https://git-scm.com/download/win) disponibile nel `PATH`
- Connessione internet per scaricare dipendenze (`git`, `npm`, Node). Se `npm` non � disponibile, il tool prover� a installare automaticamente Node.js LTS (potrebbero servire privilegi amministrativi).

## Uso rapido (sviluppo)

1. Apri un terminale nella root del progetto.
2. Esegui `python installer/setup_gui.py`.
3. Nell'interfaccia grafica:
   - Seleziona la cartella dove vuoi installare il bot (il programma creerà una sottocartella `ValorantBuddy`).
   - Incolla il token del bot Discord.
   - Premi **Installa / Aggiorna**: il tool clonerà il repository, creerà `config.json`, installerà le dipendenze `npm`.
   - Quando l'installazione è completa puoi usare **Avvia bot** / **Ferma bot** per gestire il processo `node SkinPeek.js`.

## Creare l'eseguibile

Per distribuire il tool come `.exe`:

1. Installa PyInstaller una sola volta:
   ```powershell
   py -3.11 -m pip install pyinstaller
   ```
2. Genera l'eseguibile (modifica il percorso a seconda di dove hai installato Python):
   ```powershell
   py -3.11 -m PyInstaller --noconsole --onefile installer/setup_gui.py --name ValorantBuddySetup
   ```
3. Troverai `ValorantBuddySetup.exe` nella cartella `dist/`. Puoi pubblicarlo come asset su GitHub.

> Suggerimento: aggiungi eventuali risorse (icone, README personalizzati) direttamente nella cartella `installer/` e aggiorna il comando PyInstaller con `--add-data` se necessario.

## Note

- Se scegli come cartella di destinazione direttamente `...\ValorantBuddy`, il programma la userà senza creare un sottolivello aggiuntivo.
- L'interfaccia mostra i log completi di `git`, `npm`, dell'installer di Node.js e del bot per facilitare il debug.
- Il token viene scritto in chiaro in `config.json`; conserva l'eseguibile in un luogo sicuro.
