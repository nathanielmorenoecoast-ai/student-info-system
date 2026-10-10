# Student Information System

A command-line Student Information System built in Python with a cloud-ready,
modular architecture. Student records are stored in JSON, configuration is
external, and all activity is logged.

## Features

- **CRUD**: add, view, update, and delete students
- **Persistence**: JSON storage with atomic writes
- **Validation**: ID, name, age range, email format, course
- **Search**: by ID, name, email, or course (case-insensitive)
- **Export**: dump all records to CSV
- **Error recovery**: a corrupt data file is backed up and replaced automatically
- **Logging**: file log in `logs/app.log`
- **Configuration**: `config/config.json`, with `SIS_DATA_FILE` environment override
- **Tests**: unit tests in `tests/`

## Project Structure

```
student-info-system/
├── src/
│   ├── models/student.py            # Student data class + validation
│   ├── services/student_service.py  # CRUD, search, export, persistence
│   ├── utils/config_loader.py       # Configuration management
│   ├── utils/logger.py              # Logging setup
│   └── main.py                      # CLI menu
├── data/students.json               # Data store
├── config/config.json               # Settings
├── logs/                            # Log output
├── tests/test_student_service.py    # Unit tests
├── requirements.txt
└── README.md
```

## Getting Started

Requires Python 3.9+.

```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
python -m src.main
```

## Running Tests

```bash
python -m unittest discover -s tests -t .
# or, with pytest installed:
pytest -v
```

## Configuration

| Key | Purpose | Default |
|---|---|---|
| `data_file` | JSON data store | `data/students.json` |
| `export_file` | CSV export path | `data/students_export.csv` |
| `log_file` | Log location | `logs/app.log` |
| `log_level` | DEBUG / INFO / WARNING / ERROR | `INFO` |

Set `SIS_DATA_FILE` to override the data path (useful in cloud deployments).

## Git Workflow

Work is done on feature branches and merged into `main` through pull requests
(`feature/student-model`, `feature/student-service`, `feature/cli`,
`feature/tests`, `docs/readme`).

## Author

[Your Name]
