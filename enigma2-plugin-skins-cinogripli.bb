DESCRIPTION = "GriPLi FHD skin by Cino for Open Vision and OpenPLI based images."
MAINTAINER = "dreamosat-forum.com"
SECTION = "misc"
PRIORITY = "optional"
LICENSE = "Proprietary"

LIC_FILES_CHKSUM = "file://LICENSE;md5=858b014508205322d36421a11207867c"

inherit gitpkgv allarch

PV = "1.0+git${SRCPV}"
PKGV = "1.0+git${GITPKGV}"

RRECOMMENDS:${PN} = "enigma2-plugin-extensions-weatherplugin"

SRC_URI = "git://github.com/audi06/CinoGriPLi.git;protocol=git"

FILES_${PN} = "/usr/share/enigma2/ /usr/lib/enigma2/"

S = "${WORKDIR}/git"

do_compile() {
}

do_install() {
	install -d ${D}/usr/share
	cp -r --preserve=mode,links ${S}/usr/share/* ${D}/usr/share/
	chmod -R a+rX ${D}/usr/share/enigma2/

        install -d ${D}/usr/lib
        cp -r --preserve=mode,links ${S}/usr/lib/* ${D}/usr/lib/
        chmod -R a+rX ${D}/usr/lib/enigma2/
}

