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

# file api
file.open()
file.size
file.read() and file.write()
file.read_text() and file.write_text()
file.read_bytes() and file.write_bytes()
file.copy_to()
file.delete()
file.create_hardlink()
file.load() and file.dump()

# folder api
folder.create() and folder.ensure_created()
folder.list_items()
folder.get_fileinfo() and folder.create_fileinfo()
folder.delete()
folder.create_hardlink()
```
