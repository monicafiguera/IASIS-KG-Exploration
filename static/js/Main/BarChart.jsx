import React, {Component} from 'react';

export default class BarChart extends Component {
    constructor(props) {
        super(props);

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
            <div id="barchart" />
        );
    }

}