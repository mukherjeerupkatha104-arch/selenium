"""Build browser options that keep public-site ads from covering real controls."""
from __future__ import annotations

import tempfile
from pathlib import Path

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

AD_HOSTS = (
    "googleads.g.doubleclick.net",
    "tpc.googlesyndication.com",
    "pagead2.googlesyndication.com",
    "www.googletagservices.com",
    "adservice.google.com",
    "adservice.google.co.in",
    "securepubads.g.doubleclick.net",
    "ad.doubleclick.net",
    "static.doubleclick.net",
    "www.googleadservices.com",
    "fundingchoicesmessages.google.com",
    "ep1.adtrafficquality.google",
    "ep2.adtrafficquality.google",
    "www.googletagmanager.com",
    "googletagmanager.com",
    "googleads4.g.doubleclick.net",
)


def get_browser_options(browser: str, headless: str):
    name = (browser or "chrome").strip().lower()
    headed_off = str(headless).strip().lower() == "true"
    if name == "firefox":
        options = FirefoxOptions()
        if headed_off:
            options.add_argument("-headless")
        options.add_argument("--width=1440")
        options.add_argument("--height=1080")
        return options

    options = ChromeOptions()
    if headed_off:
        options.add_argument("--headless=new")
    profile = Path(tempfile.mkdtemp(prefix="cartograph-chrome-"))
    options.add_argument(f"--user-data-dir={profile}")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-allow-origins=*")
    rules = ", ".join(f"MAP {host} 127.0.0.1" for host in AD_HOSTS)
    options.add_argument(f"--host-resolver-rules={rules}")
    return options
