// test1_express_auth_bypass.js
const express = require('express');
const app = express();

// ❌ Authentication bypass: checks only for cookie header presence
function authMiddleware(req, res, next) {
  if (req.headers['cookie']) {
    // Should validate cookie value or session, but does not.
    console.log("User authenticated!");
    next();
  } else {
    res.status(401).send("Unauthorized");
  }
}

app.get("/admin", authMiddleware, (req, res) => {
  res.send("Admin Panel");
});

app.listen(3000);
