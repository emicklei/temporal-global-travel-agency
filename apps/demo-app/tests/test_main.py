from demo_app.main import main

def test_main(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "demo"

