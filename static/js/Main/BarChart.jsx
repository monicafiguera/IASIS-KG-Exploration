import React, {Component} from 'react';
import * as d3 from "d3";

export default class BarChart extends Component {
    constructor(props) {
        super(props);

        this.state = { clickedArea: null };
        this.paintGraph = this.paintGraph.bind(this);
    }

    componentDidMount() {
        this.paintGraph();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState !== this.state) {
        }
    }


    paintGraph() {

    }

    render() {
        return(
            <div className="bar-chart" id={"barChart"} />
        );
    }

}