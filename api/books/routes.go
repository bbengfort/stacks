package books

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	"github.com/go-chi/chi"
	"github.com/go-chi/render"
)

// Routes returns the internal mux for the Books app
func Routes() *chi.Mux {
	router := chi.NewRouter()
	router.Get("/", List)
	router.Post("/", Create)
	router.Get("/{pk}", Detail)
	router.Put("/{pk}", Update)
	router.Delete("/{pk}", Delete)
	return router
}

// List the available books based on the request
func List(w http.ResponseWriter, r *http.Request) {
	bookList := make([]*Book, 0, len(books))
	for _, book := range books {
		bookList = append(bookList, book)
	}
	render.JSON(w, r, bookList)
}

// Create a new book with the posted data
func Create(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var book *Book
	if err := decoder.Decode(&book); err != nil {
		http.Error(w, http.StatusText(422), 422)
		return
	}

	sequence++
	book.ID = sequence
	books[int64(book.ID)] = book

	response := make(map[string]interface{})
	response["success"] = true
	response["message"] = fmt.Sprintf("created '%s'", book.Title)
	render.JSON(w, r, response)
}

// Detail returns a single book's information
func Detail(w http.ResponseWriter, r *http.Request) {
	pk, err := strconv.ParseInt(chi.URLParam(r, "pk"), 10, 64)
	if err != nil {
		http.Error(w, http.StatusText(400), 400)
		return
	}

	book, ok := books[pk]
	if !ok {
		http.Error(w, http.StatusText(404), 404)
		return
	}

	render.JSON(w, r, book)
}

// Update a book with the put data
func Update(w http.ResponseWriter, r *http.Request) {
	pk, err := strconv.ParseInt(chi.URLParam(r, "pk"), 10, 64)
	if err != nil {
		http.Error(w, http.StatusText(400), 400)
		return
	}

	book, ok := books[pk]
	if !ok {
		http.Error(w, http.StatusText(404), 404)
		return
	}

	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&book); err != nil {
		http.Error(w, http.StatusText(422), 422)
		return
	}

	response := make(map[string]interface{})
	response["success"] = true
	response["message"] = fmt.Sprintf("updated '%s'", book.Title)
	render.JSON(w, r, response)
}

// Delete a book by its primary key
func Delete(w http.ResponseWriter, r *http.Request) {
	pk, err := strconv.ParseInt(chi.URLParam(r, "pk"), 10, 64)
	if err != nil {
		http.Error(w, http.StatusText(400), 400)
		return
	}

	book, ok := books[pk]
	if !ok {
		http.Error(w, http.StatusText(404), 404)
		return
	}

	delete(books, pk)

	response := make(map[string]interface{})
	response["success"] = true
	response["message"] = fmt.Sprintf("deleted '%s'", book.Title)
	render.JSON(w, r, response)
}
