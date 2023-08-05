# target-keboola #

A [Singer](https://singer.io/) target that writes data to Keboola Connection.

### Install ###

Requires Python 3
```
> pip install target-keboola
```

### Configurations ###

This target requires a `config.json` to specify the user's [Storage API Token](https://developers.keboola.com/integrate/storage/python-client/) and [Bucket Destination](https://help.keboola.com/storage/buckets/).

```
{
    "bucket_id" = "in.c-singer",
    "storage_token": "YOUR_STORAGE_TOKEN"
}
```
*Note: Please ensure the specified Storage Token has compatible permission to access KBC.* 

To run `target-keboola` with the configuration file, use this command:
```
> target-keboola -c config.json
```

### Contact Info ###

Leo Chan  
Vancouver, Canada (PST time)  
Email: leo@keboola.com  
Private: cleojanten@hotmail.com  
