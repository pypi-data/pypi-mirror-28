# SG Markets Plot


## 1- Introduction

This repo is a helper package for clients (and employees) to plot slices (1-D, 2-D or 3-D) of data obtained from SG Markets APIs.  
Naturally it can also be used with any data store in a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).  


## 2 - Install

From terminal:
```bash
# download and install package from pypi.org
pip install sgmarkets_plot
```


## 3 - User guide

### 3.1 - Make an API call

Read the demo notebooks for various APIs in the same gitlab [sgmarkets organization](https://gitlab.com/sgmarkets).  
There you can see how to get data from an SG Markets API.  


### 3.2 - Plot a data slice

Then you can display a 1-D or 2-D slice with a number of plot functions.  
By default SG Colors are used (except for 3-D graphs).


```python
# examples - see ROTB demo notebook for the context

# line(s) plot
Plot.line(s1.df_pivot, figsize=(14, 6), title='Slice 1')

# heatmap
Plot.heatmap(s1.df_pivot, title='Slice 1', cmap='YlGnBu', figsize=(8, 8))

# surface
Plot.surface3D(s1.df_pivot, z_label='volNormal', z_round=4)

# dynamic chart with dates on x axis
Plot.highstock(s4.df_pivot, title='volNormal')
```
