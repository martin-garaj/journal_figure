**journal_figure** is a library contains functions for making figures for journal publishing.

---
Initial commit:
```console
git remote add origin https://github.com/martin-garaj/journal_figure.git
git branch -M main
git push -u origin main
```

---
update PV_lib from local:
```console
cd ~
cd ./Desktop/CloudStorage/Projects/Journal_figure/repo/journal_figure
git add --all
git diff --cached --name-only
git commit -m "README update"
git push -u origin main
```

---
*Forced* push
```console
git push --set-upstream origin main -f
```

---
install PV_lib from GitHub (system-wise from console):
```console
conda activate python3.9
python -m pip install git+https://github.com/martin-garaj/journal_figure.git@main
conda deactivate
```

---
**RE**install PV_lib from GitHub (system-wise from console):
```console
conda activate python3.9
python -m pip install git+https://github.com/martin-garaj/journal_figure.git@main --force-reinstall
conda deactivate
```


---
**UN**install PV_lib from local (system-wise from console):

```console
conda activate python3.9
python -m pip uninstall journal_figure
conda deactivate
```


Example plot:
![pretty_style_v1](pretty_style_v1.png)


