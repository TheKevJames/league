<a name="1.0.5"></a>
## 1.0.5 (2017-08-06)


re-release for CI


<a name="1.0.4"></a>
## 1.0.4 (2017-08-06)


re-release for CI


<a name="1.0.3"></a>
## 1.0.3 (2017-08-06)


re-release for CI


<a name="1.0.2"></a>
## 1.0.2 (2017-08-06)


re-release for CI


<a name="1.0.1"></a>
## 1.0.1 (2017-08-06)


#### Features

* **api:**
  *  update to new champion.gg api ([9fd8dec8](9fd8dec8))
  *  update to new riot api ([9402f1d3](9402f1d3))
* **cli:**  better cli output ([850a574c](850a574c))
* **items:**
  *  add dark star game mode item tags ([ccd86d11](ccd86d11))

#### Bug Fixes

* **worth:**  explicitly handle "reduced wardvision radius" ([5b0f531d](5b0f531d))



<a name="1.0.0"></a>
## 1.0.0 (2017-01-29)


#### Features

* **api:**
  *  re-released Gold Efficiency API
  *  released REST API for all features
* **cli:**  quality of life improvements (progress bars, etc)
* **core:**  many code cleanups
* **isg:**
  *  re-wrote ISG to be many orders of magnitude faster to use
  *  update some hardcoded items for season 7
  *  use champion.gg API rather tahn webscraping -- results should be more consistent

#### Performance

* **api:**  built caching system
* **core:**  asynchronous updates used all around for massive performance gains
