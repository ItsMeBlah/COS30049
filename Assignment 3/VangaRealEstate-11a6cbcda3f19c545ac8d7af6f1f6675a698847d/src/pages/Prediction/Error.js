import React from "react";
import { Link } from "react-router-dom";
import "./Error.css";

function ErrorPage() {

  return (
    <div className="error">
      <h1>Oops! Something went wrong...</h1>
      <p>No results found for the given address.</p>
      <Link to="/search">Back to Search</Link>
    </div>
  );
}

export default ErrorPage;