import math
from warframeAPI import warframeApi
scanItem = "arcane grace"
chrome_path = "/home/shadarien/Downloads/chrome-linux64/chromedriver" 
api = warframeApi(chrome_path=chrome_path)
api.scan_warframe(scanItem)
answer = math.floor(api.market_extraction['Highest Price'])
print(answer)