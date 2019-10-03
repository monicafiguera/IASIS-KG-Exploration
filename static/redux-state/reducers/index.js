import { combineReducers } from "redux";

import general   from "./general";
import ui        from "./ui";

const KGExplorationApp = combineReducers({
    general,
    ui
});

export default KGExplorationApp;