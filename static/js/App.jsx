import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Provider } from "react-redux";

import MainContainer        from "./Main/MainContainer";
import SidebarContainer     from "./SidebarContainer";
import HeaderMenu           from "./HeaderMenu";

const App = ({store}) => (
    <Provider store={store}>
        <div className="App">
            <header className="App-header">
                <HeaderMenu />

                <Router>
                    <div id="main-container">
                        <SidebarContainer />

                        <Switch>
                            <Route path="/" exact      component={MainContainer} />
                        </Switch>
                    </div>
                </Router>
            </header>
        </div>
    </Provider>
)

export default App;