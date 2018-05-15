title: Golang bongo 简单示例
date: 2017-06-28 12:52:22
---

创建Connect Config

```go
config := &bongo.Config{
    ConnectionString: "mongodb://localhost?ssl=true",
    Database:         "bongotest",
}
```

**or**

```go
config := &bongo.Config{
    DialInfo: &mgo.DialInfo{
        Addrs:    []string{127.0.0.1},
        Source:   "admin",
        Username: "root",
        Password: "password",
        Database: "test",
        Timeout:  time.Duration(time.Minute),
        // DialServer: func(addr *mgo.ServerAddr) (net.Conn, error) {
        //  return tls.Dial("tcp", addr.String(), &tls.Config{})
        //},
    },
}
```

Connect

```go
connection, err := bongo.Connect(config)

if err != nil {
    log.Fatal(err)
}
```

声明Document, 类似于Model.

```
type User struct {
    Name               string          `json:"name" bson:"name"`
    Email              string          `json:"email" bson:"email"`
    Active             bool            `json:"active" bson:"active"`
}

type UserDocument struct {
    bongo.DocumentBase `bson:",inline"`
    User
}
```

操作, 通过bongo更新一个Document.

```go
user := &UserDocument{
    Name: "JackeuyGao",
    Email: "i@jackeygao.io",
    Active: false,    
}

err := connection.Collection("user").Save(user)

if err != nil {
    log.Fatal(err)
}

// Update ...
user.Active = true

err := connection.Collection("user").Save(user)

if err != nil {
    log.Fatal(err)
}

```
