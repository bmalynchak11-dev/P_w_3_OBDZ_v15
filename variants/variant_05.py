"""
Варіант 15. Задача 5, набір 3 (навчальний заклад).
Обмеження CHECK.
"""

VARIANT = 15


def script() -> str:
    return """
CREATE TABLE student (
    id integer NOT NULL,
    full_name varchar(150) NOT NULL,
    birth_date date NOT NULL,
    record_book char(8) NOT NULL,
    CONSTRAINT pk_student PRIMARY KEY (id),
    CONSTRAINT ck_student_birth CHECK (birth_date >= DATE '1950-01-01'),
    CONSTRAINT ck_student_record_book CHECK (record_book ~ '^[A-Z]{2}[0-9]{6}$')
);

CREATE TABLE grade (
    id integer NOT NULL,
    student_id integer NOT NULL,
    points smallint NOT NULL,
    mark smallint,
    graded_on date NOT NULL,
    CONSTRAINT pk_grade PRIMARY KEY (id),
    CONSTRAINT ck_grade_points CHECK (points BETWEEN 0 AND 100),
    CONSTRAINT ck_grade_mark CHECK (mark IN (2, 3, 4, 5)),
    CONSTRAINT ck_grade_date CHECK (graded_on <= CURRENT_DATE)
);
"""