# pyequa

Equations on the move.

## Project root

Set project root in **linux**

Add to `~/.bashrc` or `~/.bash_profile` (or `~/.zshrc`):

```bash
export PYEQUA_PROJECT_ROOT="/home/some_user/Documents/my_pyequa_project"
```

Set project root in **windows**

Command to do once:

```powershell
[Environment]::SetEnvironmentVariable("PYEQUA_PROJECT_ROOT", "C:\Users\some_user\Documents\my_pyequa_project", "User")
```

Check in **Python**:

```python
import os
root_path = os.getenv("PYEQUA_PROJECT_ROOT", "default_if_missing")
print(root_path)
```

## Debug

**Potencial problems**

* Close ALL vscode windows or projects after running `[Environment]::SetEnvironmentVariable(...)`.

**Use examples**

To use exercises in folder `examples` inside package files:

1. In a terminal (powershell):

```powershell
[Environment]::SetEnvironmentVariable("PYEQUA_PROJECT_ROOT", "C:\Users\some_user\Documents\pyequa\examples", "User")
```

2. Close all `vstudio` sessions

3. Open pyequa folder

4. Open an example `producer.py` file:

```
...\pyequa\examples\determinant\producer.py
``` 




