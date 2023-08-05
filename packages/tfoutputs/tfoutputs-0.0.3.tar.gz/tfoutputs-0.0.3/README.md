# Python tfoutputs

This gem is a python interface to access your terraform outputs.

## Installation


```python
pip install tfoutputs
```


## Pre-requistes

Terraform state file >0.7.
Python 3 (May work on python 2.7, but not tested).




## Usage

Include the module

```python
import 'tfoutputs'
```

tfoutputs uses 'backends' as a means of retrieving the state files. A backend is a place where the terraform state file lives. Currently only two are supported: s3 and file.

Setting up an s3 backend:

```python
    my_config = [
        {'backend': 's3',
                      'options': {'bucket_name': 'bucket-where-i-have-my-state-files',
                                  'bucket_key': 'terraform.tfstate',
                                  'bucket_region': 'eu-west-1'
                                  }
        }
    ]

    state_reader = tfoutputs.load(my_config)
    print(state_reader.allowed_ips)

```
Gives us:

```
it works

```

Setting up a file backend:
```python

    config =    [ {'backend': 'file', 'options': {
        'path': '/Users/jedwards/terraform.tfstate'
        }
    }]

```


## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/jae2/ruby-tfoutput. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.


## License

The gem is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

