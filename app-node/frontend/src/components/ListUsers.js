import React, { Fragment, useEffect, useState } from "react";

// import EditTodo from "./EditTodo";

const ListUsers = () => {
  const [users, setUsers] = useState([]);

  //delete todo function

  const deleteUser = async (user_id) => {
    try {
      const deleteUser = await fetch(`/users/${user_id}`, {
        method: "DELETE",
      });

      setUsers(users.filter((user) => user.user_id !== user_id));
    } catch (err) {
      console.error(err.message);
    }
  };

  const getUsers = async () => {
    try {
      const response = await fetch("/users");
      const jsonData = await response.json();

      setUsers(jsonData);
    } catch (err) {
      console.error(err.message);
    }
  };

  useEffect(() => {
    getUsers();
  }, []);

  console.log(users);

  return (
    <Fragment>
      {" "}
      <table class="table mt-5 text-center">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Password</th>
            <th>Edit</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {/*<tr>
            <td>John</td>
            <td>Doe</td>
            <td>john@example.com</td>
          </tr> */}
          {users.map((user) => (
            <tr key={user.user_id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.password}</td>
              <td>a{/* <EditUser user={user} /> */}</td>
              <td>
                <button
                  className="btn btn-danger"
                  onClick={() => deleteUser(user.user_id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Fragment>
  );
};

export default ListUsers;
