**true_encoding**
==================

*Usage:*
--------
>>>from true_encoding.debug import debug

>>>r = requests.get('http://www.fang.com')

>>>r.encoding = debug(r)

>>>print(r.text)

