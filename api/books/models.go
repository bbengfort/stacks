package books

var sequence = uint64(3)

// The initial list of books to serve
var books = map[int64]*Book{
	1: {
		ID:     1,
		Title:  "On the Road",
		Author: "Jack Kerouac",
		Read:   true,
	},
	2: {
		ID:     2,
		Title:  "Harry Potter and the Philosopher's Stone",
		Author: "J.K. Rowling",
		Read:   false,
	},
	3: {
		ID:     3,
		Title:  "Green Eggs and Ham",
		Author: "Dr. Seuss",
		Read:   true,
	},
}

// Book represents something in a reading list
type Book struct {
	ID     uint64 `json:"id"`     // The id of the book
	Title  string `json:"title"`  // The title of the book
	Author string `json:"author"` // The full name of the author of the book
	Read   bool   `json:"read"`   // Whether or not the book has been read
}
