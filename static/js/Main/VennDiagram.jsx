import React, {Component} from 'react';
import * as d3 from "d3";

class VennDiagram extends Component {
    constructor(props) {
        super(props);

        this.state = { clickedArea: null };
        this.paintGraph = this.paintGraph.bind(this);
        this.checkArrayEquality = this.checkArrayEquality.bind(this);
    }

    componentDidMount() {
        this.paintGraph();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState !== this.state) {
            this.props.dialogContent(this.state.clickedArea);
        }
    }

    checkArrayEquality(arr1, arr2) {
        var a1l = arr1.length;
        var a2l = arr2.length;
        var n = a1l > a2l ? a1l : a2l;
        var isEqual = true;

        for (var i=0; i<n; i++) {
            if (arr1[i] !== arr2[i]) {
                isEqual = false;
            }
        }

        return isEqual;
    }

    paintGraph() {
        var that = this;

        var realData = [
                   {"sets": ["DDI"], "size": 347403},
                   {"sets": ["CRD"], "size": 345116},
                   {"sets": ["PubMedDI"], "size": 280},
                   {"sets": ["DDI", "CRD"], "size": 109534},
                   {"sets": ["DDI", "PubMedDI"], "size": 54},
                   {"sets": ["CRD", "PubMedDI"], "size": 55},
                   {"sets": ["DDI", "CRD", "PubMedDI"], "size": 32}
                   ];

        var data = [
                   {"sets": ["DDI"], "label": "DDI drugDrugInteraction (DrugBank)   237,847", "size": 100},
                   {"sets": ["CRD"], "label": "CRD drugDrugInteraction (metabolized by CYP enzyme)   235,559", "size": 100},
                   {"sets": ["PubMedDI"], "label": "PubMedDDI drugDrugInteraction   203", "size": 100},
                   {"sets": ["DDI", "CRD"], "label": "109502", "size": 25},
                   {"sets": ["DDI", "PubMedDI"], "label": "22", "size": 25},
                   {"sets": ["CRD", "PubMedDI"], "label": "23", "size": 25},
                   {"sets": ["DDI", "CRD", "PubMedDI"], "label": "32", "size": 15}
                   ];

        var sets = data;

        var chart = venn.VennDiagram()
                     .width(600)
                     .height(600);

        var div = d3.select("#venn");
        div.datum(sets).call(chart);

        // Changing style
        d3.select("#venn").datum(sets).call(chart);
                var colours = ['green', 'orchid', 'red', 'yellow'];
                d3.selectAll("#venn .venn-circle path")
                    .style("stroke-width", 10)
                    .style("fill", function(d,i) {
                        //var s = d.sets[0];
                        return colours[i];
                    });

        d3.selectAll("#venn .venn-circle text")
                    .style("fill", function(d,i) { return 'black'})
                    .style("font-size", "14px")
                    .style("font-weight", "300");

        // Adding tooltips on hover
        var tooltip = d3.select("body").append("div")
            .attr("class", "venntooltip");

        // add listeners to all the groups to display tooltip on mouseover
        div.selectAll("path")
            .style("stroke-opacity", 0)
            .style("stroke", "#fff")
            .style("stroke-width", 3);
        div.selectAll("g")
            .on("click", function(d, i) {
                console.log("clicked in diagram", d)
                that.setState({clickedArea: d.label})
            })
            .on("mouseover", function(d, i) {
                var realSize = 0;

                for (var i=0; i < realData.length; i++) {
                    var areEqual = that.checkArrayEquality(realData[i].sets, d.sets);
                    if (areEqual) {
                      realSize = realData[i].size;
                    }
                }

                var inter = realSize === 1 ? "1 interaction" : realSize + " interactions";

                // sort all the areas relative to the current item
                venn.sortAreas(div, d);

                // Display a tooltip with the current size
                tooltip.transition().duration(400).style("opacity", 1);
                tooltip.text(inter);

                // highlight the current path
                var selection = d3.select(this).transition("tooltip").duration(400);
                selection.select("path")
                    .style("fill-opacity", .7)
                    .style("stroke-opacity", 1);
            })
            .on("mousemove", function() {
                tooltip.style("left", (d3.event.pageX) + "px")
                       .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function(d, i) {
                tooltip.transition().duration(400).style("opacity", 0);
                var selection = d3.select(this).transition("tooltip").duration(400);
                selection.select("path")
                    .style("fill-opacity", d.sets.length === 1 ? .25 : .0)
                    .style("stroke-opacity", 0);
            });

    }

    render() {
        return(
            <div className="venn-diagram" id={"venn"} />
        );
    }

}

export default VennDiagram;