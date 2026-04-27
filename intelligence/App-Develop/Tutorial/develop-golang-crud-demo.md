# Golang 基础示例

## 配置环境

在你开始之前，确认你已经下载并安装了如下软件：

* 确认你已完成安装 MySQL 客户端。

* 已完成[创建实例](../../Instance-Mgmt/create-instance/create-serverless-instance.md)，并通过 MySQL 客户端连接 MatrixOne Intelligence 并创建一个命名为 *test* 的数据库：

    ```sql
    mysql> create database test;
    ```
  
* 确认你已完成安装 [Golang 1.18 版本及以上](https://go.dev/dl/)，可以使用下面的命令行确认你的 Golang 版本：

	```
	#To check with Golang installation and its version
	go version
	```

* 确认你已经安装 `gorm.io/driver/mysql`，使用 `go get` 命令安装，代码如下：

	```
	go get -u gorm.io/driver/mysql
	```

你可以参考 [Golang 连接 MatrixOne Intelligence 服务](../connect-mo/connect-to-matrixone-with-go.md)了解如何通过 `Golang` 连接到 MatrixOne Intelligence，本篇文档将指导你如何实现 CRUD（创建、读取、更新、删除）。

## 步骤

1. 通过 MySQL 客户端连接到 MatrixOne Intelligence。创建一个名为 *test* 的新数据库。

    ```
    mysql> create database test;
    ```

2. 创建一个命名为 `golang_crud_matrixonecloud.go` 的纯文本文件，将下面的代码拷贝至文件内：

    ```python
    package main

    import (
        "database/sql"
        "fmt"
        "log"
        _ "github.com/go-sql-driver/mysql"
    )

    func main() {
       //Open a new connection to MatrixOne Intelligence
        username := "585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin"  // modify this
        host := "freetier-01.cn-hangzhou.cluster.matrixonecloud.cn"       // modify this
        password := "your_password"     // modify this
        port := 6001
        database := "test"              
        encodedUsername := url.QueryEscape(username)
        dbConnectionString := encodedUsername + ":" + password + "@tcp(" + host + ":" + strconv.Itoa(port) + ")/" + database
        db, err := sql.Open("mysql", dbConnectionString)
        checkErr(err)

        //Create a table
        _, err2 := db.Exec("CREATE TABLE `userinfo` (`uid` INT(10) NOT NULL AUTO_INCREMENT,`username` VARCHAR(64) NULL DEFAULT NULL,`department` VARCHAR(64) NULL DEFAULT NULL,`created` DATETIME NULL DEFAULT NULL, PRIMARY KEY (`uid`));")
        if err2 != nil {
            log.Fatal(err2)
        }
        fmt.Print("Successfully Created\n")

        // Insert a record
        stmt, err := db.Prepare("INSERT userinfo SET username=?,department=?,created=?")
        checkErr(err)

        res, err := stmt.Exec("Alex", "r&d", "2023-01-01 12:00:00")
        checkErr(err)

        id, err := res.LastInsertId()
        checkErr(err)

        fmt.Println(id)
        //Update a record
        stmt, err = db.Prepare("update userinfo set username=? where uid=?")
        checkErr(err)

        res, err = stmt.Exec("Mark", id)
        checkErr(err)

        affect, err := res.RowsAffected()
        checkErr(err)

        fmt.Println(affect)

        // Query all records
        rows, err := db.Query("SELECT * FROM userinfo")
        checkErr(err)

        for rows.Next() {
            var uid int
            var username string
            var department string
            var created string
            err = rows.Scan(&uid, &username, &department, &created)
            checkErr(err)
            fmt.Println(uid)
            fmt.Println(username)
            fmt.Println(department)
            fmt.Println(created)
        }

        // Delete a record
        stmt, err = db.Prepare("delete from userinfo where uid=?")
        checkErr(err)

        res, err = stmt.Exec(id)
        checkErr(err)

        affect, err = res.RowsAffected()
        checkErr(err)

        fmt.Println(affect)

        db.Close()

    }

    func checkErr(err error) {
        if err != nil {
            panic(err)
        }
    }

    ```

3. 打开一个新的终端，使用如下命令行，执行此 Golang 文件。

    ```
    > go run golang_crud_matrixonecloud.go
    Successfully Created
    1
    1
    1
    Mark
    r&d
    2023-01-01
    1
    ```
