// test5_go_gateway_bypass.go
package main

import (
	"fmt"
	"net/http"
)

// ❌ Internal API missing gateway verification (FIG/FIP)
func internalHandler(w http.ResponseWriter, r *http.Request) {
	// Should validate service tokens, but does nothing
	user := r.Header.Get("X-Email")
	role := r.Header.Get("X-Role")

	// ❌ Identity forged from headers
	if role == "admin" {
		fmt.Fprintf(w, "Internal Admin Data")
		return
	}

	fmt.Fprintf(w, "Internal User Data: "+user)
}

func main() {
	http.HandleFunc("/internal", internalHandler)
	http.ListenAndServe(":8080", nil)
}
