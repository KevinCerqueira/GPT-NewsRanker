import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import List from "./components/List";

const Routes = () => {
  return (
    <Router>
      <div className="App">
        <Route exact path="/*" component={List} />
      </div>
    </Router>
  );
};

export default Routes;
