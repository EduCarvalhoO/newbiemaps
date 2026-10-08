# NewbieMaps

A small, free map companion for Windows. It shows where you are, which way you're facing, the extracts and your quest objectives next to Escape from Tarkov, without touching the game.

This repository only hosts **downloads and release notes**. The app source code is not public.

## Download

Get the latest version from the [Releases page](../../releases/latest).

| File | What it is |
|---|---|
| `NewbieMaps-<version>-win-x64.zip` | Unzip and run |
| `NewbieMaps-<version>-win-x64.msi` | Installer |
| `SHA256SUMS.txt` | Checksums of the files above |

Requires Windows 10 or 11, 64-bit.

### Check your download

Open PowerShell in the folder with the file and run:

```powershell
Get-FileHash .\NewbieMaps-<version>-win-x64.zip -Algorithm SHA256
```

The value must match the line for that file in `SHA256SUMS.txt`.

### Windows warning

The first versions are not code-signed, so Windows SmartScreen may show an "unknown publisher" warning. Compare the SHA-256 before you run the file.

## What it does and doesn't do

It reads only the file names of the screenshots the game saves and the log files the game writes. It does not read the game's memory, does not read or change its DLLs, does not inject code or edit game files, does not show other players, and does not send your data to any server.

Using any third-party tool is at your own risk.

## Problems or ideas

Open an [issue](../../issues/new/choose). **Please don't paste full game logs**: they can contain account identifiers.

## Disclaimer

NewbieMaps is not affiliated with, endorsed or sponsored by Battlestate Games. Escape from Tarkov and related marks belong to their owners and are only mentioned to show what the app works with.
