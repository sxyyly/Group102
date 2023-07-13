from requests_html import HTMLSession
import time
start=time.time()
session = HTMLSession()
r= session.get('https://www.blockchain.com/btc/tx/4645603184e112828bf9a52275deb01e501635589ea02af8e3c4e12fbff9e16c')
end=time.time()
print(end-start)
print(dir(r.html))

