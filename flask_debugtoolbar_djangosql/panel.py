# flask_debugtoolbar_djangosql/panel.py

from flask_debugtoolbar.panels import DebugPanel
from django.db.backends.utils import CursorWrapper
from django.utils.timezone import now
import time
import inspect


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
        return self.render("django_sql.html", context)

    def process_response(self, request, response):
        # 这里我们可以自定义如何处理 JSON 响应
        if response.mimetype == "application/json" and "_debug" in request.args:
            html_wrapped_response = make_response(
                render_template_string(
                    wrap_json,
                    response=response.data.decode("utf-8"),
                    http_code=response.status,
                ),
                response.status_code,
            )
            return html_wrapped_response
        return response

    def _tidy_stacktrace(self, stack):
        cleaned_stack = []

        for frame_info in stack:
            frame = frame_info.frame
            filename = frame.f_code.co_filename

            if "django" in filename and "contrib" not in filename:
                continue

            if "socketserver.py" in filename:
                continue

            if frame_info == stack[-1]:
                continue

            cleaned_stack.append(frame_info)

        return cleaned_stack
