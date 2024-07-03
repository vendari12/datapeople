#!/bin/sh

cd /src
coverage run -m pytest tests --junitxml=/app/tests/test_reports.xml
coverage xml -o /app/tests/report_coverage.xml