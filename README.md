![Tarantulla Facebook: a module for Facebook data extraction](./tarantulla-facebook-post.png)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg?style=for-the-badge) 
![LINUX](https://img.shields.io/badge/PLATFORM-LINUX-blue.svg?style=for-the-badge) 
![CRAN](https://img.shields.io/badge/LICENSE-GPLv3-blue.svg?style=for-the-badge) 
![LOVE](https://img.shields.io/badge/BUILT%20WITH-LOVE-red.svg?style=for-the-badge)
[![TWITTER](https://img.shields.io/badge/BY-@oncase-lightgrey.svg?style=for-the-badge)](https://twitter.com/oncase) 


## **"Tarantulla-Facebook: the solution to gather Facebook data from publishers of your interest"**

If you want to know more, check out Tarantulla's [landing page](http://tarantulla.io/) and our [post](https://medium.com/oncase/conhecendo-o-tarantulla-facebook-28c03d139661) in Medium.

On this document you will find information about: 
 
- [Requirements](#requirements)  
- [Installation](#installation)   
- [How to Run](#how-to-run)  
- [Running with PDI - Database Integration](#running-with-pdi---database-integration)


## Requirements 
- [Python 3.x (>=3.4)](https://www.python.org/getit/)
- [Facebook SDK](https://facebook-sdk.readthedocs.io/en/latest/)  
```Attention! You can install Facebook SDK with pip3```  
```sh
   $ sudo apt-get install python3-pip  
   $ pip3 install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk
```

## Installation

First things first: *git clone* this project. Prefer to clone in folder `/opt/git`.

## How to Run

### Configuration

1 - Edit `config-timeline.json`

All publishers and information such as output folders and python call should be defined on this file, according to the example:

```json
{
	"temp_output": "../data/",
	"python-command":"python3",
	"dateFrom" : "2017-05-14",
	"dateTo" : "" ,
	"publishers" :
	[
		{
			"userName": "AndroidPIT.br",
			"name": "AndroidPIT BR"
		}
	]	
}
```

with fields:

- temp_output = output folder used to store files created during execution  
  ```Attention! Folder path specified is relative to project's folder `/core` ```
- python-command = command that calls Python 3.x
- dateFrom = Tarantulla collects data from this date
- dateTo = date until when Tarantulla should collect posts
- publishers =
    - userName = user name to be queried
    - name = user full name

The fields `dateFrom` and `dateTo` are **optional**. If you don't specify them, Tarantulla Facebook collects all posts, regardless of the date they were published.

The `userName` is **fixed**, defined by Facebook, whereas `name` is **not fixed**, what means you can choose any `name` you think is representative for you. Additionaly, you can add more fields in case you need other information for any further application development. 

2 - Edit `api-keys.json`

The Facebook API access key should be specified on this file. The script will require the following access key:

```json
{
	"ACSSTKFB" : "[YOUR FACEBOOK ACCESS KEY]"
}
```
You can obtain the Facebook API keys for your project following these [steps](https://developers.facebook.com/docs/facebook-login/access-tokens).

### Execution

Execute the script `user_timeline_posts.py`, in the folder `/core`, with the **Python 3** command set on your machine. The API returns statistics from the gathered videos for the specified publisher. 

```bash
$ python3 user_timeline_posts.py
```

The **output** is a JSON file containing the fields:

- post_id
- created
- post_content
- likes
- shares
- comments
- engagement
- likes_page


## Running with PDI - Database Integration

PDI or *Pentaho Data Integration* is a platform to accelerate data pipeline, providing visual tools to reduce complexity. In this project PDI was used to integrate the results into a database such as PostgreSQL. If you want to organize your data in a database as well, follow the next steps. 

To know more about PDI, check out the [documentation](https://help.pentaho.com/Documentation/8.1). It is worth remember that PDI requires JAVA installed on your machine.

### Configuration

Steps 1 and 2 are the same as above, what means you must configure both files: `config-users.json` and `api-keys.json`. Additionaly, in order to run Tarantulla-YouTube with PDI you should perform 2 more steps:

3- Edit file `config-db.json` - Set JDBC connection, Database and Table.

```json
{  
	"database_config" :  
	{
		"database_name" : "postgres",
		"database_url" : "jdbc:postgresql://localhost:5432/",
		"database_driver" : "org.postgresql.Driver",
		"database_username" : "postgres",
		"database_password" : "[YOUR PASSWORD]",
		"database_schema" : "staging",
		"database_table" : "stg_facebook"  
	}
}
```

The above JSON is an example and you can change the fields' values according to your database configurations. 

4- Execute DDL

Execute the script `tarantulla-facebook/scripts/ddl.sql` with the appropriate changes for your environment/database. Remember to change `<yourSCHEMA>` and `<yourTABLE>` names in the script, according to the variables set in `config-db.json`.

``` Attention! If the schema does not already exist, you should create it before execute the SQL script. ```

``` Attention! In order to establish a connection to the database, PDI must have the correspondent database driver in the folder `<YOURPENTAHO>/design-tools/data-integration/lib`. ```


### Execution

When all is set, you can execute `main.kjb` directly from Pentaho `kitchen.sh` script. You should locate the **folder with PDI files** (PDI_HOME) and run:

```bash
$ <PDI_HOME>/./kitchen.sh  -file="<YOUR TARANTULLA FACEBOOK FOLDER>/etl/main.kjb"    
```

Alternatively, if your **PDI_HOME** is set to `/opt/Pentaho/design-tools/data-integration`, you can directly run the `etl.sh` script. 

```bash
$ <YOUR TARANTULLA FACEBOOK FOLDER>/scripts/etl.sh job ../etl/main.kjb    
```

Please, note that in order to execute `etl.sh`, the script must have the appropriate execution permissions in your system.


## License

Tarantulla-Facebook is released under the GPLv3 license.