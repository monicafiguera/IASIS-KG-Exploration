
data = d3.csv("/static/js/libs/data/10_o.csv", function(error, data) {
    var dataStr = "";
    dataStr += "AA,GENERAL,GASTROINTESTINAL,ENDOCRINE,CUTANEOUS,PNEUMOLOGICAL,ANALYTICAL,NEUROLOGICAL,OTHER,CARDIOLOGICAL\n";
    data.forEach(function(d) {
        var keys = Object.keys(d);
        for (var i=0; i<Object.keys(d).length; i++) {

            var elem = d[keys[i]];
            dataStr += elem;
            if (i < keys.length - 1) {
                dataStr += ",";
            }
        }
        dataStr += "\n";
    });
    console.log("data",dataStr);

    var matrix = csvToArray(dataStr);

    console.log("matrix", matrix);

    var nodes = matrix[0].slice(1);
    console.log("**",nodes);

    var links = [];
    nodes.forEach(function(d, i) {
      matrix[i+1].slice(1).forEach(function(e, j) {
        if(matrix[i+1][j+1] > 0) {
          links.push({source: i, target: j, weight: parseFloat(e)});
        }
      });
    });

    console.log("links",links);

    createJSON(nodes, links);
});


function csvToArray (csv) {
    rows = csv.split("\n");

    return rows.map(function (row) {
    	return row.split(",");
    });
}

function createJSON(nodes, links) {
    var result = [];

    for (var i=0; i<nodes.length; i++) {
        result.push({
          "data": {
            "id": i.toString(),
            "idInt": parseInt(i),
            "name": nodes[i],
            "score": 0.006769776522008331,
            "query": true,
            "gene": true
          },
          "position": {
            "x": 481.0169597039117,
            "y": 384.8210888234145
          },
          "group": "nodes",
          "removed": false,
          "selected": false,
          "selectable": true,
          "locked": false,
          "grabbed": false,
          "grabbable": true,
          "classes": "fn10273 fn6944 fn9471 fn10569 fn8023 fn6956 fn6935 fn8147 fn6939 fn6936 fn6629 fn7928 fn6947 fn8612 fn6957 fn8786 fn6246 fn9367 fn6945 fn6946 fn10024 fn10022 fn6811 fn9361 fn6279 fn6278 fn8569 fn7641 fn8568 fn6943"
        })
    }
    for (var i=0; i<links.length; i++) {
        result.push(
            {"data": {
                "source": links[i].source.toString(),
                "target": links[i].target.toString(),
                "weight": links[i].weight,
                "group": "coexp",
                "networkId": 1133,
                "networkGroupId": 18,
                "intn": true,
                "rIntnId": i + 2,
                "id": "e" + i.toString()
              },
              "position": {},
              "group": "edges",
              "removed": false,
              "selected": false,
              "selectable": true,
              "locked": false,
              "grabbed": false,
              "grabbable": true,
              "classes": ""
            }
        );
    }
    console.log(result);

}