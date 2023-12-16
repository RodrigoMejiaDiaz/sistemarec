import React, { Fragment, useState } from "react";

const InputUser = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmitForm = async (e) => {
    e.preventDefault();
    try {
      const body = { name, email, password };
      const response = await fetch("/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      window.location = "/";
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <Fragment>
      <h1 className="text-center mt-5">Pern Todo List</h1>
      <form className="d-flex mt-5" onSubmit={onSubmitForm}>
        <input
          type="text"
          className="form-control"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          className="form-control"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="text"
          className="form-control"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="btn btn-success">Add</button>
      </form>
    </Fragment>
  );
};

export default InputUser;
