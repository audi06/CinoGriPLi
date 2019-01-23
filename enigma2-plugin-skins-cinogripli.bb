DESCRIPTION = "GriPLi FHD skin by Cino for Open Vision and OpenPLI based images."
MAINTAINER = "dreamosat-forum.com"
LICENSE = "Proprietary"

LIC_FILES_CHKSUM = "file://LICENSE;md5=9c32b9ca84caf9e08bf1561569d8190a"

inherit gitpkgv allarch

PV = "1.0+git${SRCPV}"
PKGV = "1.0+git${GITPKGV}"
PR = "r0"

RRECOMMENDS_${PN} = "enigma2-plugin-extensions-weatherplugin"
SRC_URI = "git://DreamOSat@gitlab.com/DreamOSat/CinoGriPLi.git;protocol=https"
SRCREV = "${AUTOREV}"

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

