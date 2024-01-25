## Welcome to Amarula Open Source wiki

### Sphinx Setup (UBUNTU)

Install the following package in order to build the project

```bash
    sudo apt-get install python3-sphinx
    pip install sphinx_rtd_theme --break-system-packages
```

### Sphinx Usage

```bash
	usage: sphinx-build [OPTIONS] SOURCEDIR OUTPUTDIR [FILENAMES...]
	
```

### To build this document, run this command 

`sphinx-build  ./  _build/`

Open the result using firefox/chrome browser

```bash
    firefox _build/index.html
```

You can build it again using the same command

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

