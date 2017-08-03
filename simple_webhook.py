from wsgiref.simple_server import make_server
import subprocess
import tempfile
import os

env = os.environ.copy()


def application(environ, start_response):
    content_length = int(environ['CONTENT_LENGTH'] or '0')
    input = environ['wsgi.input'].read(content_length)
    with tempfile.NamedTemporaryFile() as fd:
        p = subprocess.Popen(
            [os.environ['WEBHOOK_SCRIPT']],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
        )
        stdout, stderr = p.communicate(input=input)
    body = stdout or b'{}'
    if p.returncode == 0:
        status = '200 OK'
    else:
        status = '500 Internal Server Error'
    headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(body)))
    ]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print('serving on http://localhost:8000...')
        httpd.serve_forever()
