// test8_kotlin_idor.kt
@GetMapping("/files")
fun getFile(@RequestParam id: String): String {
    // ❌ No authentication
    // ❌ No authorization
    // ❌ Direct access to file by ID = IDOR
    return "Returning file with id: $id"
}
