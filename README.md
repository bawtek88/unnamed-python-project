# Hadron-Project

## Setup

```bash
# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the simulation
python src/main.py
```

## Dependencies

All dependencies are listed in the [`requirements.txt`](requirements.txt) file.

- **pygame** - Graphics and event handling
- **pygame_gui** - UI components

## Settings

All game settings are located in the [`settings.py`](src/settings.py) file.

## Debug Mode

Aim of the built-in debug mode is to provide a possibility of inspecting and modifying in-game objects and values at runtime. It allows for the use of a command console to execute predefined commands.

### How to Enable

In the [`settings.py`](src/settings.py) file, set the `DEBUG_MODE` variable to `True`. After enabling debug mode, you can toggle the debug console in-game by pressing the `~` (backquote/tilde key).

### Currently Available Commands

- `help` - Lists all available commands with descriptions.
- `clear` - Clears the console output.
- `fpslimit` - Displays the current FPS limit setting.
- `screensize` - Displays the current screen resolution.
- `playerstats` - Displays the player's current stats (health, stamina, shield, speed).

Console keeps a history of entered commands, which can be navigated using the up and down arrow keys.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
