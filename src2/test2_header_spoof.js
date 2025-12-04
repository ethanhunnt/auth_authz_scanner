// test2_header_spoof.js
const express = require("express");
const app = express();

// ❌ Authorization bypass: trusts identity headers directly
app.get("/internal-api", (req, res) => {
  const email = req.headers["x-email"];
  const role = req.headers["x-role"];

  // This trusts whatever attacker sends
  const user = { email, role };

  // Sensitive internal function
  if (user.role === "admin") {
    return res.send("Sensitive admin data");
  }

  res.send("User access");
});

app.listen(4000);
