// Table schema is below.
// https://github.com/oinume/tinyblog/blob/master/migrations/20160503000000_chapter3_create_tables.migration
package model

import (
	"testing"
	"fmt"
)

func TestGorpSelectByPk(t *testing.T) {
	db, err := OpenGorp()
	panicIf(err)
	defer db.Db.Close()

	record, err := db.Get(Blog{}, 1)
	panicIf(err)
	if blog, ok := record.(*Blog); ok { // type assertionしないといけない
		fmt.Printf("%d\n", blog.Id)
	}
}

func TestGormSelectByPk(t *testing.T) {
	db, err := OpenGorm()
	panicIf(err)
	defer db.Close()

	var blog Blog
	// SELECT * FROM `blogs`  WHERE (`id` = ?) ORDER BY `blogs`.`id` ASC LIMIT 1
	if err := db.First(&blog, 1).Error; err != nil {
		panic(err)
	}
	fmt.Printf("%d\n", blog.Id)
}

func TestGorpCompositePk(t *testing.T) {
	db, err := OpenGorp()
	panicIf(err)
	defer db.Db.Close()

	// select `article_id`,`category_id` from `article_categories` where `article_id`=? and `category_id`=?;
	ac, err := db.Get(ArticleCategory{}, 1, 1)
	panicIf(err)
	fmt.Printf("ac = %+v\n", ac)
}

func TestGormCompositePk(t *testing.T) {
	db, err := OpenGorm()
	panicIf(err)
	defer db.Close()

	var ac ArticleCategory
	// 本当は db.First(&ac, 1, 1) と書きたい。バグ？
	// SELECT * FROM `article_categories`  WHERE (article_id = ? AND category_id = ?) ORDER BY `article_categories`.`article_id` ASC LIMIT 1
	if err := db.First(&ac, "article_id = ? AND category_id = ?", 1, 1).Error; err != nil {
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
		// 全てのカラムが更新されてしまう
		// update `articles` set `title`=?, `body`=?, `published`=?, `published_at`=? where `id`=?; [1:"test" 2:"test" 3:true 4:2016-05-01 00:00:00 +0000 UTC 5:1]
		_, err := db.Update(article)
		panicIf(err)
	}
}

func TestGormUpdate(t *testing.T) {
	db, err := OpenGorm()
	panicIf(err)
	defer db.Close()

	var article Article
	if err := db.First(&article, 1).Error; err != nil {
		panic(err)
	}
	// UPDATE `articles` SET `title` = ?, `body` = ?  WHERE `articles`.`id` = ?
	if err := db.Model(&article).Update(Article{Title: "test", Body: "test"}).Error; err != nil {
		panic(err)
	}
}

func panicIf(err error) {
	if err != nil {
		panic(err)
	}
}
