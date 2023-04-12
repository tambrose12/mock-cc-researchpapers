import { Route, Switch } from "react-router";
import Home from "./Home";
// import Navbar from "./Navbar";
// import Restaurant from "./Restaurant";

function App() {
  return (
    <>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
      </Switch>
    </>
  );
}

export default App;
