# open more chrome with itself data and then copy js into console
 os.popen(
    "/home/jin/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome "
    "--remote-debugging-port=%d --no-first-run --no-default-browser-check --user-data-dir=./test-%d"%(remote_port,data_num))
