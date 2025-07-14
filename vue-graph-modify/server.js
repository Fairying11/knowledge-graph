const express = require('express');
const cors = require('cors');
const app = express();

// enable CORS globally
app.use(cors());

// add your routes and middleware here
// ...

// start server
app.listen(8080, () => {
  console.log('Server is listening on port 8080');
});