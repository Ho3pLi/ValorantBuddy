# ValorantBuddy

> Un assistente per gestire facilmente il bot Valorant basato su SkinPeek. / A companion that makes managing the Valorant bot built on SkinPeek straightforward.

## Italiano

### Basato su SkinPeek

Il progetto nasce come fork evoluto di [SkinPeek](https://github.com/giorgi-o/SkinPeek), il celebre bot Discord che mostra negozio giornaliero, night market, bundle e statistiche di Valorant. Abbiamo mantenuto l'intero core del bot e delle sue feature, concentrandoci sull'offrire un'esperienza d'uso piu semplice per chi lavora su Windows.

### Novita principali introdotte da ValorantBuddy

- **Installer grafico (Tkinter) incluso**: al primo avvio guida la clonazione del repository originale, la creazione del `config.json` e l'installazione delle dipendenze Node.js.
- **Dashboard integrata**: una volta completata la configurazione, la stessa finestra diventa una mini-dashboard che permette di avviare o fermare il bot con un click e mostra i log in tempo reale.
- **Persistenza dello stato**: il programma ricorda percorso di installazione, token configurato e modalita corrente, cosi da tornare subito alla dashboard ai successivi avvii.

### Funzionalita del bot (ereditarie da SkinPeek)

- Visualizza negozio giornaliero, bundle, Night Market e battle pass senza aprire il gioco.
- Imposta alert per essere avvisato quando una skin arriva nel negozio.
- Gestisce piu account, memorizza lo storico delle skin e traduce i nomi nella lingua di Valorant.
- Offre comandi amministrativi per configurazione rapida e supporta sharding per server di grandi dimensioni.

### Requisiti

- Windows 10/11.
- [Python 3.11](https://www.python.org/downloads/) o superiore (necessario per l'installer GUI).
- [Node.js](https://nodejs.org/) v16.6 o superiore (l'installer propone l'installazione automatica della versione LTS se non presente).
- [Git](https://git-scm.com/) per clonare il repository originale.
- Token di un bot Discord con permessi `bot` e `applications.commands`.

### Installazione rapida (consigliata)

1. Assicurati di avere Python 3.11 installato e nel PATH.
2. Clona questo repository o scarica il pacchetto zip e estrailo.
3. Esegui `python installer/setup_gui.py`.
4. Nella finestra GUI:
   - Scegli la cartella di destinazione dove installare SkinPeek.
   - Inserisci il token del tuo bot Discord.
   - Premi **Installa / Aggiorna** e attendi: il programma clonera SkinPeek, generera `config.json` e lancera `npm install`.
5. A installazione completata la finestra passera automaticamente alla modalita dashboard, pronta per avviare il bot.

### Modalita dashboard

- **Setup**: visibile solo la prima volta o quando si sceglie "Apri setup". Permette di modificare percorso e token, reinstallare o aggiornare il bot.
- **Dashboard**: mostra lo stato corrente, i pulsanti **Avvia bot**/**Ferma bot** e un log console in tempo reale. La modalita viene ricordata agli avvii successivi se la configurazione e valida.

### Installazione manuale (alternativa)

Se preferisci non usare l'interfaccia grafica puoi:
1. Clonare manualmente [SkinPeek](https://github.com/giorgi-o/SkinPeek).
2. Copiare `config.json.example` in `config.json` e inserire il token del bot.
3. Eseguire `npm install` e poi `node SkinPeek.js`.

La dashboard di ValorantBuddy puo comunque essere usata in seguito solo per avviare o fermare il processo, puntandola alla stessa cartella.

### Aggiornamenti e manutenzione

- L'installer puo essere rilanciato in qualsiasi momento: se trova un'installazione esistente propone direttamente l'aggiornamento (`git pull` + `npm install`).
- Il file di stato `installer_state.json` viene creato all'interno della cartella `installer/` ed e escluso dal controllo di versione.

### Supporto e contributi

Per suggerimenti, bug o contributi apri una issue su questo repository. Ricordati che il core del bot resta quello di SkinPeek: per problemi specifici al bot consulta anche la documentazione originale.

### Credits

- [SkinPeek](https://github.com/giorgi-o/SkinPeek) di [giorgi-o](https://github.com/giorgi-o) -- progetto originale e cuore funzionale del bot.
- Tutti i contributor di ValorantBuddy per l'interfaccia grafica, l'installer e la documentazione.

## English

### Based on SkinPeek

This project starts as an advanced fork of [SkinPeek](https://github.com/giorgi-o/SkinPeek), the popular Discord bot that surfaces Valorant's daily store, bundles, Night Market and detailed stats. We kept the entire bot core and its features, focusing on a smoother Windows experience.

### Key additions in ValorantBuddy

- **Bundled graphical installer (Tkinter)**: on first run it walks through cloning the original repository, creating `config.json`, and installing all Node.js dependencies.
- **Integrated dashboard**: once setup is complete, the same window turns into a mini dashboard that can start or stop the bot with one click while streaming live logs.
- **State persistence**: ValorantBuddy remembers installation path, configured token, and the current mode so the dashboard is ready on subsequent launches.

### Bot features (inherited from SkinPeek)

- View the daily shop, bundles, Night Market and battle pass without launching the game.
- Create alerts to be notified when a skin appears in the store.
- Handle multiple accounts, keep track of skin history, and translate names to the Valorant locale.
- Provide admin commands for quick configuration and support sharding for large Discord deployments.

### Requirements

- Windows 10/11.
- [Python 3.11](https://www.python.org/downloads/) or newer (required for the GUI installer).
- [Node.js](https://nodejs.org/) v16.6 or newer (the installer can fetch the LTS release automatically).
- [Git](https://git-scm.com/) to clone the original repository.
- Discord bot token with `bot` and `applications.commands` scopes.

### Quick installation (recommended)

1. Ensure Python 3.11 is installed and available in PATH.
2. Clone this repository or download and extract the zip.
3. Run `python installer/setup_gui.py`.
4. In the GUI window:
   - Choose the destination folder for the SkinPeek installation.
   - Paste your Discord bot token.
   - Click **Installa / Aggiorna** and wait while the program clones SkinPeek, generates `config.json`, and runs `npm install`.
5. After installation completes the window automatically switches to dashboard mode, ready to start the bot.

### Dashboard mode

- **Setup**: visible only on first launch or when selecting "Apri setup". Lets you adjust path and token, reinstall or update the bot.
- **Dashboard**: shows current status, provides **Avvia bot**/**Ferma bot** buttons, and streams log output. The mode is remembered for future sessions when configuration is valid.

### Manual installation (alternative)

If you prefer a manual workflow:
1. Clone [SkinPeek](https://github.com/giorgi-o/SkinPeek) yourself.
2. Copy `config.json.example` to `config.json` and add your bot token.
3. Run `npm install` followed by `node SkinPeek.js`.

You can still use ValorantBuddy later just to launch or stop the process by pointing it at the same folder.

### Updates and maintenance

- Run the installer at any time; if an existing setup is detected it automatically performs `git pull` and `npm install`.
- The state file `installer_state.json` lives in the `installer/` directory and is ignored by version control.

### Support and contributions

Open an issue on this repository for suggestions, bugs, or contributions. Remember that the bot core remains SkinPeek: for bot-specific questions, refer to the original documentation as well.

### Credits

- [SkinPeek](https://github.com/giorgi-o/SkinPeek) by [giorgi-o](https://github.com/giorgi-o) -- original project and bot functionality.
- All ValorantBuddy contributors for the graphical installer, dashboard enhancements, and documentation.
