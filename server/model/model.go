package model

import (
	"time"
	"github.com/jinzhu/gorm"
	_ "os"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
	"gopkg.in/gorp.v1"
	"database/sql"
	"log"
	"os"
)

var _ = fmt.Print

type Blog struct {
	//Id int `db:"id,primarykey,autoincrement" gorm:"primary_key;AUTO_INCREMENT"`
	Id int `db:"id" gorm:"primary_key;AUTO_INCREMENT"`
	Name string `db:"name" gorm:"column:name"`
}

type Article struct {
	Id int `db:"id" gorm:"primary_key;AUTO_INCREMENT"`
	Title string `db:"title"`
	Body string `db:"body"`
	Published bool `db:"published"`
	PublishedAt time.Time `db:"published_at"`
}

type Category struct {
	Id int `db:"id" gorm:"primary_key;AUTO_INCREMENT"`
	Name string `db:"name"`
}

type ArticleCategory struct {
	ArticleId int `db:"article_id" gorm:"primary_key"`
	CategoryId int `db:"category_id" gorm:"primary_key"`
}

func (_ *Blog) TableName() string {
	return "blogs"
}

func (_ *Article) TableName() string {
	return "articles"
}

func (_ *Category) TableName() string {
	return "categories"
}

func (_ *ArticleCategory) TableName() string {
	return "article_categories"
}

type logger struct {}
func (l *logger) Print(v ...interface{}) {
	fmt.Printf("logger: %#v", v)// [sql /Users/oinuma/go/src/github.com/oinume/tinyblog/server/model/model_test.go:26 788.002µs SELECT * FROM `blogs`   ORDER BY `blogs`.`id` ASC LIMIT 1 []]1
}

func OpenGorm() (*gorm.DB, error) {
	//dbDsn := os.Getenv("DB_DSN")
	db, err := gorm.Open(
		"mysql",
		//fmt.Sprintf("%v?charset=utf8mb4&parseTime=true&loc=UTC", dbDsn),
		"root:root@tcp(192.168.9.10:3306)/tinyblog?charset=utf8mb4&parseTime=true&loc=UTC",
	)
	db.LogMode(true)
	db.SetLogger(&logger{})
	return db, err
}

func OpenGorp() (*gorp.DbMap, error) {
	db, err := sql.Open("mysql", "root:root@tcp(192.168.9.10:3306)/tinyblog?charset=utf8mb4&parseTime=true&loc=UTC")
	if err != nil {
		return nil, err
	}
	dbmap := &gorp.DbMap{Db: db, Dialect: gorp.MySQLDialect{}}
	dbmap.TraceOn("[gorp]", log.New(os.Stdout, "myapp:", log.Lmicroseconds))

	dbmap.AddTableWithName(Blog{}, (&Blog{}).TableName()).SetKeys(true, "id")
	dbmap.AddTableWithName(Article{}, (&Article{}).TableName()).SetKeys(true, "id")
	dbmap.AddTableWithName(Category{}, (&Category{}).TableName()).SetKeys(true, "id")
	dbmap.AddTableWithName(ArticleCategory{}, (&ArticleCategory{}).TableName()).SetKeys(false, "article_id", "category_id")

	return dbmap, nil
}
