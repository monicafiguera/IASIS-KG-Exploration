import React, {Component} from 'react';
import * as d3 from "d3";

class VennDiagram extends Component {
    constructor(props) {
        super(props);
        this.paintGraph = this.paintGraph.bind(this);
    }

    componentDidMount() {
        this.paintGraph();
    }

    paintGraph() {
        var sets = [
                    {sets:["Audio"], figure: 8.91, label: "Audio", size: 8.91},
                    {sets:["Direct Buy"], figure: 34.53, label: "Direct Buy", size: 34.53},
                    {sets:["Branded Takeover"], figure: 40.9, label: "Branded Takeover", size: 40.9},
                    {sets: ["Audio", "Direct Buy"], figure: 5.05, label: "Audio and Direct Buy", size: 5.05},
                    {sets: ["Audio", "Branded Takeover"], figure: 3.65, label: "Audio and Branded Takeover", size: 3.65},
                    {sets: ["Direct Buy", "Branded Takeover"], figure: 4.08, label: "Direct Buy and Branded Takeover", size: 4.08},
                    {sets: ["Audio", "Direct Buy", "Branded Takeover"], figure: 2.8, label: "Audio, Direct Buy, and Branded Takeover", size: 2.8}
                    ];

        var chart = venn.VennDiagram()
            .width(500)
            .height(400);

        var div = d3.select("#vennDiagram").datum(sets).call(chart);
            div.selectAll("text").style("fill", "white");
            div.selectAll(".venn-circle path")
                    .style("fill-opacity", .8)
                    .style("stroke-width", 1)
                    .style("stroke-opacity", 1)
                    .style("stroke", "fff");

        var tooltip = d3.select("#vennDiagram").append("div")
            .attr("class", "venntooltip");

        div.selectAll("g")
            .on("mouseover", function(d, i) {
                // sort all the areas relative to the current item
                venn.sortAreas(div, d);

                // Display a tooltip with the current size
                tooltip.transition().duration(40).style("opacity", 1);
                tooltip.text(d.size + "% of Audience One saw " + d.label);

                // highlight the current path
                // highlight the current path
                var selection = d3.select(this).transition("tooltip").duration(400);
                selection.select("path")
                    .style("stroke-width", 3)
                    .style("fill-opacity", d.sets.length === 1 ? .8 : 0)
                    .style("stroke-opacity", 1);
            })

            .on("mousemove", function() {
                tooltip.style("left", (d3.event.pageX) + "px")
                       .style("top", (d3.event.pageY - 28) + "px");
            })

            .on("mouseout", function(d, i) {
                tooltip.transition().duration(2000).style("opacity", 0);
                var selection = d3.select(this).transition("tooltip").duration(400);
                selection.select("path")
                    .style("stroke-width", 3)
                    .style("fill-opacity", d.sets.length === 1 ? .8 : 0)
                    .style("stroke-opacity", 1);
            });
    }

    render() {
        return(
            <div className="venn-diagram" id={"vennDiagram"} />
        );
    }

}

export default VennDiagram;