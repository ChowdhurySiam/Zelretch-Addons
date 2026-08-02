# Zelretch Addons

<p align="center"><img src="assets/Zelretch.jpg" alt="Zelretch Addons" width="100%"></p>

Official addon collection for **Zelretch**.

- **Source:** `https://github.com/SiamTestingProject/Addons`
- **Maintainer:** [Siam Chowdhury](https://github.com/ChowdhurySiam)
- **Telegram:** [@Ch0wdhury_Siam](https://t.me/Ch0wdhury_Siam)
- **Default prefix:** `.`

## Separate-project design

This repository contains addons only. The Zelretch deployment core remains a separate project and synchronizes this repository automatically during startup. Addon source files are not bundled into the main repository.

## Automatic loading

Zelretch downloads the `main` branch, validates every Python file, stores the active addon cache in MongoDB, and loads compatible addons automatically. No additional enable switch is required because `AUTO_ADDONS=true` is the built-in default.

## Command-center design

Every addon provides a clean `ZELRETCH_MODULE_INFO` metadata block. Zelretch uses that metadata to render a consistent inline command center with an icon, category, plain-language description, and command syntax.

## Module catalog

### Administration

| Module | Description | Commands |
|---|---|---|
| 🛡️ **Chat Administration** | Provides chat IDs, permissions, moderation, roles, links, and group-management tools. | `.id [reply]`, `.rights [-u username/id]`, `.leave`, `.pin [reply]`, `.unpin [reply]`, `.unpinall`, `.admins`, `.ban [reply] [duration]`, `.unban [reply]`, `.kick [reply]`, `.mute [reply] [duration]`, `.unmute [reply]`, `.rename [name]`, `.create [-g|--group name] [-c|--channel name]`, `.geturl [reply]`, `.addrole -n role_name -p число`, `.delrole -n role_name`, `.roles [-n role_name]`, `.chatinfo` |
| 🙈 **Ignore User** | Suppresses selected incoming messages from a specified user or chat. | `.ignore [user_id/@username]` |
| 🧹 **Member Cleanup** | Performs bulk member cleanup actions in chats where you have permission. | `.kickall`, `.kickall_hide`, `.kickall_withbot`, `.kickdeleted` |
| 📢 **Mention All** | Mentions chat members sequentially or in grouped batches. | `.tagallone [delay] [text]`, `.tagall [delay] [text]` |
| 🗑️ **Message Cleanup** | Deletes a replied message or a selected message range. | `.del [reply]`, `.purge [reply/group_id] [start_id] [stop_id]` |

### AI & Automation

| Module | Description | Commands |
|---|---|---|
| 🤖 **AI Gateway** | Sends prompts to supported OpenRouter models from a single command. | `.ai [Gemini/DeepSeek/Qwen] [message]` |
| ✨ **Gemini AI** | Connects to Google Gemini for prompts, conversations, model selection, and history control. | `.gemini [text]`, `.gemini_api [api_key]`, `.gemini_model [model]`, `.gemini_chat [text]`, `.gemini_clear` |

### Automation

| Module | Description | Commands |
|---|---|---|
| 💬 **Auto Answer** | Configures automatic replies using a selected message or post. | `.aws [ID/Username] [Post ID]` |
| 👁️ **Auto Read** | Automatically marks messages as read in configured chats. | `.autoread` |
| 🟢 **Presence Control** | Keeps the account online or returns it to normal presence behavior. | `.online`, `.offline` |
| 🎟️ **Promo Claimer** | Monitors supported promo messages and attempts eligible token redemptions. | `.checktokens` |

### Community

| Module | Description | Commands |
|---|---|---|
| ⭐ **Reputation** | Tracks simple positive and negative reputation reactions in a chat. | `.rep [number]` |

### Creative

| Module | Description | Commands |
|---|---|---|
| 🎭 **Patriot Text** | Transforms text with a stylized character-substitution effect. | `.patriot`, `.pat [reply]` |

### Developer Tools

| Module | Description | Commands |
|---|---|---|
| 🧩 **Module Bridge** | Converts compatible legacy modules into the Zelretch addon format. | `.module_bridge [Link/Reply]`, `.module_bridge_config [Model]` |

### Files & Media

| Module | Description | Commands |
|---|---|---|
| 🖼️ **Demotivator** | Creates a demotivational-style image from replied media and custom text. | `.dem [text]` |
| 🎞️ **Media to GIF** | Converts replied photos or videos into an optimized GIF. | `.media2gif [reply to photo or video]` |
| ☁️ **Multi Uploader** | Uploads replied files to multiple temporary file-hosting services. | `.catbox`, `.envs`, `.kappa`, `.0x0`, `.x0`, `.tmpfiles`, `.pomf`, `.bash` |
| 📌 **Pinterest Downloader** | Extracts and downloads supported Pinterest images or videos. | `.pinterest [link]` |
| 💬 **Quote Maker** | Creates a quote image from a replied Telegram message. | `.q [reply]` |
| 📥 **Social Downloader** | Downloads supported social-media videos from a supplied URL. | `.tt [url]` |
| 📡 **Stream Utilities** | Provides supported streaming and media-link utilities. | `.stream` |
| 🔊 **Text to Speech** | Converts supplied text into an audio message in supported languages. | `.voice [text]`, `.voice_ru [text]` |
| 📸 **Website Screenshot** | Captures a screenshot of a supplied web page. | `.webshot [url]` |

### Fun

| Module | Description | Commands |
|---|---|---|
| 🎲 **Aurora Bull** | Creates randomized playful text sequences and timed message loops. | `.abull`, `.abullspam [time] [text]`, `.abulloff` |
| 💬 **Bull Text** | Generates randomized dramatic text for entertainment. | `.bull`, `.bulli` |
| 🎯 **Chance Meter** | Generates a playful probability score for any question or phrase. | `.chance [text]` |
| 🧾 **Fictional Profile Generator** | Creates a fictional profile card for entertainment and testing. | `.doxx` |
| 🎬 **Fun Animations** | Runs a collection of harmless animated text sequences. | `.hack`, `.drugs`, `.police [duration]`, `.ghoul`, `.stupid`, `.bombs`, `.call`, `.kill`, `.ZV` |
| 💗 **Heart Animation** | Displays an animated heart sequence in the current message. | `.hearts`, `.magic`, `.love` |
| 🐱 **Neko Text Mode** | Adds a configurable neko-style transformation to outgoing text. | `.nekoed [on/off]` |
| 💠 **Premium Text** | Transforms supported characters into premium-emoji styled text. | `.prem_text [text]` |
| 📊 **Progress Animation** | Displays an animated progress bar with optional custom text. | `.progressbar [text]` |
| 🪜 **Text Ladder** | Builds an animated ladder pattern from custom text. | `.ladder [text]` |
| 🔄 **Text Switch** | Applies a reversible visual transformation to replied or supplied text. | `.sw [reply|text]` |
| ⌨️ **Typing Animation** | Animates supplied text as though it is being typed. | `.type [text]` |
| ⏳ **Wait Animation** | Displays a short animated waiting sequence. | `.wait` |

### Information

| Module | Description | Commands |
|---|---|---|
| ⛅ **Advanced Weather** | Provides detailed weather data with optional API configuration. | `.weather [city]`, `.weather_config [api_key]`, `.weather_help` |
| 💱 **Currency Converter** | Converts amounts between configured currencies using current exchange data. | `.cr [amount] [currency]`, `.currency_config [currencies]` |
| 📚 **History Facts** | Returns random historical, science, music, and general-interest facts. | `.rfact`, `.hfact`, `.mfact`, `.sfact` |
| 🌐 **IP Information** | Displays location, network, timezone, and provider data for an IP address. | `.ipi [ip]`, `.ipinfo [ip]` |
| 🔎 **Public OSINT Lookup** | Queries supported public OSINT sources for a supplied phone number. | `.eye [phone]`, `.osint [phone]` |
| 🕵️ **Username Search** | Checks a username or identifier across supported public services. | `.sher [query]` |
| 🌦️ **Weather** | Shows a text forecast and weather image for a city. | `.weather [city]` |
| 📖 **Wikipedia Search** | Searches Wikipedia in the selected language and returns a summary. | `.wiki [RU/EN] [WORD]` |

### Media

| Module | Description | Commands |
|---|---|---|
| 🌸 **Anime Character** | Fetches random anime character images by category. | `.waf [category]` |
| 🎧 **Last.fm Status** | Displays and optionally auto-updates your currently playing Last.fm track. | `.lastfm_api [api_key]`, `.nowplayed`, `.lastfm_config [LastFM Nickname] [Username/ID Channel] [ID Message] [Autostart: True/False]`, `.autoplayed` |
| 🖼️ **Media Gallery** | Fetches images from several supported themed media sources. | `.anime`, `.cat`, `.lolic`, `.loli`, `.lolih`, `.fem`, `.sfw`, `.furry`, `.nsfw` |
| 🎵 **Music Finder** | Finds lyrics and music results across supported providers. | `.genius_config [api_token]`, `.l [song_name]`, `.lyrics [song_name]`, `.dm [song_name]`, `.dmusic [song_name]`, `.lm [song_name]`, `.lmusic [song_name]` |
| 🐾 **Neko Media** | Fetches a random neko-themed image. | `.neko` |

### Productivity

| Module | Description | Commands |
|---|---|---|
| 🌙 **AFK Manager** | Sets an away status, records the reason, and responds to mentions until you return. | `.afk [reason]`, `.unafk` |
| ✅ **Task Manager** | Creates, lists, prioritizes, and removes personal tasks. | `.td [importance:int] [task]`, `.tdl`, `.utd [task_id]` |

### Restricted Tools

| Module | Description | Commands |
|---|---|---|
| 🔞 **Adult Media Search** | Searches an adult-content provider by tags; use only where lawful and appropriate. | `.rule34 [tags]` |
| 📣 **Bulk Messaging** | Sends repeated text or sticker messages with configurable count and delay. | `.stspam [count] [delay] [sticker_id]`, `.spam [count] [delay] [text]`, `.help_spam` |
| ⚠️ **Legacy Stress Tools** | Provides legacy stress-test commands; use only with explicit authorization. | `.bomber`, `.sbomber` |

### System

| Module | Description | Commands |
|---|---|---|
| 🚀 **Speed Test** | Measures network download, upload, and latency information. | No public command |
| 🖥️ **System Information** | Displays CPU, memory, disk, platform, and runtime information. | `.sysinfo` |
| ⚙️ **Systemd Manager** | Lists and manages systemd units on compatible Linux hosts. | `.units`, `.addunit [unit] [name]`, `.delunit [unit]`, `.unit [unit] [action]`, `.nameunit [unit] [new_name]` |

### Telegram Tools

| Module | Description | Commands |
|---|---|---|
| 🪪 **Account Insights** | Displays detailed public information and activity estimates for a Telegram account. | `.aboutacc [username/reply]` |
| 📈 **Account Statistics** | Shows Telegram dialog, contact, group, and channel statistics. | `.stat`, `.stats` |
| 🆔 **Chat ID Finder** | Shows the current chat identifier and related Telegram IDs. | `.id` |
| 📱 **Client Detector** | Estimates which Telegram client a user is using from public message data. | `.telega [reply/@username/id]` |
| 📊 **Detailed Statistics** | Provides an expanded summary of account and dialog statistics. | `.stats_xdesai` |
| 📨 **Direct Sender** | Sends replied content to a Telegram ID or username. | `.send [ID/Username]` |
| 💎 **Fragment Checker** | Checks supported Telegram Fragment username information. | `.fcheck [username]` |
| 🛡️ **Spam Protection Check** | Checks the current account against supported Telegram spam restrictions. | `.spamban` |
| 👤 **User Information** | Displays concise or detailed public information about a Telegram user. | `.user_info [user_id/@username]`, `.user_info_full [user_id/@username]` |

### Utilities

| Module | Description | Commands |
|---|---|---|
| 🕒 **Current Time** | Shows the current date and time. | `.time` |
| 🔐 **Password Generator** | Generates a random password with the requested length. | `.gen_password [length]` |
| 🔳 **QR Generator** | Generates a QR code from supplied text or a link. | `.qr [text]` |
| 🎲 **Random Number** | Generates a random number using configurable minimum and maximum values. | `.rnd [min] [max]`, `.randomizer_config [min] [max]` |
| 🔗 **Rich Link Builder** | Creates safe clickable text using a validated HTTP or HTTPS URL and label. | `.link [url] [text]` |
| 🗝️ **Subscription Key Extractor** | Parses supported subscription links and extracts available connection keys. | `.get_keys [link to sub]` |
| 🧭 **URL Inspector** | Expands shortened URLs and displays resolved host or IP information. | `.expandurl [URL]`, `.ipurl [URL]` |
| ✂️ **URL Shortener** | Creates a shortened link from supplied or replied text. | `.short [Reply/Link]` |

## Optional service credentials

Some addons connect to third-party services. Keep credentials in environment variables or save them through the provided configuration command; no third-party credential is embedded in this repository.

| Variable | Used by | Alternative command |
|---|---|---|
| `GENIUS_API_TOKEN` | Music Finder lyrics search | `.genius_config YOUR_TOKEN` |
| `LASTFM_API_KEY` | Last.fm status | `.lastfm_api YOUR_KEY` |
| `OPENWEATHER_API_KEY` | Advanced Weather | `.weather_config YOUR_KEY` |
| `TELEGA_CALLS_API_KEY` | Client Detector | Environment variable only |

## Addon requirements

1. Target Python 3.11 and Kurigram.
2. Import `zel_command` and `zel_sudo` from `command.py`.
3. Include a clear `ZELRETCH_MODULE_INFO` block.
4. Keep credentials in environment variables or MongoDB-backed configuration; do not hardcode tokens.
5. Compile the module before submitting it.

## Credits

- **Maintainer:** [Siam Chowdhury](https://github.com/ChowdhurySiam)
- **Telegram:** [@Ch0wdhury_Siam](https://t.me/Ch0wdhury_Siam)

License notices embedded in individual modules are retained where applicable.


## Dependency installation

The shared `requirements.txt` file lists the maintained Addons dependencies. Zelretch 3.0.2 installs these during the Docker build and skips already satisfied packages at runtime, preventing repeated upgrades and dependency downgrades.

The Gemini Addon uses the supported `google-genai` SDK and defaults to `gemini-2.5-flash`.
