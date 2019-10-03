import { connect } from "react-redux";
import { bindActionCreators } from "redux";

import Main from "./Main";

import { changeActiveSidebarTab } from "../../redux-state/actions/ui";
import * as GeneralActions from "../../redux-state/actions/general";

function mapStateToProps(state) {
    return {
        currentDataset: state.general["currentDataset"]
    };
}

function mapDispatchToProps(dispatch) {
    return {
        generalActions: bindActionCreators(GeneralActions, dispatch),
        changeActiveSidebarTab: (index) => dispatch(changeActiveSidebarTab(index)),
    };
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Main);