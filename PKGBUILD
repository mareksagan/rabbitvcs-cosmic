# Maintainer: Your Name <your.email@example.com>
pkgname=rabbitvcs-cosmic
pkgver=0.1.0.stash
pkgrel=1
pkgdesc="RabbitVCS integration for COSMIC Files"
arch=('any')
url="https://github.com/yourusername/rabbitvcs-cosmic"
license=('GPL')
install='rabbitvcs-cosmic.install'
depends=('rabbitvcs' 'python-gobject' 'gtk3' 'zenity')
optdepends=('cosmic-files: the file manager this integrates with')
source=(
    "rabbitvcs-cosmic"
    "rabbitvcs-cosmic-action"
    "config.py"
    "settings.py"
    "install.py"
    "uninstall.py"
    "README.md"
    "Makefile"
    "rabbitvcs-cosmic.install"
)
md5sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    cd "${srcdir}"

    # Main executables
    install -Dm755 "rabbitvcs-cosmic-action" "${pkgdir}/usr/bin/rabbitvcs-cosmic-action"
    install -Dm755 "rabbitvcs-cosmic" "${pkgdir}/usr/bin/rabbitvcs-cosmic"

    # Support scripts
    install -Dm644 "config.py" "${pkgdir}/usr/lib/${pkgname}/config.py"
    install -Dm755 "settings.py" "${pkgdir}/usr/lib/${pkgname}/settings.py"
    install -Dm755 "install.py" "${pkgdir}/usr/lib/${pkgname}/install.py"
    install -Dm755 "uninstall.py" "${pkgdir}/usr/lib/${pkgname}/uninstall.py"
    install -Dm644 "Makefile" "${pkgdir}/usr/lib/${pkgname}/Makefile"

    # Convenience wrappers for utility scripts
    install -d "${pkgdir}/usr/bin"
    printf '#!/bin/bash\nexec python3 /usr/lib/%s/settings.py "$@"\n' "${pkgname}" \
        > "${pkgdir}/usr/bin/rabbitvcs-cosmic-settings"
    chmod 755 "${pkgdir}/usr/bin/rabbitvcs-cosmic-settings"

    printf '#!/bin/bash\nexec python3 /usr/lib/%s/install.py "$@"\n' "${pkgname}" \
        > "${pkgdir}/usr/bin/rabbitvcs-cosmic-install"
    chmod 755 "${pkgdir}/usr/bin/rabbitvcs-cosmic-install"

    printf '#!/bin/bash\nexec python3 /usr/lib/%s/uninstall.py "$@"\n' "${pkgname}" \
        > "${pkgdir}/usr/bin/rabbitvcs-cosmic-uninstall"
    chmod 755 "${pkgdir}/usr/bin/rabbitvcs-cosmic-uninstall"

    # Documentation
    install -Dm644 "README.md" "${pkgdir}/usr/share/doc/${pkgname}/README.md"
}
