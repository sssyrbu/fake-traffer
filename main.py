import tkinter as tk
import threading
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time


class SeleniumTraffic():
    def __init__(self):
        self.counter = 0
        self.threads = []
        self.user_agent = UserAgent()
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.bind_all("<Key>", self._onKeyRelease, "+")
        self.root.title("Fake Traffer")
        
        # Add checkbox for proxy requirement
        self.url_label = tk.Label(self.root, text="URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()
        self.use_proxy_var = tk.BooleanVar()
        self.use_proxy_cb = tk.Checkbutton(self.root, text="Use proxy", variable=self.use_proxy_var)
        self.use_proxy_cb.pack()

        # Add button to start web automation
        self.start_btn = tk.Button(self.root, text="Start", command=self.run_selenium)
        self.start_btn.pack()
        self.label = tk.Label(self.root, text="Fake website entries: 0")
        self.label.pack()


    def run_selenium(self):
        if self.use_proxy_var.get():
            for _ in range(6):
                t = threading.Thread(target=self.selenium_thread_proxy)
                t.start()
        else:
            for _ in range(6):
                t = threading.Thread(target=self.selenium_thread)
                t.start()


    def selenium_thread_proxy(self):
        with open("proxy.txt", "r") as f:
            proxies = f.readlines()

        while True:
            try:
                for proxy in proxies:
                    url = self.url_entry.get()
                    options = webdriver.ChromeOptions()
                    options.add_argument('--headless')
                    options.add_argument('--proxy-server=http://%s:%s@%s' % proxy)
                    options.add_argument('--autoplay-policy=no-user-gesture-required')
                    options.add_argument(f"user-agent={self.user_agent.random}")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])

                    driver = webdriver.Chrome(options=options)
                    actions = ActionChains(driver)
                    driver.get(url)
                    driver.close()
                    driver.quit()
                    self._counter()
                    self._emulate_scroll(driver=driver)
            except:
                pass


    def selenium_thread(self):
        while True:
            try:
                url = self.url_entry.get()
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--autoplay-policy=no-user-gesture-required')
                options.add_argument(f"user-agent={self.user_agent.random}")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])

                driver = webdriver.Chrome(options=options)
                actions = ActionChains(driver)
                driver.get(url)
                driver.close()
                driver.quit()
                self._counter()
                self._emulate_scroll(driver=driver)
            except:
                pass


    def _emulate_scroll(self, driver):
        height = int(driver.execute_script("return document.documentElement.scrollHeight"))
        while True:
            driver.execute_script('window.scrollBy(0,30)')
            time.sleep(0.10)
            totalScrolledHeight = driver.execute_script("return window.pageYOffset + window.innerHeight")
            
            if totalScrolledHeight == height:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                element.send_keys(Keys.CONTROL + Keys.HOME)
                break


    def _onKeyRelease(self, event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")


    def _counter(self):
        self.counter += 1
        self.label['text'] = f'Fake website entries: {self.counter}'


if __name__ == "__main__":
    app = SeleniumTraffic()
    app.root.mainloop()
