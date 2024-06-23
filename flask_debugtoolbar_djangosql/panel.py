# flask_debugtoolbar_djangosql/panel.py

from flask_debugtoolbar.panels import DebugPanel
from django.db.backends.utils import CursorWrapper
from django.utils.timezone import now
import time
import inspect
from jinja2 import Environment, FileSystemLoader
import os


class DjangoSQLPanel(DebugPanel):
    name = "DjangoSQL"
    has_content = True

    def __init__(self, jinja_env=None, context=None):
        super().__init__(jinja_env, context)
        self.queries = []
        self._original_execute = CursorWrapper.execute
        self._original_executemany = CursorWrapper.executemany
        CursorWrapper.execute = self._wrap_execute(CursorWrapper.execute)
        CursorWrapper.executemany = self._wrap_executemany(CursorWrapper.executemany)

        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def _wrap_execute(self, original_execute):
        def wrapped_execute(cursor, sql, params=None):
            start_time = time.time()
            try:
                result = original_execute(cursor, sql, params)
            except Exception as e:
                raise e
            else:
                duration = time.time() - start_time
                stack = inspect.stack()
                self._record_query(sql, params, duration, self._tidy_stacktrace(stack))
                return result

        return wrapped_execute

    def _wrap_executemany(self, original_executemany):
        def wrapped_executemany(cursor, sql, param_list):
            start_time = time.time()
            try:
                result = original_executemany(cursor, sql, param_list)
            except Exception as e:
                raise e
            else:
                duration = time.time() - start_time
                stack = inspect.stack()
                self._record_query(
                    sql, param_list, duration, self._tidy_stacktrace(stack)
                )
                return result

        return wrapped_executemany

    def _record_query(self, sql, params, duration, stack):
        self.queries.append(
            {
                "sql": sql,
                "params": params,
                "duration": duration * 1000,  # ms
                "time": now(),
                "stack": stack,
            }
        )

    def nav_title(self):
        return "Django SQL"

    def nav_subtitle(self):
        total_duration = sum(query["duration"] for query in self.queries)
        return f"{len(self.queries)} queries in {total_duration:.2f}ms"

    def title(self):
        return "Django SQL Queries"

    def url(self):
        return ""

    def content(self):
        context = self.context.copy()
        context["queries"] = self.queries
        return self.render("panels/django_sql.html", context)

    def _tidy_stacktrace(self, stack):
        cleaned_stack = []

        for frame_info in stack:
            frame = frame_info.frame
            filename = frame.f_code.co_filename

            # Check if part of Django (excluding contrib apps)
            if "django" in filename and "contrib" not in filename:
                continue

            # Check if part of SocketServer
            if "socketserver.py" in filename:
                continue

            # Skip the last entry (our stacktracing code)
            if frame_info == stack[-1]:
                continue

            cleaned_stack.append(frame_info)

        return cleaned_stack
