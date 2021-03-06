## Welcome to Amarula Open Source wiki

### Sphinx Usage

```bash
	usage: sphinx-build [OPTIONS] SOURCEDIR OUTPUTDIR [FILENAMES...]
	
```

### To build this document, run this command 

`sphinx-build  ./  _build/`

Once above comamnd run successfully, a `Makefile` would generated.

On next time onward we can use generated `Makefile` to build the document

`make html`

### Layout of Documentation
```
.
├── bsp
│   ├── allwinner
│   │   ├── a13
│   │   ├── a20
│   │   ├── a64
│   │   ├── h3
│   │   ├── h5
│   │   └── h6
│   ├── imx6
│   │   ├── biticino
│   │   └── imx6qdl
│   └── rockchip
│       ├── rk3288
│       └── rk3399
├── giotto_tune
├── multimedia
├── os_automatic_testing
├── risc_v
├── uboot
│   ├── boot_time
│   ├── falcon_mode
│   ├── image_boot
│   ├── image_build
│   └── secure_boot
└── yocto

87 directories
```

### Sphinx Documentation

For sphinx-document and syntax refer [this link](https://www.sphinx-doc.org/en/master/contents.html)
Here is small [sphinx cheatsheet](https://matplotlib.org/sampledoc/cheatsheet.html)

