# Windows System Health & Cleanup Assistant

A Python-based CLI tool to maintain Windows system health by cleaning temporary files, organizing directories, and generating detailed system health reports. Built using a hybrid human–AI engineering workflow combining Microsoft Copilot, Google Jules, and traditional development tools.

---

## 🚀 Features

### 🧹 System Cleanup
- Removes temporary files, logs, and leftover installer fragments  
- Clears browser caches (Chrome, Edge, Firefox)  
- Cleans Windows temp directories safely  

### 🗂 File Organization
- Organizes Desktop and Downloads folders by file type  
- Categories include Images, Documents, Installers, Archives, Audio, Video, and Misc  
- Supports **Dry Run mode** to preview changes before applying them  

### 📊 System Health Report
- CPU and RAM usage  
- Disk usage and free space  
- Large file detection (>100MB)  
- Duplicate file detection  
- Timestamped logs  

### 🛡 Safety First
- **Dry Run mode enabled by default**  
- No files are deleted or moved unless `--no-dry-run` is used  
- All actions logged for transparency  

---

## 🧠 AI-Assisted Development

This project was developed using a multi‑AI orchestration workflow:

- **Microsoft Copilot** — architectural guidance, debugging support, documentation, and workflow design  
- **Google Jules** — code generation, refinement, and iterative module development  

The human remained the engineer in control, directing the AI systems through:

- defining the problem  
- shaping the architecture  
- reviewing plans  
- approving modules  
- refining logic  
- testing behavior  
- documenting the final product  

This repository captures that process.  
It’s not just a tool — it’s proof of a new skillset:

### **AI Orchestration**  
The ability to think, design, and direct intelligent systems to build real software.

---

## 📦 Installation

### Prerequisites
- **Python 3.12+** (recommended)  
- **Windows 10/11** for full functionality  
- No external dependencies required (uses Python standard libraries)

### Clone the Repository
```
git clone https://github.com/YOUR-USERNAME/AI-teaching-human-to-direct-AI.git
cd AI-teaching-human-to-direct-AI
```

---

## ▶️ Usage

Run the assistant from the command line:

```
python assistant.py [OPTIONS]
```

### Options
- `--clean` — Clean temp files, logs, and browser caches  
- `--organize` — Organize Desktop and Downloads folders  
- `--report` — Generate a system health report  
- `--dry-run` — Preview actions without executing them (default)  
- `--no-dry-run` — Execute actions (delete/move files)  

### Examples

#### Preview cleanup (Dry Run)
```
python assistant.py --clean
```

#### Perform actual cleanup
```
python assistant.py --clean --no-dry-run
```

#### Organize Downloads folder
```
python assistant.py --organize --no-dry-run
```

#### Generate a system report
```
python assistant.py --report
```

---

## 🧩 Module Structure

- `src/cleaner.py` — Handles deletion logic  
- `src/organizer.py` — Handles file organization logic  
- `src/reporter.py` — Handles system metrics and reporting  
- `src/utils.py` — Helper functions (logging, dry-run logic)  
- `assistant.py` — Main CLI entry point  

---

## 📘 Project Story: *AI Teaching Human to Direct AI*

This project wasn’t built the traditional way.  
It wasn’t just “written” — it was **orchestrated**.

The Windows System Health & Cleanup Assistant is the result of a workflow where AI didn’t replace the human…  
**it trained the human to direct the AI.**

Every component — from cleanup logic to reporting — was created through a deliberate back‑and‑forth where:

- the human acted as the engineer  
- the AI acted as the accelerator  

This project stands as a snapshot of that evolution:

> **A human learning to command AI, and AI empowering the human to build something bigger than either could alone.**

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ⚠️ Disclaimer

This tool is provided “as is” with no warranties or guarantees.  
Use at your own risk.  
The author is not responsible for any data loss, system issues, or unintended consequences resulting from the use of this software.

---

## 👤 Author

**James**  
Cybersecurity & IT Support Student  
Windows Troubleshooting | Automation | AI‑Assisted Development  

