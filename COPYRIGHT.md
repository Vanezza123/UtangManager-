# Copyright & Licensing Statement
> **Project:** UtangManager  
> **Repository:** https://github.com/vanezza123/UtangManager  
> **Date:** 2026-05-21

## 1️⃣ Authors & Contributors
| Name | Role | Email | Contribution |
|------|------|-------|--------------|
| Vanezza Ragutero | Lead Developer | vragutero@ssct.edu.ph | Core Django app, models, views, templates |
| {{ Author 2 }} | Front‑end Designer | {{ email2@example.com }} | UI/UX, Bootstrap styling, chart integration |
| {{ Author 3 }} | DevOps / Deployment | {{ email3@example.com }} | Render.yaml, Gunicorn config, CI/CD |
| *(add more rows as needed)* |

## 2️⃣ License
The **UtangManager** codebase is released under the **MIT License**.


## 3️⃣ Third‑Party Dependencies
| Dependency | Version | License | Source |
|------------|---------|---------|--------|
| Django | 6.0.4 | BSD‑3-Clause | https://www.djangoproject.com/ |
| gunicorn | 26.0.0 | MIT | https://github.com/benoitc/gunicorn |
| whitenoise | 6.12.0 | MIT | https://github.com/evansd/whitenoise |
| openpyxl | 3.1.5 | MIT | https://openpyxl.readthedocs.io/ |
| Bootstrap (CDN) | 5.x | MIT | https://getbootstrap.com/ |
| Chart.js (CDN) | 4.x | MIT | https://www.chartjs.org/ |
| *(add any additional packages from `requirements.txt`)* |

## 4️⃣ Source Files Included


## 5️⃣ Deployment Details
- **Target platform:** Render.com (see `render.yaml`).  
- **Runtime:** Python 3.11 (or the version you use).  
- **Build command:**  
  ```bash
  pip install -r requirements.txt && \
  python manage.py collectstatic --noinput && \
  python manage.py migrate