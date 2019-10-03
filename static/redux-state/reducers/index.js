import { combineReducers } from "redux";

import general   from "./general";
import ui        from "./ui";

const ontarioApp = combineReducers({
    general,
    ui
});

export default ontarioApp;