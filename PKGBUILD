# Maintainer: Your Name <your.email@example.com>
pkgname=rabbitvcs-cosmic
pkgver=0.1.0
pkgrel=1
pkgdesc="RabbitVCS integration for COSMIC Files"
arch=('any')
url="https://github.com/yourusername/rabbitvcs-cosmic"
license=('GPL')
depends=('rabbitvcs' 'python-gobject' 'gtk3' 'zenity')
optdepends=('cosmic-files: the file manager this integrates with')

package() {
    cd "${srcdir}"
    install -Dm755 "rabbitvcs-cosmic-action" "${pkgdir}/usr/bin/rabbitvcs-cosmic-action"
    install -Dm755 "rabbitvcs-cosmic" "${pkgdir}/usr/bin/rabbitvcs-cosmic"
    install -Dm644 "README.md" "${pkgdir}/usr/share/doc/${pkgname}/README.md"
}
