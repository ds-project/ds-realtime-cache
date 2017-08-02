# ds-realtime-cache
Machine Learning realtime cache with Redis

use python 3.5.2

Only redis-client library for python is required.

```
> cd /d/home/site/tools/
> python -m pip install azure 
```

Then, put some configs on file and send post request and put body just following as json type.
"Inputs" should follow the definition of azure ML we will use.

```json
{
    "inputs": [
        [ "0", "0", "0", "0", "0", "0", "0", "0", "value", "value", "0", "0", "0", "value", "value" ],
        [ "2", "30", "100", "300", "100", "00", "500", "300", "value", "value", "0", "0", "0", "value", "value" ]
    ]
}
```

If azure function do correctly, you will see this response 

```json
{"2":"['100', '100', '0', '500', '300', 'value', 'Y', '0.997041344642639']","0":"['0', '0', '0', '0', '0', 'value', 'Y', '0.994130671024323']"}
```
