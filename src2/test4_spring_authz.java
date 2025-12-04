// test4_spring_authz.java
@RestController
@RequestMapping("/api")
public class UserController {

    // ❌ No @PreAuthorize annotation
    @GetMapping("/admin")
    public String getAdminData(@RequestHeader("X-Role") String role) {
        // ❌ Trusts role from header
        if (role.equals("admin")) {
            return "Sensitive admin info";
        }
        return "Denied";
    }

    // ❌ No authentication enforcement
    @GetMapping("/user")
    public String userData() {
        return "User data with no auth!";
    }
}
