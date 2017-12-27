    success = False
    git_rep = "git://github.com/chamli/CyberCrowl.git"
    tool_path = modulePath()
    
    if not os.path.exists(os.path.join(tool_path, ".git")):
        errMsg = "not a git repository. Please checkout the 'CyberCrowl' repository "
        exit(write(errMsg))
    else:
        infoMsg = "updating CyberCrowl to the latest development version from the "
        infoMsg += "GitHub repository"
        exit(write(infoMsg))

        debugMsg = "sqlmap will try to update itself using 'git' command"
        exit(write(debugMsg))


        try:
            process = subprocess.Popen("git checkout . && git pull %s HEAD" % git_rep, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tool_path.encode(locale.getpreferredencoding()))
            pollProcess(process, True)
            stdout, stderr = process.communicate()
            success = not process.returncode
        except (IOError, OSError), ex:
            success = False
            exit(write(ex))

        if success:
            exit(write("%s the latest revision '%s'" % ("already at" if "Already" in stdout else "updated to", getRevisionNumber())))
        else:
            if "Not a git repository" in stderr:
                errMsg = "not a valid git repository. Please checkout the 'CyberCrowl' repository "
                errMsg += "from GitHub (e.g. 'git clone --depth 1 https://github.com/chamli/CyberCrowl.git CyberCrowl')"
                exit(write(errMsg))
            else:
                exit(write("update could not be completed ('%s')" % re.sub(r"\W+", " ", stderr).strip())

    if not success:
        if platform.system() == 'Windows':
            infoMsg = "for Windows platform it's recommended "
            infoMsg += "to use a GitHub for Windows client for updating "
            infoMsg += "purposes (http://windows.github.com/) or just "
            infoMsg += "download the latest snapshot from "
            infoMsg += "https://github.com/chamli/CyberCrowl/archive/master.zip"
        else:
            infoMsg = "for Linux platform it's required "
            infoMsg += "to install a standard 'git' package (e.g.: 'sudo apt-get install git')"

        exit(write(infoMsg))
