## Welcome to Amarula Open Source wiki

At Amarula Solutions, we pride ourselves on our commitment to excellence, utilizing
the latest technologies and methodologies to stay at the forefront of the industry.
Our team of highly skilled engineers and developers has a wealth of experience
working on complex software projects, and we have a proven track record of
delivering exceptional results.

Our services include software development, hardware design, and consulting services,
all aimed at helping businesses improve their processes, increase efficiency,
and gain a competitive edge. We have extensive experience working with a wide
range of clients, from small startups to large enterprises, and we have a deep
understanding of the challenges faced by businesses in today's rapidly evolving
digital landscape.

We take a customer-focused approach to our work, working closely with our clients
to understand their unique needs and develop customized solutions that meet their
requirements. Our commitment to quality is unwavering, and we adhere to the highest
industry standards to ensure our solutions are reliable and robust.

Whether you are looking for software development services, hardware design solutions,
or consulting services, Amarula Solutions has the expertise and achieve your business
goals. Contact us today to discover how we can help you stay ahead of the curve.

### Sphinx Setup (UBUNTU)

Install the following package in order to build the project

```bash
     python3 -m venv .venv
     . ./.venv/bin/activate
     pip install -r requirements.txt
```

### Sphinx Usage

```bash
usage: sphinx-build [OPTIONS] SOURCEDIR OUTPUTDIR [FILENAMES...]
```

### To build this document, run this command

```bash
sphinx-build  ./  _build/
```
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

