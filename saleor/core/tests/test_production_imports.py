import os
import subprocess
import sys

from django.conf import settings

MODULES_USED_IN_PRODUCTION = [
    "saleor.account.management.commands.createsuperuser",
    "saleor.core.management.commands.populatedb",
    "saleor.core.utils.random_data",
]


def test_production_modules_do_not_require_dev_dependencies():
    imports = "\n".join(f"import {module}" for module in MODULES_USED_IN_PRODUCTION)
    code = f"""
import sys

sys.modules["pytest"] = None

import django

django.setup()
{imports}
"""
    env = {**os.environ, "DJANGO_SETTINGS_MODULE": "saleor.settings"}

    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=settings.PROJECT_ROOT,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
