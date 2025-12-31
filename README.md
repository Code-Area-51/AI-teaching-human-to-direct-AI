# Windows System Health & Cleanup Assistant

A Python-based CLI tool to maintain Windows system health by cleaning temporary files, organizing directories, and generating health reports.

## Features

*   **System Cleanup**: Removes temporary files, logs, and browser caches (Chrome, Edge, Firefox).
*   **File Organization**: Organizes Desktop and Downloads folders by file type (Images, Documents, Installers, Archives, Audio, Video, Misc).
*   **System Health Report**: Generates a report including CPU/RAM usage, disk usage, large files, and duplicate files.
*   **Safety First**: Includes a "Dry Run" mode (enabled by default) to preview actions without deleting or moving files.

## Usage

### Prerequisites

*   Python 3.8+
*   Windows OS (for full functionality)

### Installation

1.  Clone the repository.
2.  No external dependencies required (uses standard libraries).

### Commands

Run the assistant from the command line:

```bash
python assistant.py [OPTIONS]
```

#### Options:

*   `--clean`: Clean temp files, logs, and browser caches.
*   `--organize`: Organize Desktop and Downloads folders.
*   `--report`: Generate a system health report.
*   `--dry-run`: (Default) List actions without executing them.
*   `--no-dry-run`: Execute actions (Delete/Move files).

### Examples

**Check what would be cleaned (Dry Run):**
```bash
python assistant.py --clean
```

**Actually clean files:**
```bash
python assistant.py --clean --no-dry-run
```

**Organize Downloads folder:**
```bash
python assistant.py --organize --no-dry-run
```

**Generate System Report:**
```bash
python assistant.py --report
```

## Module Structure

*   `src/cleaner.py`: Handles deletion logic.
*   `src/organizer.py`: Handles file organization logic.
*   `src/reporter.py`: Handles system metrics and reporting.
*   `src/utils.py`: Helper functions (logging, dry-run logic).
*   `assistant.py`: Main CLI entry point.

## Disclaimer
This tool is provided “as is” with no warranties or guarantees. 
Use at your own risk. The author is not responsible for any data loss, 
system issues, or unintended consequences resulting from the use of this software.

## AI Assistance
This project was developed with assistance from AI tools such as Microsoft Copilot and Google Jules.|

## Project Story: AI Teaching Human to Direct AI

This project wasn’t built the traditional way. It wasn’t just “written” — it was orchestrated.  
The Windows System Health & Cleanup Assistant is the result of a workflow where AI didn’t replace the human… it trained the human to direct the AI.

Instead of typing code blindly, the human guided the AI through:

- defining the problem  
- shaping the architecture  
- reviewing the plan  
- approving modules  
- refining logic  
- testing behavior  
- documenting the final product  

Every component — from cleanup logic to reporting — was created through a deliberate back‑and‑forth where the human acted as the engineer, and the AI acted as the accelerator.

This repo captures that process.  
It’s not just a tool — it’s proof of a new skillset:  
**AI orchestration.**  
The ability to think, design, and direct intelligent systems to build real software.

This project stands as a snapshot of that evolution:  
a human learning to command AI, and AI empowering the human to build something bigger than either could alone.


