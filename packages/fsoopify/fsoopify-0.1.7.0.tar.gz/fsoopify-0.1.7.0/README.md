# fsoopify

Just make file system oopify.

## install

``` cmd
pip install fsoopify
```

## usage

``` py
import fsoopify

file/folder = fsoopify.NodeInfo.from_path(...)

fp = file.open() ...
file.read_alltext() ...
file.read_allbytes() ...
file.copy_to() ...

folder.list_items() ...
```
