**journal_figure** is a library for journal-level data plotting.
The library comes with examples and pre-defined styles. 

Example figure:
![pretty_style_v1](pretty_style_v1.png)

---
**Install** journal_figure from GitHub (system-wise from console):
```console
python -m pip install git+https://github.com/martin-garaj/journal_figure.git@main
```

---
**RE**install journal_figure from GitHub (system-wise from console):
```console
python -m pip install git+https://github.com/martin-garaj/journal_figure.git@main --force-reinstall
```

---
**UN**install journal_figure from local (system-wise from console):

```console
python -m pip uninstall journal_figure
```

---
**How to get the Example figure:**

```python
import journal_figure as jp
# use help(jf.<function name>) when in doubt.

# close any previous figure
plt.close('all')

# create figure
figure = plt.figure(1)
# add main axes
axes = figure.add_axes([0.10,0.10,0.80,0.80])
# add axis for detail
detail_ax = figure.add_axes([0.40,0.40,0.20,0.20])
## axes limits
limX = [-0.5, 49.5]
limY = [-1.1, 1.1]
# pick colormap
colormap= 'viridis'
# number of data plotted
resolution = 5

# apply specific style
jf.set_style(style='pretty_style_v1', apply_to=['figure', 'fonts', 'grid', 'ticks', 'legend'])

# get colormap function
cmap = plt.get_cmap(colormap,resolution)

# plot data
for idx in range(0, resolution):
    axes.plot( ((idx+0.3)/resolution)*np.sin(np.linspace(0, 2 * np.pi)), color=cmap(idx), label = 'Line '+str(idx+1))
    detail_ax.plot( ((idx+0.3)/resolution)*np.sin(np.linspace(0, 2 * np.pi)), color=cmap(idx))

# set ticks position
axes.xaxis.set_major_locator(MultipleLocator(10))
axes.yaxis.set_major_locator(MultipleLocator(0.5))
axes.xaxis.set_minor_locator(MultipleLocator(1))
axes.yaxis.set_minor_locator(MultipleLocator(0.05))
axes.xaxis.set_ticks_position('both')
axes.yaxis.set_ticks_position('both')

detail_ax.xaxis.set_major_locator(MultipleLocator(1))
detail_ax.yaxis.set_major_locator(MultipleLocator(0.1))
detail_ax.xaxis.set_minor_locator(MultipleLocator(1))
detail_ax.yaxis.set_minor_locator(MultipleLocator(0.05))
detail_ax.xaxis.set_ticks_position('both')
detail_ax.yaxis.set_ticks_position('both')

# set ticks format
axes.xaxis.set_major_formatter('${x:.0f}$')
axes.yaxis.set_major_formatter('${x:.1f}$')

# set detail
jf.pretty_detail_axis(axes,
                   detail_ax,
                   main_limits=[limX, limY],
                   detail_limits=[[21.5, 27.5],[-0.35, 0.35]],
                   detail_pos=[[5, 20],[-0.9, -0.1]],
                   connections=[{'connector_detail':'NE', 'connector_detail_ax':'NE'}, {'connector_detail':'SW', 'connector_detail_ax':'SW'}],
                   line_setting = {'linestyle':'-', 'color':'black', 'linewidth':1.0, 'alpha':1.0} )

# enable grid
axes.grid('on')

# set figure size
jf.set_figure_size(20,12,axes)

# add legend
label_order = [[ 1 , 2 , 3],
              ['e', 0 , 4 ]]
jf.pretty_legend(axes, position=[1.03, 1.05], label_order=label_order, title='$Legend \; \Omega$')

```



**Some personal notes:**

---
Initial commit:
```console
git remote add origin https://github.com/martin-garaj/journal_figure.git
git branch -M main
git push -u origin main
```

---
update journal_figure from local:
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
Reminedr to set proper conda environment:
```console
conda activate python3.9
conda deactivate
```




