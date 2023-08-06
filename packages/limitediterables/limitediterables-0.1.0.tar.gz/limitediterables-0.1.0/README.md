# Limited Iterables [![Build Status](https://travis-ci.org/Poogles/limitediterables.svg?branch=master)](https://travis-ci.org/Poogles/limitediterables)

Basic library to rate limit how quickly you get the next value out of an iterable.

## Install

```sh
pip install limitediterables
```


## Example

```python
target = range(100)
slow_iter = LimitedIterable(target, limit=50)  # This gives us 50 messages a second.

for i in slow_iter:
    print(i)

```

Should be useful for rate limiting against APIs or anything else that's sensitive to number of requests.

## Dev

```
pip install pytest
pytest
```

PRs accepted.
