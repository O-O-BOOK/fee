# Env verification workspace

This directory is a minimal workspace for validating the local package index
with Env.

Typical command from this directory:

```powershell
$env:ENV_ROOT='C:\Work\InstallTools\env-windows'
$env:PKGS_ROOT='C:\sourcedata\custom_fee\package-index'
$env:PKGS_DIR=$env:PKGS_ROOT
& 'C:\Work\InstallTools\env-windows\.venv\Scripts\pkgs.exe' --list
```
