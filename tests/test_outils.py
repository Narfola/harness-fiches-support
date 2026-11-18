import pytest
from pathlib import Path

from assistant.outils import AccesRefuse, lire_fiche


def test_refuse_une_fiche_hors_du_dossier(limites):
    with pytest.raises(AccesRefuse):
        lire_fiche("../.env.md", limites)


def test_lecture_fiche_valide(limites):
    fiche_dir = Path(limites["dossier_fiches"])
    fiche_dir.mkdir(parents=True, exist_ok=True)

    f = fiche_dir / "test.md"
    f.write_text("Contenu de test")

    assert lire_fiche("test.md", limites) == "Contenu de test"


def test_refuse_chemin_absolu(limites):
    with pytest.raises(AccesRefuse):
        lire_fiche("/etc/passwd", limites)


def test_refuse_extension_incorrecte(limites):
    with pytest.raises(AccesRefuse):
        lire_fiche("fiche.txt", limites)
