# Buy and Hold 100 Crypto

## The "Experiment"
I came across an interesting experiment where a person has bought $10 of each of the top 100 crypto assests with the intent of
holding them for 5 years and then selling them. You can read more about it as well as see how the portfolio is doing 
[here](https://buyandhold100crypto.com/).

## The Tool
Myself and quite a few others have become interested in this "experiment" and have 
looked at doing something similar. There is a decent amout of leg work that goes into getting started such as figuring out how 
many of the top cryptos you would like to invest in as well as where you can purchase them. To help I created this simple command 
line tool in python.

## Usage
Install using pip:
```
pip install bh100
```
Then just run the CLI:
```
bh100
```
Then just answer the questions. Two JSON files will be created. One containing information for each Crypto named coins.json and a second
showing which Cryptos are on your prefered exchanges named prefered.json. You can open the files in a web browser for easy viewing.

## Todo
 * Add additional output formats.
 * Show amount to send to each exchange.
 
## Some Packages Used
 *  [coinmarketcap](https://github.com/barnumbirr/coinmarketcap)
 *  [click](http://click.pocoo.org/5/)
 *  [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
 *  [Requests](http://docs.python-requests.org/en/master/)
 
## Tips
 * BTC: 16XKpeFeeDJCc11eMz459mc7BhWabgFYE8
 * ETH: 0xC41a9b23c3536aaA5D3CAF462771eBA42b157C4D
 * XRB/NANO: xrb_39iboti6r3pwzq39aipm5a6mdcremk1izkg9tc78h99a5331be8m4n7kxmaw
