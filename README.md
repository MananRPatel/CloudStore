# CloudStore
This project purpose is to provide a file storage service with sharing files with other users.
User can share files with other users,Remove access and delete file which remove all access to all non-owner(friends) users
We use SHA256 to compare files with other file if file already exists with don't store the file only we use that file.


<p align="center">
Here our Database Schema design
 </p>
<p align="center">

  <img width="250" height="auto" src="https://firebasestorage.googleapis.com/v0/b/db-tester-f302d.appspot.com/o/download.png?alt=media&token=b0f88a5f-a8d9-4879-90c5-829a81416351">
</p>


***
----

user can login and register using **POST** method with following end point
```
/login
/register
```

***
----

using **GET** method with providing file name user can access the file. if user has permission to access the file
```
/cloud/my-drive/?filename=<filename>
```

***

using **POST** method user can send file to storage 
```
/cloud/my-drive/
```

***

using ****DELETE**** method user can delete the file. if user has file ownership 
#### add following JSON data to providing file name
 {
      " filename " : " <filename> "
  } 
```
/cloud/my-drive/
```


***
----

using **GET** method user can check their all files. 
```
/cloud/drive-permit/
```
***
using **POST** method owner can share their file with other users with friends privilege. 
```
/cloud/drive-permit/
```
***
using **PUT** method owner can change its ownership to other user. 
```
/cloud/drive-permit/
```
***
using **DELETE** method owner can remove the other users to use the shared file. 
```
/cloud/drive-permit/
```


***
----


using **GET** method owner of file can check, their total friends. 
```
/cloud/drive-share/<string:filename>/
```
***
----

### .env should contain below  details

```text
HOST = 'host:port'
USER = 'username'
PASSWORD = 'password'
DATABASE = 'database name'
SECRET = "secret key"
```
### If auth-token user doesn't want to store in cookie then user can also provide in authentication header