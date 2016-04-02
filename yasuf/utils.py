from io import TextIOWrapper, BytesIO
import sys


class YasufRuntimeException(Exception):
    pass

def _redirect_output(f, capture_stdout=True, capture_return=True):
    def redirect(*params, **kwargs):
        if sys.version_info[0] == 3:
            captured_stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
        else:
            captured_stdout = BytesIO()
        old_stdout = sys.stdout
        sys.stdout = captured_stdout

        ret_val = f(*params, **kwargs)

        sys.stdout = old_stdout
        captured_stdout.seek(0)
        return captured_stdout, ret_val
    return redirect
