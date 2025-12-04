<?php
// test7_php_cookie.php

// ❌ Authentication bypass: only checks cookie presence
if (isset($_COOKIE['session'])) {
    echo "Welcome user";
} else {
    echo "Unauthorized";
}
