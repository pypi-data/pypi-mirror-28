import os
import sys
import subprocess
import threading
import signal


def get_environment():
    """
    Get the environment parameter, depending on OS (Win/Unix).
    """
    if os.name == 'nt':  # not tested!
        environment = '--environment=WIN'
    else:
        environment = '--environment=UNIX'
    return environment


def print_no_newline(string):
    sys.stdout.write(str(string))
    sys.stdout.flush()


def run_popen_with_timeout(
        command, timeout, input_data, stdin, stdout, stderr, env=None):
    """
    Run a sub-program in subprocess.Popen, pass it the input_data,
    kill it if the specified timeout has passed.
    returns a tuple of success, stdout, stderr

    sample usage:

    timeout = 60  # seconds
    path = '/path/to/event.log'
    command = ['/usr/bin/tail', '-30', path]
    input_data = ''
    success, stdout, stderr = run_popen_with_timeout(command, timeout,
                                                     input_data)
    if not success:
        print('timeout on tail event.log output')
    tail_output = stdout
    """
    kill_check = threading.Event()

    def _kill_process_after_a_timeout(pid):
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            # catch a possible race condition, the process terminated normally
            # between the timer firing and our kill
            return
        kill_check.set()  # tell the main routine that we had to kill
        # use SIGKILL if hard to kill...
        return

    stdout_l = []

    # don't use shell if command/options come in as list
    use_shell = not isinstance(command, list)
    try:
        p = subprocess.Popen(command, bufsize=1, shell=use_shell,
                             stdin=stdin, stdout=stdout,
                             stderr=stderr, env=env)
    except OSError as error_message:
        stderr = 'OSError: ' + str(error_message)
        return (False, '', stderr)
    pid = p.pid

    watchdog = threading.Timer(timeout, _kill_process_after_a_timeout,
                               args=(pid, ))
    watchdog.start()

    while True:
        output = p.stdout.readline(1).decode('utf-8')
        if output in ['', b''] and p.poll() is not None:
            break
        if output == '\n':
            print(output)
        else:
            print_no_newline(output)
        stdout_l.append(output)

    try:
        (stdout, stderr) = p.communicate(input_data)
    except OSError as error_message:
        stdout = ''
        stderr = 'OSError: ' + str(error_message)
        p.returncode = -666

    watchdog.cancel()  # if it's still waiting to run

    # if it timed out, success is False
    success = (not kill_check.isSet()) and p.returncode >= 0
    kill_check.clear()
    return (success, ''.join(stdout_l), stderr)


class Runner(object):
    """
    Setup to run envjasmine "specs" (tests).

    To use it, probably best to put it inside a normal python
    unit test suite, then just print out the output.
    """

    def __init__(self, rootdir=None, testdir=None, configfile=None,
                 browser_configfile=None):
        """
        Set up paths, by default everything is
        inside the "envjasmine" folder right here.
        Giving no paths, the sample specs from envjasmine will be run.
        XXX: it would be more practical if this raised an exception
             and you know you're not running the tests you want.

        parameters:
        testdir - the directory that holds the "mocks", "specs"
            and "include" directories for the actual tests.
        rootdir - the directory where the envjasmine code lives in.
        configfile - path to an extra js config file that is run for the tests.
        browser_configfile - path to an extra js config file for running
                    the tests in browser.
        """
        here = os.path.dirname(__file__)
        self.libdir = here
        self.rootdir = rootdir or os.path.join(here, 'envjasmine')
        self.testdir = testdir or self.rootdir
        self.configfile = configfile
        self.browser_configfile = browser_configfile
        self.runner_html = os.path.join(here, 'runner.html')

    def run(self, spec=None, timeout=None):
        """
        Run the js tests with envjasmine, return success (true/false) and
        the captured stdout data

        spec: (relative) path to a spec file (run only that spec)
        timeout: Set it to a given number of seconds and the process running
                 the js tests will be killed passed that time
        """
        environment = get_environment()
        rhino_path = os.path.join(self.rootdir, 'lib', 'rhino', 'js.jar')
        envjasmine_js_path = os.path.join(self.rootdir, 'lib', 'envjasmine.js')
        rootdir_param = '--rootDir=%s' % self.rootdir
        testdir_param = '--testDir=%s' % self.testdir
        if self.browser_configfile and os.path.exists(self.browser_configfile):
            self.write_browser_htmlfile()

        command = [
            'java',
            '-Duser.timezone=US/Eastern',
            '-Dfile.encoding=utf-8',
            '-jar',
            rhino_path,
            envjasmine_js_path,
            '--disableColor',
            environment,
            rootdir_param,
            testdir_param
            ]

        if self.configfile and os.path.exists(self.configfile):
            command.append('--configFile=%s' % self.configfile)

        # if we were asked to test only some of the spec files,
        # addd them to the command line:
        if spec is not None:
            if not isinstance(spec, list):
                spec = [spec]
            command.extend(spec)

        shell = False
        stdin = None
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        input_data = ''

        success, stdout, stderr = run_popen_with_timeout(
            command, timeout, input_data, stdin, stdout, stderr
        )

        # success will be true if the subprocess did not timeout, now look
        # for actual failures if there was not a timeout
        if success:
            success = self.did_test_pass(stdout)
        return success, stdout

    def did_test_pass(self, stdout):
        for line in stdout.splitlines():
            if 'Failed' in line:
                failed = line.split(':')[1].strip()
                return failed == '0'
        return False

    def write_browser_htmlfile(self):
        markup = self.create_testRunnerHtml()
        with open("browser.runner.html", 'w') as file:
            file.write(markup)

    def create_testRunnerHtml(self):
        with open(self.runner_html, 'r') as runner_html:
            html = runner_html.read()
            return html % {"libDir": os.path.normpath(self.libdir),
                           "testDir": os.path.normpath(self.testdir),
                           "browser_configfile": self.browser_configfile}
