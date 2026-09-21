# Seagull Scaring V2 (PyQt5)
By Gabriel Alonso-Holt.

This repo ~~is~~ was a scrapped rewrite of Seagull Scaring V2 using PyQt5. It is currently WIP and not as feature-complete as its Tk counterpart.

The days of having me run around scaring seagulls manually are over! With Seagull Scaring, you can just start the program, choose a time to scare seagulls for, and relax as the seagulls fly away when you want.

Recommended settings: 2700 seconds (timer), 60 seconds (min time), 300 seconds (max time), seagull (sound).

### Install instructions
1. Download the latest release from the "Releases" page.  
2. Run the `SSV2-Qt5_Setup.exe` file as administrator.  
3. Follow the on-screen instructions to install.  
4. Launch the program from the shortcut. If you also have the regular Tk edition installed, you can tell the difference because the shortcut for this version says "Qt Edition" in brackets.  

### Manual install instructions
1. Unzip the program folder.
2. Run `install.bat` to set up the virtual environment and install dependencies.
3. Copy a `media.zip` to the program folder, run `main.pyw`, click "about" and then click "extract gull effects".

### If installer does not work:
1. Run this command to create a virtual environment: `python -m venv .venv`
2. Activate the environment: `.venv\Scripts\activate.bat`
3. Install dependencies: `pip install -r requirements.txt`
4. Run program: `python main.pyw`