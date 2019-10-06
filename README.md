# Nintendo GameCube GOG Galaxy 2.0 Integration

A GOG Galaxy 2.0 integration with the Dolphin emulator.
This is a fork of my Wii plugin and that is a fork of AHCoder (on GitHub)'s PCSX2 GOG Galaxy Plugin edited for support with Dolphin! 

Thank you AHCoder for the original program, and the GamesList and XML files 
is from GameTDB.

You can find GameTDB here: https://www.gametdb.com/

## Setup:
Just download the file [here](https://github.com/JTNDev/galaxy-integration-gc/releases) and extract the ZIP into:
- Windows:

    `%localappdata%\GOG.com\Galaxy\plugins\installed`

- macOS:

    `~/Library/Application Support/GOG.com/Galaxy/plugins/installed`

Open up user_config.py and edit the ROM and Dolphin location
Make sure you use "/" instead of "\\" for the file paths

Go into GOG Galaxy 2.0, click on integrations and connect the one with "Nintendo Game Cube" 
and you're done.

## Limitations:

All ROMs must be in the same folder, no subfolders, and also the name of the ROM must be equivalent to its counterpart in GamesList.txt. You can look up the name in GamesList.txt and edit it accordingly.
Example:
To add the game The Legend of Zelda: Twilight Princess, you can look it up in GamesList.txt:
```
...
RZDE01 = The Legend of Zelda Twilight Princess
...
```
Therefore the ROM file must be named "The Legend of Zelda Twilight Princess.iso".

If one item in the folder cannot be recognized by the program, none of them can. You can have files with different file extensions in the same folder but if you have for example, "Kingdom Hearts.iso" in the same folder none of them will be registered in GOG Galaxy 2.0.
