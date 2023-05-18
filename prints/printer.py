import subprocess


DAEMON_AVAILABLE = False


def check_printer_daemon():
    global DAEMON_AVAILABLE
    if not DAEMON_AVAILABLE:
        proc = subprocess.Popen("which lpr", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        DAEMON_AVAILABLE = "lpr" in out.decode() and err.decode() == ""
    return DAEMON_AVAILABLE


def submit_to_printer(filename: str, printer=""):
    """
        Submits the file to a printer as a print job.
        Returns a subprocess.Popen object after running the command.

        `filename' should be the absolute or relative path of the file to print.
            For relative path, note the CWD and check ``settings.BASE_DIR``
        `printer' is the name of the printer to submit the job to. If it's empty,
            the default printer will be used.
    """
    if not check_printer_daemon():
        return None
    cmd = "lpr " + filename
    if printer != "":
        cmd += "-P " + printer
    return subprocess.Popen(cmd, shell=True)
