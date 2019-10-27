Promise.all([
  fetch('/static/js/libs/cy-style.json')
    .then(function(res) {
      return res.json();
    }),
  fetch('/static/jsonFilesGeneration/jsons_all/json_line1/line1_all_exp.json')
    .then(function(res) {
      return res.json();
    })
])
  .then(function(dataArray) {


  var cy = (window.cy = cytoscape({
    container: document.getElementById("cy"),
    style: dataArray[0],
    elements: dataArray[1],
    layout: {
      name: "cola"
    }
  }));

  function makePopper(ele) {
    let ref = ele.popperRef(); // used only for positioning

    ele.tippy = tippy(ref, { // tippy options:
      content: () => {
        let content = document.createElement('div');
        if (ele._private.group === 'nodes') {
            content.innerHTML = "No. patients: " + ele.data('patients');
        } else {
            content.innerHTML = "Patients: " + ele.data('patients');
        }

        return content;
      },
      trigger: 'manual' // probably want manual mode
    });
  }

  cy.ready(function() {
    cy.elements().forEach(function(ele) {
      makePopper(ele);
    });
  });

  cy.elements().unbind('mouseover');
  cy.elements().bind('mouseover', (event) => {
      event.target.tippy.show();
       cy.elements().forEach(function(ele) {
           if (ele !== event.target) {
            ele.tippy.hide();
           }
       });
  }) ;

});