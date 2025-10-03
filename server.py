
# server.py (put next to manage.py)
import os
import sys
from django.core.management import execute_from_command_line

def main():
    # If running as onefile exe, _MEIPASS points to extracted files
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    # change cwd to project folder (where manage.py is)
    os.chdir(base)

    # ensure settings module is set if not already
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    # Use runserver without autoreload and serve static (--insecure if DEBUG False)
    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000", "--noreload", "--insecure"])

if __name__ == "__main__":
    main()
