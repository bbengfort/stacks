package api

import (
	"log"
	"net/http"

	"github.com/bbengfort/stacks/api/books"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/cors"
	"github.com/go-chi/render"
)

// PackageVersion of the current Stacks API
const PackageVersion = "0.1"

// Routes creates the API router and multiplexer with associated middleware
func Routes() *chi.Mux {
	router := chi.NewRouter()

	// Setup CORS
	cors := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300,
	})

	// Setup middleware
	router.Use(
		render.SetContentType(render.ContentTypeJSON), // Set content-type header as application/json
		middleware.Logger,          // Log API request calls
		middleware.DefaultCompress, // Compress results, mostly gzipping assets and json
		middleware.RedirectSlashes, // Redirect slashes to no slash URL versions
		middleware.Recoverer,       // Recover from panics without crashing server
		cors.Handler,               // Setup cross-origin resource sharing
	)

	// Mount the associated routes from different resources
	router.Route("/api/v1", func(r chi.Router) {
		r.Mount("/books", books.Routes())
	})

	return router
}

// Serve the API, listening on the specified address
func Serve(addr string, debug bool) (err error) {
	router := Routes()

	// Walk and printout all routes
	walkFunc := func(method, route string, handler http.Handler, middlewares ...func(http.Handler) http.Handler) error {
		log.Printf("%s %s\n", method, route)
		return nil
	}

	if err := chi.Walk(router, walkFunc); err != nil {
		return err
	}

	return http.ListenAndServe(addr, router)
}
