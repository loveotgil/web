#!/usr/bin/env python3
"""
deploy_github_pages.py
------------------------
מעלה את קבצי האתר (HTML/CSS/JS) לריפו קיים ב-GitHub, כדי שיוצג ב-GitHub Pages.

לפני הרצה ראשונה - הגדר בהמשך הקובץ (בקטע CONFIG):
  1. REPO_URL     - כתובת ה-git של הריפו שלך (SSH או HTTPS)
  2. BRANCH       - הברנץ' שממנו GitHub Pages מגיש (בדוק ב-Settings > Pages)
  3. SITE_DIR     - התיקייה המקומית עם קבצי האתר להעלאה (ברירת מחדל: "site")

איך זה עובד:
  - אם יש כבר קלון מקומי של הריפו (בתיקייה local_repo/) - הסקריפט מעדכן אותו.
  - אם אין - הסקריפט משכפל (clone) את הריפו אוטומטית.
  - מעתיק את כל הקבצים מ-SITE_DIR לתוך הריפו (שומר על .git ו-README קיימים).
  - עושה git add + commit + push.

דרישות מקדימות במחשב שמריץ את הסקריפט:
  - git מותקן ובהרשאות push לריפו (מוגדר SSH key, או HTTPS עם token שמור ב-credential helper).

הרצה:
  python3 deploy_github_pages.py
  python3 deploy_github_pages.py --message "עדכון דף הרשמה לטורניר"
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# ============== CONFIG - ערוך לפני הרצה ==============
REPO_URL = "git@github.com:USERNAME/REPO_NAME.git"   # <-- להחליף בכתובת הריפו שלך
BRANCH = "main"                                       # <-- הברנץ' ש-Pages מגיש ממנו (main / gh-pages)
SITE_DIR = Path(__file__).parent / "site"             # תיקיית קבצי האתר המקומית להעלאה
LOCAL_CLONE_DIR = Path(__file__).parent / "local_repo"  # לאן יישמר הקלון המקומי
# =======================================================


def run(cmd, cwd=None):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        sys.exit(f"שגיאה בהרצת הפקודה: {' '.join(cmd)}")
    if result.stdout.strip():
        print(result.stdout.strip())
    return result


def ensure_repo_cloned():
    if LOCAL_CLONE_DIR.exists() and (LOCAL_CLONE_DIR / ".git").exists():
        print(f"נמצא קלון קיים ב-{LOCAL_CLONE_DIR}, מעדכן...")
        run(["git", "fetch", "origin"], cwd=LOCAL_CLONE_DIR)
        run(["git", "checkout", BRANCH], cwd=LOCAL_CLONE_DIR)
        run(["git", "pull", "origin", BRANCH], cwd=LOCAL_CLONE_DIR)
    else:
        print(f"משכפל את הריפו לתוך {LOCAL_CLONE_DIR} ...")
        run(["git", "clone", "--branch", BRANCH, REPO_URL, str(LOCAL_CLONE_DIR)])


def copy_site_files():
    if not SITE_DIR.exists():
        sys.exit(f"תיקיית האתר {SITE_DIR} לא נמצאה. ודא שיש בה את קבצי ה-HTML/CSS/JS להעלאה.")

    print(f"מעתיק קבצים מ-{SITE_DIR} אל {LOCAL_CLONE_DIR} ...")
    for item in SITE_DIR.iterdir():
        dest = LOCAL_CLONE_DIR / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)


def commit_and_push(message: str):
    run(["git", "add", "-A"], cwd=LOCAL_CLONE_DIR)

    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=LOCAL_CLONE_DIR, capture_output=True, text=True
    )
    if not status.stdout.strip():
        print("אין שינויים חדשים להעלאה.")
        return

    run(["git", "commit", "-m", message], cwd=LOCAL_CLONE_DIR)
    run(["git", "push", "origin", BRANCH], cwd=LOCAL_CLONE_DIR)
    print("\n✅ האתר הועלה בהצלחה! השינויים יופיעו ב-GitHub Pages בדרך כלל תוך דקה-שתיים.")


def main():
    parser = argparse.ArgumentParser(description="פריסת האתר ל-GitHub Pages")
    parser.add_argument(
        "--message", "-m", default="עדכון אתר", help="הודעת ה-commit"
    )
    args = parser.parse_args()

    if "USERNAME/REPO_NAME" in REPO_URL:
        sys.exit(
            "עדכן קודם את REPO_URL בתחילת הקובץ עם כתובת הריפו האמיתית שלך "
            "(לדוגמה: git@github.com:your-username/lovegame-site.git)"
        )

    ensure_repo_cloned()
    copy_site_files()
    commit_and_push(args.message)


if __name__ == "__main__":
    main()
