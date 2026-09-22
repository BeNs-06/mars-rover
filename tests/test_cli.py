from mars_rover.cli import main


def test_cli_prints_final_position_and_direction(capsys):
    exit_code = main(
        [
            "--width",
            "5",
            "--height",
            "5",
            "--start-x",
            "1",
            "--start-y",
            "2",
            "--start-direction",
            "N",
            "LMLMLMLMM",
        ]
    )
    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "1:3:N"


def test_cli_reports_out_of_bounds_error(capsys):
    exit_code = main(
        [
            "--width",
            "2",
            "--height",
            "2",
            "--start-x",
            "0",
            "--start-y",
            "1",
            "--start-direction",
            "N",
            "M",
        ]
    )
    assert exit_code == 1
    stderr = capsys.readouterr().err
    assert "hors de la carte" in stderr or "sortir de la carte" in stderr


def test_cli_reports_invalid_command(capsys):
    exit_code = main(
        [
            "--width",
            "5",
            "--height",
            "5",
            "--start-x",
            "0",
            "--start-y",
            "0",
            "--start-direction",
            "N",
            "X",
        ]
    )
    assert exit_code == 1
    assert "Commande inconnue" in capsys.readouterr().err
