//index.js
const path = require("path");
const express = require("express");
const pool = require("./db");
const app = express();
const cors = require("cors");

//middleware
app.use(cors());
app.use(express.json()); //req.body

//GET USERS
app.get("/users", async (req, res) => {
  try {
    const allUsers = await pool.query(
      "SELECT * FROM users ORDER BY user_id ASC"
    );
    res.json(allUsers.rows);
  } catch (err) {
    console.error(err.message);
  }
});

//GET A USER
app.get("/users/:user_id", async (req, res) => {
  try {
    const { user_id } = req.params;
    const todo = await pool.query("SELECT * FROM users WHERE user_id = $1", [
      user_id,
    ]);

    res.json(todo.rows[0]);
  } catch (err) {
    console.error(err.message);
  }
});

//CREATE USER
app.post("/users", async (req, res) => {
  try {
    const { name, email, password } = req.body;
    const newUser = await pool.query(
      "INSERT INTO users (name, email, password) VALUES($1, $2, $3) RETURNING *",
      [name, email, password]
    );

    res.json(newUser.rows[0]);
  } catch (err) {
    console.error(err.message);
  }
});

//UPDATE USER
app.put("/users/:user_id", async (req, res) => {
  try {
    const { user_id } = req.params;
    const { name, email, password } = req.body;
    const updateTodo = await pool.query(
      "UPDATE users SET name, email, password = $1, $2, $3 WHERE user_id = $4",
      [name, email, password, user_id]
    );

    res.json("User was updated!");
  } catch (err) {
    console.error(err.message);
  }
});

//DELETE USER
app.delete("/users/:user_id", async (req, res) => {
  try {
    const { user_id } = req.params;
    const deleteTodo = await pool.query(
      "DELETE FROM users WHERE user_id = $1",
      [user_id]
    );
    res.json("User was deleted!");
  } catch (err) {
    console.log(err.message);
  }
});

// Hacer que node sirva los archivos de nuestro app React
app.use(express.static(path.resolve(__dirname, "./frontend/build")));

// Todas las peticiones GET que no hayamos manejado en las líneas anteriores retornaran nuestro app React
app.get("*", (req, res) => {
  res.sendFile(path.resolve(__dirname, "./frontend/build", "index.html"));
});

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
