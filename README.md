# trbot - Work in progress!

CLI Binance Trading Bot



<p  align="center">

  

<a> [<img src="https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg" alt="forthebadge"/>](https://forthebadge.com/) </a>

  

</p>

Dependencies:

---

pip install binance-connector tabulate websocket-client

---

Tested using Python 3.9.7.

Does tests using RSI14 and MA25.


in a folder with bot.py you need:

real.txt, containing your public api key on line 1 and secret key on line 2

test.txt, containing your test server api key on line 1 and secret key on line 2

vassets.txt, containing a float (local testing USDT)

If you're wondering, the test server key in old commits is my real test server key. The real key doesn't exist.
