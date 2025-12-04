// test6_csharp_missing_authorize.cs
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("[controller]")]
public class AdminController : ControllerBase
{
    // ❌ Missing [Authorize]
    [HttpGet("settings")]
    public IActionResult GetSettings([FromHeader] string role)
    {
        // ❌ Trusts header blindly
        if (role == "admin")
            return Ok("Admin settings");

        return Unauthorized();
    }
}
