from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("file:///home/consta/Desktop/Programing/helloworld.html")
a = time.time()
while time.time() <= a + 3.1:
    print('.',end="")
    if time.time() >= a + 3:
        f = open('/home/consta/Desktop/Programing/helloworld.html','w')
        print('!',end="")
        message = "<html><head></head><body><p><i>" + time.ctime(time.time()) + "</i></p></body></html>"
        f.write(message)
        f.close()
        driver.refresh()
        a = time.time()
    time.sleep(0.1)
f.close()
