# ValorantBuddy

> Un assistente che semplifica la gestione del bot Valorant basato su SkinPeek.  
> A companion that makes managing the Valorant bot built on SkinPeek straightforward.

---

## 🇮🇹 Italiano

**ValorantBuddy** è un tool per *Valorant* che permette di visualizzare facilmente il **negozio giornaliero**, il **Night Market** e i **bundle** direttamente da Discord, senza aprire il gioco.  
Il progetto nasce come fork evoluto di [SkinPeek](https://github.com/giorgi-o/SkinPeek) e ne mantiene tutte le funzionalità principali, migliorando l’esperienza d’uso su Windows grazie a un **installer grafico** e una **dashboard integrata**.

### 🆕 Novità introdotte da ValorantBuddy

- 🪟 **Installer grafico (Tkinter)**: guida l’utente nella configurazione iniziale, clonando automaticamente SkinPeek, creando il `config.json` e installando le dipendenze Node.js.  
- 🖥️ **Dashboard integrata**: consente di avviare o fermare il bot con un click e visualizzare i log in tempo reale.  
- 💾 **Persistenza dello stato**: ricorda percorso di installazione, token e modalità, riaprendosi direttamente in dashboard ai successivi avvii.  

### 💡 Funzionalità del bot (derivate da SkinPeek)

- Mostra negozio giornaliero, bundle, Night Market e Battle Pass.  
- Supporta più account e traduce i nomi delle skin nella lingua di Valorant.  
- Permette di impostare alert quando una skin appare nello shop.  
- Include comandi admin e supporta sharding per server di grandi dimensioni.  

---

## 🇬🇧 English

**ValorantBuddy** is an unofficial *Valorant* tool that lets you check your **daily store**, **Night Market**, and **bundles** right from Discord — no need to open the game.  
It’s built as an advanced fork of [SkinPeek](https://github.com/giorgi-o/SkinPeek), keeping its full functionality while adding a **graphical installer** and an **integrated dashboard** for a smoother Windows experience.

### 🆕 Key Additions in ValorantBuddy

- 🪟 **Graphical Installer (Tkinter)**: automatically clones SkinPeek, generates the `config.json`, and installs Node.js dependencies.  
- 🖥️ **Integrated Dashboard**: lets you start/stop the bot with one click and view live logs.  
- 💾 **State Persistence**: remembers installation path, bot token, and mode, reopening directly into the dashboard on next launch.  

### 💡 Bot Features (from SkinPeek)

- View daily shop, bundles, Night Market, and Battle Pass without launching Valorant.  
- Handle multiple accounts and translate skin names to your locale.  
- Set up alerts when a specific skin appears.  
- Includes admin commands and sharding support for large Discord servers.  

---

## 🧩 Badges

[![GPLv3 License](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)  
![GitHub last commit](https://img.shields.io/github/last-commit/Ho3pLi/ValorantBuddy)  
![GitHub repo size](https://img.shields.io/github/repo-size/Ho3pLi/ValorantBuddy)  

---

## ⚙️ Requisiti / Requirements

- Windows 10 / 11  
- [Python 3.11+](https://www.python.org/downloads/)  
- [Node.js 16.6+](https://nodejs.org/)  
- [Git](https://git-scm.com/)  
- Discord bot token con permessi `bot` e `applications.commands`  

---

## 🚀 Installazione & Utilizzo / Installation & Usage

### 🇮🇹 Italiano

1. Assicurati di avere **Python 3.11** nel PATH.  
2. Clona questo repository o scarica lo zip.  
3. Esegui `python installer/setup_gui.py`.  
4. Nella GUI:
   - Scegli la cartella di installazione di SkinPeek.  
   - Inserisci il token del tuo bot Discord.  
   - Premi **Installa / Aggiorna** e attendi la configurazione automatica.  
5. Al termine, la finestra passerà alla **dashboard** per avviare o fermare il bot.

### 🇬🇧 English

1. Make sure **Python 3.11** is installed and available in PATH.  
2. Clone this repo or extract the zip.  
3. Run `python installer/setup_gui.py`.  
4. In the GUI:
   - Select the installation folder for SkinPeek.  
   - Enter your Discord bot token.  
   - Click **Install / Update** and wait for setup.  
5. Once complete, the window switches to **dashboard mode** — ready to start the bot.  

---

## 🧰 Aggiornamenti / Updates

- L’installer può essere rilanciato in qualsiasi momento: se trova un’installazione esistente, propone l’**aggiornamento automatico** (`git pull` + `npm install`).  
- Il file `installer_state.json` salva lo stato locale ed è ignorato dal controllo di versione.  

---

## 💬 Supporto / Support

For issues, suggestions, or contributions:  
📧 **daniele.barile.lavoro@gmail.com**  
or open an issue directly on this repository.  

Remember: ValorantBuddy builds on **SkinPeek**, so for core bot issues refer to its [original documentation](https://github.com/giorgi-o/SkinPeek).  

---

## 🪄 Licenza / License

[GPL v3](https://choosealicense.com/licenses/gpl-3.0/)

---

## 👥 Autori / Authors

- [@Ho3pLi](https://github.com/Ho3pLi) — maintainer & GUI/dashboard developer  
- [@giorgi-o](https://github.com/giorgi-o) — creator of the original **SkinPeek** project  
