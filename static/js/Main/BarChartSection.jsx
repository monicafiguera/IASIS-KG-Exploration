import React from "react";
import {
    Col,
    Row } from "reactstrap";
import Modal from "../Modal";
import BarChart from "./BarChart";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes }         from "@fortawesome/free-solid-svg-icons";

export default class BarChartSection extends React.Component {
    constructor(props) {
        super(props);

        this.state = { showModal: false,
                       content: ''};

        this.closeModal = this.closeModal.bind(this);
        this.openModal  = this.openModal.bind(this);
        this.dialogContent = this.dialogContent.bind(this);

    }

    openModal(content) {
        this.setState({showModal: true, content: content});
    }

    closeModal() {
        this.setState({showModal: false});
    }


    componentDidMount() {
        this.props.changeActiveSidebarTab(1);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
    }

    dialogContent(content) {
        console.log("content", content);
        this.openModal(content);
    }

    render() {
        return (
            <div id="body-container" className="contents-container">
                <Row className="body-content-header">
					<Col lg="12">
						<h3 className="title" style={{color: "black"}}>IASIS-KG Exploration</h3>
						<div tabIndex="-1" className="sidebar-divider"></div>
					</Col>
				</Row>

                <Row>
                    <Col lg="12">
                        <BarChart />
                    </Col>
                </Row>

                <Modal
                    containerClassName="modal-dialog modal-add-ds"
                    closeOnOuterClick={false}
                    show={this.state.showModal}
                    onClose={this.closeModal}
                >
                    <div className="modal-container">
                        <div className="modal-header">
                            <p>Clicked on area: -</p>
                            <FontAwesomeIcon icon={faTimes}
                                             style={{color: "black", cursor: "pointer"}}
                                             onClick={this.closeModal}/>
                        </div>

                        <div className="modal-body">
                            <a href={"http://www.wineandcheesemap.com/"}>Click to open link</a>
                        </div>
                    </div>
                </Modal>
            </div>
        );
    }
}