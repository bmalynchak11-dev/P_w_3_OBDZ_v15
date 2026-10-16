from conftest import load
from pgutil import attempt


def test_my_record_book_invalid_format(db):
    """Перевірка порушення формату залікової книжки (має бути 2 великі латинські літери та 6 цифр)."""
    module = load(5)
    db.run(module.script())
    
    # 3 літери замість двох порушують регулярний вираз
    out = attempt(
        db,
        [],
        "INSERT INTO student (id, full_name, birth_date, record_book) "
        "VALUES (1, 'Олександр Коваль', '2005-06-15', 'ABC12345')"
    )
    assert out.state == "23514"
    assert out.constraint == "ck_student_record_book"


def test_my_grade_points_out_of_range(db):
    """Перевірка обмеження діапазону балів (повинно бути від 0 до 100)."""
    module = load(5)
    db.run(module.script())
    
    # Спочатку додаємо валідного студента
    db.run(
        "INSERT INTO student (id, full_name, birth_date, record_book) "
        "VALUES (1, 'Олександр Коваль', '2005-06-15', 'AB123456');"
    )
    
    # Спроба виставити 105 балів
    out = attempt(
        db,
        [],
        "INSERT INTO grade (id, student_id, points, mark, graded_on) "
        "VALUES (1, 1, 105, 5, CURRENT_DATE)"
    )
    assert out.state == "23514"
    assert out.constraint == "ck_grade_points"


def test_my_grade_date_future(db):
    """Перевірка обмеження дати виставлення оцінки (не пізніше за CURRENT_DATE)."""
    module = load(5)
    db.run(module.script())
    
    # Спроба вказати дату з майбутнього
    out = attempt(
        db,
        [],
        "INSERT INTO grade (id, student_id, points, mark, graded_on) "
        "VALUES (1, 1, 85, 4, CURRENT_DATE + INTERVAL '1 day')"
    )
    assert out.state == "23514"
    assert out.constraint == "ck_grade_date"