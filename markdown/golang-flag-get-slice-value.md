title: Golang flag 获取多个值
date: 2017-06-26 20:36:12
---

flag包是golang中处理command line参数标准库。 

> GoDoc: https://golang.org/pkg/flag/


但是在某些情况下，我们要对一个key指定多个值。 并获取多个值得数组。 这时我们需要定义一个Type Value接口类型

```go
type Value interface {
    String() string
    Set(string) error
}
```

重写Set方法, 处理每个value， 追加到最终的数组.


```go
type arrayFlags []string

// Value ...
func (i *arrayFlags) String() string {
    return fmt.Sprint(*i)
}

// Set 方法是flag.Value接口, 设置flag Value的方法.
// 通过多个flag指定的值， 所以我们追加到最终的数组上.
func (i *arrayFlags) Set(value string) error {
    *i = append(*i, value)
    return nil
}
```

使用

```go
var mongoAddrs arrayFlags

flag.Var(&mongoAddrs, "addr", "Database hosts")

flag.Parse()
```

传参执行方式

```bash
./main --addr 192.168.0.55 --addr 192.168.0.56
```

