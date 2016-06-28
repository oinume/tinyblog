package model

import (
	"testing"
	"fmt"
)

func TestGorpSelectOne(t *testing.T) {
	db, err := OpenGorp()
	panicIf(err)
	defer db.Db.Close()

	record, err := db.Get(Blog{}, 1)
	panicIf(err)
	if blog, ok := record.(*Blog); ok { // type assertionしないといけない
		fmt.Printf("%d\n", blog.Id)
	}
}

func TestGormSelectOne(t *testing.T) {
	db, err := OpenGorm()
	panicIf(err)
	defer db.Close()

	var blog Blog
	// SELECT * FROM `blogs`  WHERE (`id` = ?) ORDER BY `blogs`.`id` ASC LIMIT 1
	if err := db.First(&blog, 1).Error; err != nil {
		panicIf(err)
	}
	fmt.Printf("%d\n", blog.Id)
}

func TestGorpCompositePk(t *testing.T) {
	db, err := OpenGorp()
	panicIf(err)
	defer db.Db.Close()

	// select `article_id`,`category_id` from `article_categories` where `article_id`=? and `category_id`=?;
	ac, err := db.Get(ArticleCategory{}, 1, 1)
	if err != nil {
		panic(err)
	}
	fmt.Printf("ac = %+v\n", ac)
}

func TestGorpUpdate(t *testing.T) {
	db, err := OpenGorp()
	panicIf(err)
	defer db.Db.Close()

	record, err := db.Get(Article{}, 1)
	panicIf(err)
	if article, ok := record.(*Article); ok {
		article.Title = "test"
		article.Body = "test"
		_, err := db.Update(article)
		// update `articles` set `title`=?, `body`=?, `published`=?, `published_at`=? where `id`=?; [1:"test" 2:"test" 3:true 4:2016-05-01 00:00:00 +0000 UTC 5:1]
		panicIf(err)
	}
}

func panicIf(err error) {
	if err != nil {
		panic(err)
	}
}
