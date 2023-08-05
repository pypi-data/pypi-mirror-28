# input-picker-python

## Usage

``` py
from input_picker import pick_bool, pick_item, Stop, Help

try:
    value = pick_bool()
except Help: # when user pick the help
    print_your_help()
except Stop: # when user pick the stop
    stop_your_app()
```

**Tips**: you can handle `Stop` on root:

``` py
if __name__ == '__main__':
    try:
        main()
    except Stop:
        print('User stop application.')
```
